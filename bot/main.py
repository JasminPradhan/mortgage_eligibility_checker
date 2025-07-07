from fastapi import FastAPI, HTTPException, Depends, Security, Query, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import json
import os
import hashlib
from prompt import chain
from typing import Optional



app = FastAPI()
network = HTTPBasic()


class User(BaseModel):
    username: str
    password_hash: str
    customer_id: str

def load_users(file: str) -> dict:
    try:
        with open(file) as f:
            data = json.load(f)
            return {user['username']: user for user in data}
    except FileNotFoundError:
        return {}

users_db = load_users("users.json")

with open("customer_profiles.json") as f:
    cp = json.load(f)
    p_db = {p["customer_id"]: p for p in cp}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algo, iter_str, salt_hex, hash_hex = hashed_password.split('$')
        iterations = int(iter_str)
        salt = bytes.fromhex(salt_hex)
        hash_bytes = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt, iterations)
        return hash_bytes.hex() == hash_hex
    except Exception as e:
        return False

def authenticate(credentials: HTTPBasicCredentials = Security(network)):
    user_data = users_db.get(credentials.username)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(credentials.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_data


@app.get("/me")
def get_me(curr_user: dict = Depends(authenticate)):
    cid = curr_user["customer_id"]
    prof = p_db.get(cid)
    if not prof:
        raise HTTPException(status_code=404, detail="Customer profile not found")
    return {"customer_id": cid, "name": prof["name"]}

@app.get("/profile/{customer_id}")
def get_profile(customer_id:str):
    p = p_db.get(customer_id)
    if not p:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return{
        "name": p["name"],
        "age": p["age"],
        "credit_score": p["credit_score"],
        "annual_income": p["annual_income"],
        "spending_habits": p["spending_habits"]
    }
# end point
from fastapi.responses import JSONResponse

@app.post("/assess")
def post_res(customer_id: Optional[str] = Query(None),
                query: str = Body("", embed=True, title="user_query"),
             curr_user: dict = Depends(authenticate)):
    cid = customer_id or curr_user["customer_id"]
    print(f"[INFO] Received assess request for customer_id: {cid}")

    p = p_db.get(cid)
    if not p:
        print("[ERROR] Profile not found.")
        raise HTTPException(status_code=404, detail="Customer profile not found")

    # Validate required fields early
    required_fields = ["age", "credit_score", "annual_income"]
    missing = [field for field in required_fields if field not in p]
    if missing:
        print(f"[ERROR] Missing fields: {missing}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Missing field(s) in profile: {', '.join(missing)}"}
        )

    try:
        print("[DEBUG] Profile data:", p)
        # 👇 Use invoke instead of run
        res = chain.invoke({
            "age": p["age"],
            "credit_score": p["credit_score"],
            "annual_income": p["annual_income"]
        })
        return {"answer": res}
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

if __name__ == '__main__':
    pass

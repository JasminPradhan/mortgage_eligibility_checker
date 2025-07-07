# Mortgage Eligibility Checker

This is an LLM based mortgage assistant chatbot designed to provide preliminary eligibility assessments based on a user's financial profile.

## The Tech Stack Used:
- FastAPI for backend logic and secure routing

- LangChain + Ollama (LLaMA 3) for natural language reasoning

- HTTP Basic Authentication to protect user data

- Streamlit (optional) for a simple, interactive frontend

- JSON-based mock databases for user and profile management

## What It Does:
- Checks mortgage eligibility based on:

  - ✅ Age (must be ≥ 21)

  - ✅ Credit Score (must be ≥ 700)

  - ✅ Annual Income (must be ≥ 50,000)

- Gives preliminary, non-committal assessments — never promises approval

- Handles both self-checks and third-party (via customer ID) assessments
- Uses soft guardrails to prevent financial disclosure or misuse


## What to be fixed:
Gracefully handling customer's vague or unrelated questions.


## Mortgage Bot Workflow
```mermaid
flowchart TD
    A[User Authentication] --> B[ Identify Customer ID]
    B --> C{Profile Exists?}
    C -- Yes --> D[ Fetch Customer Profile]
    C -- No --> E[ Return 'Profile not found']
    D --> F{All Required Fields Present?}
    F -- No --> G[ Ask for missing fields]
    F -- Yes --> H[ Run LangChain with LLM]
    H --> I[ Get Bot Response]
    I --> J[ Return Answer to User]
```

## How to run the code:

### Backend:
In the terminal:
```
cd bot
fastapi dev main.py
```

### Frontend:
Open another terminal:
```
streamlit run app.py
```
 

## Users Conversations

#### For John Doe

![Screenshot (197)](https://github.com/user-attachments/assets/2237431a-24dd-4540-b21e-01dcb4417524)
![Screenshot (198)](https://github.com/user-attachments/assets/62e41aca-97ca-4516-ab3d-035d539a7985)
![Screenshot (199)](https://github.com/user-attachments/assets/22f6c2b8-1419-40af-8227-8e73b77b79d9)
![Screenshot (200)](https://github.com/user-attachments/assets/fc0fe38a-9eaa-471e-a206-09187a1a18ef)

#### For Jane Smith
![Screenshot (196)](https://github.com/user-attachments/assets/0b47bb59-9d17-4814-9f3b-8e6d98b69726)
![Screenshot (195)](https://github.com/user-attachments/assets/df7b23d5-67b5-4a09-9c94-061973c908e6)

#### For Evelyn Goods
![Screenshot (194)](https://github.com/user-attachments/assets/445df7e8-f9ae-4591-93d1-94012442804e)
![Screenshot (193)](https://github.com/user-attachments/assets/62166beb-f6b0-42cd-96f6-5f60ea2de097)

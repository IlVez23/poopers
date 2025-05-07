import sys
import os
from datetime import datetime

# Add the /app directory to the Python path
sys.path.insert(0, '/poopers')

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models 
import crud
import auth
from jose import jwt, JWTError

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token missing")
    try:
        payload = jwt.decode(token.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = crud.get_user_by_username(db, username)
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Token invalid")

@app.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.create_user(db, username, password)
    return {"message": "User created successfully", "username": user.username}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token}

@app.post("/questionnaire")
def submit_questionnaire(data: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    for q, a in data.items():
        crud.save_questionnaire_response(db, user.id, q, a)
    return {"msg": "Saved"}

@app.post("/daily_input")
def submit_daily_input(data: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        print(f"Received data: {data}")  # Debug log
        # Convert date string to date object
        poop_date = datetime.strptime(data["poop_date"], "%Y-%m-%d").date()
        # Ensure count is an integer
        poop_count = int(data["poop_count"])
        
        print(f"Processed data - date: {poop_date}, count: {poop_count}")  # Debug log
        
        crud.save_daily_input(
            db, 
            user.id, 
            poop_date, 
            poop_count,
            data["poop_type"],
            data["poop_color"],
            data["poop_size"]
        )
        return {"msg": "Saved"}
    except ValueError as e:
        print(f"ValueError: {str(e)}")  # Debug log
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")

@app.get("/stats")
def get_stats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_stats(db, user.id)
from fastapi import APIRouter, HTTPException, Depends
from database import database
from models import User, UserLogin
from auth.auth_handler import create_access_token
from auth.auth_bearer import JWTBearer
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
async def register_user(user: User):
    existing_user = await database.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    user.password = hashed_pwd
    result = await database.users.insert_one(user.dict())
    return {"message": "User registered successfully", "id": str(result.inserted_id)}

@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await database.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        data={"sub": db_user["email"], "role": db_user["role"]},
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile", dependencies=[Depends(JWTBearer())])
async def get_profile(token_data=Depends(JWTBearer())):
    user = await database.users.find_one({"email": token_data["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"username": user["username"], "email": user["email"], "role": user["role"]}

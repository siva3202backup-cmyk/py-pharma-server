from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import User
from app.schemas.common import AuthResponse, LoginRequest, RegisterRequest, UserOut
from app.security import create_token, hash_password, verify_password
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register",response_model=AuthResponse,status_code=201)
def register(body:RegisterRequest,db:Session=Depends(get_db)):
    user=User(name=body.name or body.email,email=str(body.email).lower(),password=hash_password(body.password),role="CUSTOMER")
    db.add(user)
    try: db.commit(); db.refresh(user)
    except IntegrityError: db.rollback(); raise HTTPException(status_code=409,detail="Email already exists")
    return {"token":create_token(user),"user":user}
@router.post("/login",response_model=AuthResponse)
def login(body:LoginRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==str(body.email).lower()))
    if not user or not verify_password(body.password,user.password or ""): raise HTTPException(status_code=401,detail="Invalid credentials")
    return {"token":create_token(user),"user":user}

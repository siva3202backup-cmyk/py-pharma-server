from datetime import datetime, timedelta, timezone
import bcrypt, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.entities import User

bearer=HTTPBearer(auto_error=False)
def hash_password(value:str)->str: return bcrypt.hashpw(value.encode(),bcrypt.gensalt(rounds=10)).decode()
def verify_password(value:str, hashed:str)->bool:
    try: return bcrypt.checkpw(value.encode(),hashed.encode())
    except (ValueError, TypeError): return False
def create_token(user:User)->str:
    now=datetime.now(timezone.utc); payload={"id":user.id,"email":user.email,"role":user.role,"iat":now,"exp":now+timedelta(minutes=settings.jwt_expires_minutes)}
    return jwt.encode(payload,settings.jwt_secret,algorithm=settings.jwt_algorithm)
def current_user(credentials:HTTPAuthorizationCredentials|None=Depends(bearer),db:Session=Depends(get_db))->User:
    if not credentials: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    try: payload=jwt.decode(credentials.credentials,settings.jwt_secret,algorithms=[settings.jwt_algorithm]); uid=int(payload["id"])
    except Exception: raise HTTPException(status_code=401,detail="Invalid token")
    user=db.get(User,uid)
    if not user: raise HTTPException(status_code=401,detail="Invalid token")
    return user
def admin_user(user:User=Depends(current_user))->User:
    if user.role!="ADMIN": raise HTTPException(status_code=403,detail="Admin access required")
    return user

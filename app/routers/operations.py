from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import Integer, extract, func, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Coupon,Order,Payment,Product,Review,User
from app.schemas.common import PaymentCreate
from app.security import admin_user,current_user
router=APIRouter(prefix="/api",tags=["Payments and Administration"])
@router.get("/coupons")
def coupons(db:Session=Depends(get_db)): return db.scalars(select(Coupon).where(Coupon.is_active.is_(True)).order_by(Coupon.id)).all()
@router.get("/payments")
def payments(db:Session=Depends(get_db),_=Depends(admin_user)): return db.scalars(select(Payment).order_by(Payment.id.desc())).all()
@router.post("/payments/create",status_code=201)
def payment_create(body:PaymentCreate,db:Session=Depends(get_db),_=Depends(current_user)):
    p=Payment(**body.model_dump(),transaction_id=f"TXN-{int(datetime.now(timezone.utc).timestamp()*1000)}",payment_status="SUCCESS"); db.add(p); db.commit(); db.refresh(p); return p
@router.post("/payments/verify")
def verify(_=Depends(current_user)): return {"verified":True}
@router.get("/reports/monthly-sales")
def monthly(db:Session=Depends(get_db),_=Depends(admin_user)):
    m=func.to_char(Order.created_at,"YYYY-MM").label("month"); return [dict(x._mapping) for x in db.execute(select(m,func.sum(Order.total).label("total")).group_by(m).order_by(m)).all()]
@router.get("/reports/yearly-sales")
def yearly(db:Session=Depends(get_db),_=Depends(admin_user)):
    y=extract("year",Order.created_at).cast(Integer).label("year"); return [dict(x._mapping) for x in db.execute(select(y,func.sum(Order.total).label("total")).group_by(y).order_by(y)).all()]
@router.get("/reports/sales")
def sales(year:int=datetime.now().year,db:Session=Depends(get_db),_=Depends(admin_user)):
    m=extract("month",Order.created_at).cast(Integer).label("month"); rows=db.execute(select(m,func.sum(Order.total).label("total")).where(extract("year",Order.created_at)==year).group_by(m).order_by(m)).all(); return {"year":year,"months":[dict(r._mapping) for r in rows]}
@router.get("/reports/inventory")
def inventory(db:Session=Depends(get_db),_=Depends(admin_user)): return db.scalars(select(Product).where(Product.stock<40).order_by(Product.stock).limit(100)).all()
@router.get("/admin/dashboard")
def dashboard(db:Session=Depends(get_db),_=Depends(admin_user)):
    return {"products":db.scalar(select(func.count()).select_from(Product)),"orders":db.scalar(select(func.count()).select_from(Order)),"revenue":float(db.scalar(select(func.coalesce(func.sum(Order.total),0))) or 0),"users":db.scalar(select(func.count()).select_from(User)),"reviews":db.scalar(select(func.count()).select_from(Review))}

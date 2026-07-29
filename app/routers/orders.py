from datetime import datetime, timezone
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Order,OrderItem,Product,User
from app.schemas.common import OrderCreate
from app.security import admin_user,current_user
router=APIRouter(prefix="/api/orders",tags=["Orders"])
@router.post("",status_code=201)
def create_order(body:OrderCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    try:
        total=Decimal("0"); resolved=[]
        for item in body.items:
            p=db.get(Product,item.product_id)
            if not p: raise HTTPException(404,"Product not found")
            if (p.stock or 0)<item.quantity: raise HTTPException(400,"Insufficient stock")
            price=p.sale_price if p.sale_price is not None else p.price or Decimal("0"); total+=price*item.quantity; resolved.append((item,p,price))
        o=Order(order_number=f"ORD-{int(datetime.now(timezone.utc).timestamp()*1000)}",user_id=user.id,total=total,status="Processing",payment_status="Pending" if body.payment_method=="Cash on Delivery" else "Paid",payment_method=body.payment_method); db.add(o); db.flush()
        for item,p,price in resolved: db.add(OrderItem(order_id=o.id,product_id=p.id,quantity=item.quantity,price=price)); p.stock-=item.quantity
        db.commit(); db.refresh(o); return o
    except: db.rollback(); raise
@router.get("/my")
def my_orders(db:Session=Depends(get_db),user:User=Depends(current_user)): return db.scalars(select(Order).where(Order.user_id==user.id).order_by(Order.id.desc())).all()
@router.get("")
def all_orders(db:Session=Depends(get_db),_:User=Depends(admin_user)): return db.scalars(select(Order).order_by(Order.id.desc())).all()
@router.get("/{order_id}")
def order_detail(order_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    o=db.get(Order,order_id)
    if not o or (o.user_id!=user.id and user.role!="ADMIN"): raise HTTPException(404,"Order not found")
    items=db.execute(select(OrderItem,Product.name).join(Product,Product.id==OrderItem.product_id).where(OrderItem.order_id==order_id)).all(); data={k:v for k,v in o.__dict__.items() if not k.startswith('_')}; data["items"]=[{**{k:v for k,v in x.__dict__.items() if not k.startswith('_')},"name":name} for x,name in items]; return data

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, or_, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Brand, Category, Product
from app.schemas.common import ProductWrite
from app.security import admin_user
from app.utils import product_json, slugify
router=APIRouter(prefix="/api",tags=["Catalog"])
@router.get("/categories")
def categories(db:Session=Depends(get_db)): return [{"id":x.id,"name":x.name,"slug":x.slug,"icon":x.icon or "💊","description":x.description or ""} for x in db.scalars(select(Category).order_by(Category.id)).all()]
@router.get("/brands")
def brands(db:Session=Depends(get_db)): return [{"id":x.id,"name":x.name,"slug":x.slug,"description":x.description or ""} for x in db.scalars(select(Brand).order_by(Brand.id)).all()]
def base_stmt(): return select(Product,Category.name,Category.slug,Brand.name,Brand.slug).outerjoin(Category,Category.id==Product.category_id).outerjoin(Brand,Brand.id==Product.brand_id)
@router.get("/products")
def products(search:str|None=None,category:str|None=None,brand:str|None=None,prescription:bool|None=None,sort:str|None=Query(None),db:Session=Depends(get_db)):
    q=base_stmt()
    if search: q=q.where(or_(Product.name.ilike(f"%{search}%"),Product.description.ilike(f"%{search}%")))
    if category: q=q.where(Category.slug==category)
    if brand: q=q.where(Brand.slug==brand)
    if prescription is True: q=q.where(Product.prescription_required.is_(True))
    order={"price-low":asc(Product.sale_price),"price-high":desc(Product.sale_price),"rating":desc(Product.rating)}.get(sort,desc(Product.id))
    return [product_json(r) for r in db.execute(q.order_by(order).limit(1000)).all()]
@router.get("/products/{product_id}")
def product(product_id:int,db:Session=Depends(get_db)):
    r=db.execute(base_stmt().where(Product.id==product_id)).first()
    if not r: raise HTTPException(404,"Product not found")
    return product_json(r)
@router.get("/products/{product_id}/related")
def related(product_id:int,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p:return []
    q=base_stmt().where(Product.id!=product_id,or_(Product.category_id==p.category_id,Product.brand_id==p.brand_id)).limit(8)
    return [product_json(r) for r in db.execute(q).all()]
@router.post("/products",status_code=201,dependencies=[Depends(admin_user)])
def create_product(body:ProductWrite,db:Session=Depends(get_db)):
    p=Product(**body.model_dump(),slug=slugify(body.name)); db.add(p); db.commit(); db.refresh(p); return p
@router.put("/products/{product_id}",dependencies=[Depends(admin_user)])
def update_product(product_id:int,body:ProductWrite,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p: raise HTTPException(404,"Product not found")
    for k,v in body.model_dump().items(): setattr(p,k,v)
    p.slug=slugify(body.name); db.commit(); db.refresh(p); return p
@router.delete("/products/{product_id}",status_code=204,dependencies=[Depends(admin_user)])
def delete_product(product_id:int,db:Session=Depends(get_db)): p=db.get(Product,product_id); p and db.delete(p); db.commit(); return Response(status_code=204)

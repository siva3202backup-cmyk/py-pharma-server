from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Cart,CartItem,Product,Review,User,Wishlist
from app.schemas.common import CartItemCreate,ProductIdRequest,QuantityUpdate,ReviewCreate
from app.security import current_user
router=APIRouter(prefix="/api",tags=["Customer Resources"])
@router.get("/users/profile")
def profile(user:User=Depends(current_user)): return {"id":user.id,"name":user.name,"email":user.email,"role":user.role}
def get_cart(db,user_id):
    cart=db.scalar(select(Cart).where(Cart.user_id==user_id))
    if not cart: cart=Cart(user_id=user_id); db.add(cart); db.commit(); db.refresh(cart)
    return cart
@router.get("/cart")
def cart(db:Session=Depends(get_db),user:User=Depends(current_user)):
    c=get_cart(db,user.id); rows=db.execute(select(CartItem,Product.name,Product.price,Product.sale_price).join(Product,Product.id==CartItem.product_id).where(CartItem.cart_id==c.id)).all()
    return [{**{k:v for k,v in x[0].__dict__.items() if not k.startswith('_')},"name":x.name,"price":x.price,"sale_price":x.sale_price} for x in rows]
@router.post("/cart/items",status_code=201)
def add_cart(body:CartItemCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    c=get_cart(db,user.id); item=CartItem(cart_id=c.id,**body.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.put("/cart/items/{item_id}")
def update_cart(item_id:int,body:QuantityUpdate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    item=db.scalar(select(CartItem).join(Cart).where(CartItem.id==item_id,Cart.user_id==user.id))
    if not item: raise HTTPException(404,"Cart item not found")
    item.quantity=body.quantity; db.commit(); db.refresh(item); return item
@router.delete("/cart/items/{item_id}",status_code=204)
def remove_cart(item_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    item=db.scalar(select(CartItem).join(Cart).where(CartItem.id==item_id,Cart.user_id==user.id))
    if item: db.delete(item); db.commit()
    return Response(status_code=204)
@router.get("/wishlist")
def wishlist(db:Session=Depends(get_db),user:User=Depends(current_user)): return db.scalars(select(Wishlist).where(Wishlist.user_id==user.id)).all()
@router.post("/wishlist",status_code=201)
def add_wishlist(body:ProductIdRequest,db:Session=Depends(get_db),user:User=Depends(current_user)):
    x=Wishlist(user_id=user.id,product_id=body.product_id); db.add(x)
    try: db.commit(); db.refresh(x); return x
    except IntegrityError: db.rollback(); return {}
@router.delete("/wishlist/{product_id}",status_code=204)
def remove_wishlist(product_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)): db.execute(delete(Wishlist).where(Wishlist.user_id==user.id,Wishlist.product_id==product_id)); db.commit(); return Response(status_code=204)
@router.get("/reviews/product/{product_id}")
def reviews(product_id:int,db:Session=Depends(get_db)):
    rows=db.execute(select(Review,User.name).outerjoin(User,User.id==Review.user_id).where(Review.product_id==product_id).order_by(Review.id.desc())).all(); return [{**{k:v for k,v in r.__dict__.items() if not k.startswith('_')},"name":name} for r,name in rows]
@router.post("/reviews",status_code=201)
def add_review(body:ReviewCreate,db:Session=Depends(get_db),user:User=Depends(current_user)): r=Review(**body.model_dump(),user_id=user.id,is_approved=True); db.add(r); db.commit(); db.refresh(r); return r

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ORMModel(BaseModel): model_config=ConfigDict(from_attributes=True)
class UserOut(ORMModel):
    id:int; name:str|None=None; email:EmailStr; role:str
class RegisterRequest(BaseModel):
    name:str|None=None; email:EmailStr; password:str=Field(min_length=6)
class LoginRequest(BaseModel): email:EmailStr; password:str
class AuthResponse(BaseModel): token:str; user:UserOut
class ProductWrite(BaseModel):
    name:str; sku:str|None=None; description:str|None=""; price:Decimal=Field(ge=0); sale_price:Decimal|None=Field(default=None,ge=0); stock:int=Field(default=0,ge=0); image_url:str|None=""; category_id:int; brand_id:int|None=None; is_featured:bool=False; prescription_required:bool=False
class CartItemCreate(BaseModel): product_id:int; quantity:int=Field(default=1,gt=0); unit_price:Decimal=Field(default=0,ge=0)
class QuantityUpdate(BaseModel): quantity:int=Field(gt=0)
class ProductIdRequest(BaseModel): product_id:int
class ReviewCreate(BaseModel): product_id:int; rating:int=Field(ge=1,le=5); title:str|None=None; review_text:str|None=None
class OrderItemIn(BaseModel): product_id:int; quantity:int=Field(default=1,gt=0); price:Decimal|None=Field(default=None,ge=0)
class OrderCreate(BaseModel): items:list[OrderItemIn]=Field(min_length=1); payment_method:str="Cash on Delivery"
class PaymentCreate(BaseModel): order_id:int; payment_gateway:str|None=None; payment_method:str|None=None; amount:Decimal=Field(ge=0)

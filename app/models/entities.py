from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    name: Mapped[str|None]=mapped_column(String(150))
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    password: Mapped[str|None]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(30), default="CUSTOMER")
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Category(Base):
    __tablename__="categories"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    name: Mapped[str|None]=mapped_column(String(200))
    slug: Mapped[str|None]=mapped_column(String(250), unique=True)
    icon: Mapped[str|None]=mapped_column(String(20))
    description: Mapped[str|None]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Brand(Base):
    __tablename__="brands"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    name: Mapped[str|None]=mapped_column(String(200))
    slug: Mapped[str|None]=mapped_column(String(250), unique=True)
    logo_url: Mapped[str|None]=mapped_column(Text)
    description: Mapped[str|None]=mapped_column(Text)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Product(Base):
    __tablename__="products"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    name: Mapped[str|None]=mapped_column(String(500))
    slug: Mapped[str|None]=mapped_column(String(500), unique=True)
    sku: Mapped[str|None]=mapped_column(String(100), unique=True)
    description: Mapped[str|None]=mapped_column(Text)
    price: Mapped[Decimal]=mapped_column(Numeric(12,2), default=0)
    sale_price: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    mrp: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    stock: Mapped[int]=mapped_column(Integer, default=0)
    image_url: Mapped[str|None]=mapped_column(Text)
    category_id: Mapped[int|None]=mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[int|None]=mapped_column(ForeignKey("brands.id"))
    rating: Mapped[Decimal|None]=mapped_column(Numeric(3,2), default=Decimal("4.4"))
    reviews: Mapped[int|None]=mapped_column(Integer, default=0)
    ingredients: Mapped[str|None]=mapped_column(Text)
    dosage: Mapped[str|None]=mapped_column(Text)
    warnings: Mapped[str|None]=mapped_column(Text)
    is_featured: Mapped[bool]=mapped_column(Boolean, default=False)
    prescription_required: Mapped[bool]=mapped_column(Boolean, default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Cart(Base):
    __tablename__="cart"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class CartItem(Base):
    __tablename__="cart_items"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    cart_id: Mapped[int]=mapped_column(ForeignKey("cart.id", ondelete="CASCADE"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]=mapped_column(Integer, default=1)
    unit_price: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Wishlist(Base):
    __tablename__="wishlists"; __table_args__=(UniqueConstraint("user_id","product_id"),)
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Review(Base):
    __tablename__="reviews"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    rating: Mapped[int]=mapped_column(Integer)
    title: Mapped[str|None]=mapped_column(String(200))
    review_text: Mapped[str|None]=mapped_column(Text)
    is_approved: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class Coupon(Base):
    __tablename__="coupons"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    code: Mapped[str|None]=mapped_column(String(80), unique=True)
    discount_type: Mapped[str|None]=mapped_column(String(30))
    discount_value: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    start_date: Mapped[date|None]=mapped_column(Date)
    end_date: Mapped[date|None]=mapped_column(Date)
    usage_limit: Mapped[int|None]=mapped_column(Integer)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)

class Order(Base):
    __tablename__="orders"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    order_number: Mapped[str|None]=mapped_column(String(50), unique=True)
    user_id: Mapped[int|None]=mapped_column(ForeignKey("users.id"))
    total: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    status: Mapped[str]=mapped_column(String(50), default="Processing")
    payment_status: Mapped[str]=mapped_column(String(50), default="Pending")
    payment_method: Mapped[str|None]=mapped_column(String(100))
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

class OrderItem(Base):
    __tablename__="order_items"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int]=mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]=mapped_column(Integer, default=1)
    price: Mapped[Decimal|None]=mapped_column(Numeric(12,2))

class Payment(Base):
    __tablename__="payments"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int|None]=mapped_column(ForeignKey("orders.id"))
    transaction_id: Mapped[str|None]=mapped_column(String(200))
    payment_gateway: Mapped[str|None]=mapped_column(String(100))
    payment_method: Mapped[str|None]=mapped_column(String(100))
    amount: Mapped[Decimal|None]=mapped_column(Numeric(12,2))
    payment_status: Mapped[str|None]=mapped_column(String(50))
    created_at: Mapped[datetime]=mapped_column(DateTime, server_default=func.now())

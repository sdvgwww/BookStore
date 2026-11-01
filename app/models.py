from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from app.database import Base

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(String)
    cover_path = Column(String(500))
    rating = Column(Numeric(3, 2), default=0)
    cost = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    publish_date = Column(Date, nullable=False)
    is_ebook = Column(Boolean, default=False)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    publisher_id = Column(Integer, ForeignKey("publishers.id"))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False) # guest, seller, manager, admin

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, nullable=False)
    delivery_date = Column(Date, nullable=False)
    customer_name = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False, default="новый")
    manager_id = Column(Integer, ForeignKey("users.id"))

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="RESTRICT"), nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
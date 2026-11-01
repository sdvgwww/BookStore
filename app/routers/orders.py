from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from pydantic import BaseModel
from datetime import date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Схема для обновления статуса
class StatusUpdate(BaseModel):
    status: str

# 1. Получение списка заказов
@router.get("/api/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    result = []
    for order in orders:
        # Собираем состав заказа (названия книг и количество)
        items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
        items_list = []
        for item in items:
            book = db.query(models.Book).filter(models.Book.id == item.book_id).first()
            items_list.append(f"{book.title} ({item.qty} шт.)")
            
        result.append({
            "id": order.id,
            "order_date": str(order.order_date),
            "delivery_date": str(order.delivery_date),
            "customer_name": order.customer_name,
            "status": order.status,
            "items": ", ".join(items_list) if items_list else "Нет товаров"
        })
    return result

# 2. Обновление статуса заказа
@router.put("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status_data: StatusUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    order.status = status_data.status
    db.commit()
    return {"message": "Статус обновлен"}
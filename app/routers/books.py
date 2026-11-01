from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from typing import Optional
import shutil
import os
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ПОЛУЧЕНИЕ СПИСКА КНИГ ---
@router.get("/api/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    result = []
    for book in books:
        genre_name = book.genre.name if book.genre_id else "Без жанра"
        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "cover_path": book.cover_path,
            "rating": float(book.rating),
            "cost": float(book.cost),
            "quantity": book.quantity,
            "publish_date": str(book.publish_date),
            "is_ebook": book.is_ebook,
            "genre": genre_name,
            "genre_id": book.genre_id
        })
    return result

# --- ПОЛУЧЕНИЕ СПИСКА ЖАНРОВ (для выпадающего списка) ---
@router.get("/api/genres")
def get_genres(db: Session = Depends(get_db)):
    genres = db.query(models.Genre).all()
    return [{"id": g.id, "name": g.name} for g in genres]

# --- ДОБАВЛЕНИЕ КНИГИ ---
@router.post("/api/books")
async def create_book(
    title: str = Form(...),
    description: str = Form(None),
    cost: float = Form(...),
    quantity: int = Form(...),
    publish_date: str = Form(...),
    is_ebook: bool = Form(False),
    genre_id: int = Form(...),
    cover: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Валидация из ТЗ
    if cost < 0 or quantity < 0:
        raise HTTPException(status_code=400, detail="Цена и количество не могут быть отрицательными")

    cover_path = None
    if cover and cover.filename:
        # Проверка размера (2 МБ)
        file_content = await cover.read()
        if len(file_content) > 2 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Файл больше 2 МБ")
        
        # Сохраняем файл с уникальным именем в static/covers
        ext = os.path.splitext(cover.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join("static", "covers", filename)
        
        with open(filepath, "wb") as buffer:
            buffer.write(file_content)
            
        cover_path = f"/static/covers/{filename}"

    new_book = models.Book(
        title=title, description=description, cost=cost,
        quantity=quantity, publish_date=publish_date,
        is_ebook=is_ebook, genre_id=genre_id, cover_path=cover_path
    )
    db.add(new_book)
    db.commit()
    return {"message": "Книга добавлена"}

# --- УДАЛЕНИЕ КНИГИ ---
@router.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # ПРОВЕРКА ИЗ ТЗ: Нельзя удалить книгу, если она есть в заказах
    order_item = db.query(models.OrderItem).filter(models.OrderItem.book_id == book_id).first()
    if order_item:
        raise HTTPException(status_code=400, detail="Нельзя удалить книгу, которая есть в заказах!")
    
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
        
    db.delete(book)
    db.commit()
    return {"message": "Книга удалена"}
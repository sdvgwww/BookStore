from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Отображение страницы входа (GET)
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 2. Обработка формы входа (POST)
@router.post("/login")
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    # Ищем пользователя в БД
    user = db.query(models.User).filter(models.User.login == user_data.login).first()
    
    # В реальности здесь должна быть проверка хеша пароля. 
    # Для теста мы предполагаем, что пароль верный, если пользователь найден.
    if not user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
        
    # В реальном приложении здесь нужно создавать сессию или JWT-токен.
    # Пока просто вернем данные пользователя.
    return {"message": "Успешный вход", "user": {"full_name": user.full_name, "role": user.role}}
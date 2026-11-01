from fastapi import FastAPI
from app.database import engine, Base
import app.models
from app.routers import auth  # <-- Импортируем наш роутер

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подключаем роутер авторизации
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "BookStore работает"}
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/catalog", response_class=HTMLResponse)
def catalog_page(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})
from fastapi import FastAPI
from app.database import engine, Base
import app.models
from app.routers import auth, books  # <-- Добавили books

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router) # <-- Подключили API книг

@app.get("/")
def read_root():
    return {"message": "BookStore работает"}
from app.routers import auth, books, orders  # <-- Добавили orders

# ... (создание app)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(orders.router) # <-- Подключили роутер заказов

# ...
# Не забудьте, что у вас должна быть функция отдачи страницы /catalog
# Добавьте такую же для /orders
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})
    @app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
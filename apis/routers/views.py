from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# login画面への遷移
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# signup画面への遷移
@router.get("/signup", response_class=HTMLResponse)
async def read_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# main画面への遷移
@router.get("/index", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 予定追加画面への遷移
@router.get("/itinerary_create", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("itinerary_create.html", {"request": request})

# 予定変更画面への遷移
@router.get("/itinerary_edit", response_class=HTMLResponse)
async def read_signup(request: Request):
    return templates.TemplateResponse("itinerary_edit.html", {"request": request})

# ユーザー情報変更画面への遷移
@router.get("/user_info_edit", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("user_info_edit.html", {"request": request})

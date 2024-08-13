from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# ログイン画面への遷移
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# サインアップ画面への遷移
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# メイン画面への遷移
@router.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 予定追加画面への遷移
@router.get("/itinerary_create", response_class=HTMLResponse)
async def itinerary_create(request: Request):
    return templates.TemplateResponse("itinerary_create.html", {"request": request})

# 予定変更画面への遷移
@router.get("/itinerary_edit", response_class=HTMLResponse)
async def itinerary_edit(request: Request):
    return templates.TemplateResponse("itinerary_edit.html", {"request": request})

# ユーザー情報変更画面への遷移
@router.get("/user_edit", response_class=HTMLResponse)
async def user_info_edit(request: Request):
    return templates.TemplateResponse("user_info_edit.html", {"request": request})

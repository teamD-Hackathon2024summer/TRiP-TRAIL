from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import get_schedules
from security import get_current_user

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

# # メイン画面への遷移 使わない
# @router.get("/index", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# メイン画面への遷移
@router.get("/index", response_class=HTMLResponse)
async def view_schedules(request: Request, user=Depends(get_current_user)):
    try:
        user_id = user["user_id"]

        # 予定一覧を取得
        schedules = get_schedules(user_id)

        # `schedules` 変数をテンプレートに渡す
        return templates.TemplateResponse("index.html", {"request": request, "schedules": schedules})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 予定追加画面への遷移
@router.get("/itinerary_create", response_class=HTMLResponse)
async def itinerary_create(request: Request):
    return templates.TemplateResponse("itinerary_create.html", {"request": request})

# 予定変更画面への遷移
@router.get("/itinerary_edit/{schedule_id}", response_class=HTMLResponse)
async def itinerary_edit(request: Request, schedule_id: int, user=Depends(get_current_user)):
    try:
        user_id = user["user_id"]

        # 予定一覧を取得
        schedules = get_schedules(user_id)

        # `schedule_id` に一致するスケジュールを検索
        schedule = next((s for s in schedules if s["schedule_id"] == schedule_id), None)

        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")

        # `schedule` 変数をテンプレートに渡す
        return templates.TemplateResponse("itinerary_edit.html", {"request": request, "schedule": schedule})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ユーザ情報変更画面への遷移
@router.get("/user_edit", response_class=HTMLResponse)
async def user_info_edit(request: Request, user=Depends(get_current_user)):
    try:
        # `user` 変数をテンプレートに渡す
        return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load user information: {str(e)}")
    
# エラー画面への遷移
@router.get("/error", response_class=HTMLResponse)
async def error(request: Request, error: str):
    return templates.TemplateResponse("error.html", {"request": request, "error": error})

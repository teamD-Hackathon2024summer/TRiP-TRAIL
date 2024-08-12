# routers/routes.py
from fastapi import APIRouter, HTTPException, Depends, Form
from schemas import RouteRequest, UserCreate, UserEdit, LoginForm, ScheduleCreate, ScheduleEdit
from models import create_user, update_user, create_schedule,get_user_by_username, get_user_by_email, update_schedule, get_schedules
from users import  authenticate_user
from security import hash_password, create_access_token,get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
import googlemaps
import os

router = APIRouter()

gmaps = googlemaps.Client(key=os.getenv("GMAPS_API_KEY"))

# ユーザー登録のエンドポイント
@router.post("/signup", summary="ユーザー登録", description="ユーザーを登録します")
async def signup(
    request: UserCreate = Depends()
    ):
    try:
        # ユーザー名の重複チェック
        if get_user_by_username(request.user_name):
            raise HTTPException(status_code=400, detail="Username already registered")

        # メールアドレスの重複チェック
        if get_user_by_email(request.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # パスワードをハッシュ化
        hashed_password = hash_password(request.password1)

        # 受け取ったデータを使って新規ユーザーを作成
        create_user(request.user_name, request.email, hashed_password, request.user_address)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ログインのエンドポイント
@router.post("/login", summary="ログイン", description="ログインしてトークンを取得")
async def login(form_data: LoginForm):
    user = authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_id"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ログアウトのエンドポイント

# ユーザー情報変更のエンドポイント
@router.patch("/users/{user_id}", summary="ユーザー情報変更", description="ユーザー情報を変更します")
async def edit_user(
    request: UserEdit = Depends(),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["user_id"]

        # ユーザー名の重複チェック
        if request.user_name and request.user_name != current_user['user_name']:
            existing_user = get_user_by_username(request.user_name)
            if existing_user and existing_user["user_id"] != user_id:
                raise HTTPException(status_code=400, detail="Username already registered")

        # メールアドレスの重複チェック
        if request.email and request.email != current_user['email']:
            existing_user = get_user_by_email(request.email)
            if existing_user and existing_user["user_id"] != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # パスワードのハッシュ化
        if request.password1:
            hashed_password = hash_password(request.password1)
        else:
            # パスワードが変更されない場合、現在のパスワードをそのまま使用
            hashed_password = current_user["password"]
        
        update_user(user_id, request.user_name, request.email, hashed_password, request.user_address)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 予定一覧の取得のエンドポイント
@router.get("/users/{user_id}/schedules", summary="予定一覧取得", description="予定一覧を取得します")
async def get_user_schedules(
    user_id: int,  # パスパラメータとして user_id を受け取る
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["user_id"]

        # 予定一覧を取得
        schedules = get_schedules(user_id)
        
        if not schedules:
            return {"message": "No schedules found for this user"}

        return {"schedules": schedules}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# 予定追加のエンドポイント
@router.post("/schedules", summary="予定の追加", description="予定を追加します")
async def add_schedule(
    request: ScheduleCreate = Depends(),
    current_user: dict = Depends(get_current_user)
):
    try:  
        user_id = current_user["user_id"]
        create_schedule(user_id, request.date, request.destination, request.destination_address)
        return {"message": "Schedule created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 予定変更のエンドポイント
@router.patch("/schedules/{schedule_id}", summary="予定の変更", description="予定を変更します")
async def edit_schedule(
    schedule_id: int,
    request: ScheduleEdit = Depends(),
    current_user: dict = Depends(get_current_user)
):
    try:  
        user_id = current_user["user_id"]

        # スケジュールがこのユーザーに属しているかを確認
        schedules = get_schedules(user_id)
        if not any(schedule["schedule_id"] == schedule_id for schedule in schedules):
            raise HTTPException(status_code=404, detail="Schedule not found or does not belong to the user")
        
        update_schedule(schedule_id, request.date, request.destination, request.destination_address)
        return {"message": "Schedule updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@router.post("/route")
async def get_route(request: RouteRequest):
    try:
        directions = gmaps.directions(request.origin, request.destination)
        return directions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

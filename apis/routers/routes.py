# routers/routes.py
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Optional
from schemas import  UserCreate, UserEdit, LoginForm, ScheduleCreate, ScheduleEdit
from models import create_user, update_user, create_schedule, update_schedule, get_schedules, delete_schedule, get_user_address, get_destination_address
from users import get_user_by_username, get_user_by_email
from security import hash_password, authenticate_user, create_access_token,get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, date as dt_date
import googlemaps
import os
import requests

router = APIRouter()
GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
gmaps = googlemaps.Client(key=GMAPS_API_KEY)
templates = Jinja2Templates(directory="templates")

""" テスト用 ユーザーの情報を取得するエンドポイント """
@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user

""" ユーザー登録のエンドポイント """

# フォームデータを取得して UserCreate に渡す関数
def get_signup_form_data(
    user_name: str = Form(...),
    email: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    user_address: str = Form(...)
) -> UserCreate:
    form_data = {
        "user_name": user_name,
        "email": email,
        "password1": password1,
        "password2": password2,
        "user_address": user_address
    }
    return UserCreate(**form_data)

@router.post("/signup", summary="ユーザー登録", description="ユーザーを登録します")
async def signup(
    user_data: UserCreate = Depends(get_signup_form_data)
):
    try:
        # ユーザー名の重複チェック
        if get_user_by_username(user_data.user_name):
            raise HTTPException(status_code=400, detail="Username already registered")

        # メールアドレスの重複チェック
        if get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # パスワードをハッシュ化
        hashed_password = hash_password(user_data.password1)

        # 受け取ったデータを使って新規ユーザーを作成
        create_user(user_data.user_name, user_data.email, hashed_password, user_data.user_address)

        # ユーザー作成成功後に /login へリダイレクト
        return RedirectResponse(url="/login", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

""" ログインのエンドポイント """

# フォームデータを取得してLoginFormへ渡す
def get_login_form_data(
    email: str = Form(...),
    password: str = Form(...)
) -> LoginForm:
    form_data = {
        "email": email,
        "password": password,
    }
    return LoginForm(**form_data)

@router.post("/login", summary="ログイン", description="ログインしてトークンを取得")
async def login(
    form_data: LoginForm = Depends(get_login_form_data)
    ):
    user = authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # sub（subject）フィールドにuser_idを格納
    access_token = create_access_token(
       data={"sub": str(user["user_id"])}, expires_delta=access_token_expires
    )
     # クライアントにトークンを含むクッキーを設定する
    response = RedirectResponse(url="/index", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    
    return response

""" ログアウトのエンドポイント """

@router.post("/logout", summary="ログアウト", description="ログアウトしてトークンを削除します")
async def logout(response: Response):
    # クライアントのクッキーからトークンを削除
    response.delete_cookie(key="access_token", path="/", domain=None)

    # ログアウト後にログイン画面にリダイレクト
    return RedirectResponse(url="login", status_code=303)

""" ユーザー情報変更のエンドポイント """

# フォームデータを取得してUserEditへ渡す

def get_edituser_form_data(
    user_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password1: Optional[str] = Form(None),
    password2: Optional[str] = Form(None),
    user_address: Optional[str] = Form(None),
) -> UserEdit:
    form_data = {
        "user_name": user_name,
        "email": email,
        "password1": password1,
        "password2": password2,
        "user_address": user_address
    }
    return UserEdit(**form_data)

@router.post("/users", summary="ユーザー情報変更", description="ユーザー情報を変更します")
async def edit_user(
    user_data: UserEdit = Depends(get_edituser_form_data),
    current_user: dict = Depends(get_current_user)
):
    # 入力がないフィールドは現在の値を使用し、パスワードが変更された場合のみハッシュ化
    updated_data = {
        "user_name": user_data.user_name or current_user["user_name"],
        "email": user_data.email or current_user["email"],
        "password": hash_password(user_data.password1) if user_data.password1 else current_user["password"],
        "user_address": user_data.user_address or current_user["user_address"]
    }

    # ユーザー名の重複チェック
    if updated_data["user_name"] != current_user['user_name']:
        existing_user = get_user_by_username(updated_data["user_name"])
        if existing_user and existing_user["user_id"] != current_user["user_id"]:
            raise HTTPException(status_code=400, detail="Username already registered")

    # メールアドレスの重複チェック
    if updated_data["email"] != current_user['email']:
        existing_user = get_user_by_email(updated_data["email"])
        if existing_user and existing_user["user_id"] != current_user["user_id"]:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # ユーザー情報を更新
    try:
        update_user(
            current_user["user_id"],
            updated_data["user_name"],
            updated_data["email"],
            updated_data["password"],
            updated_data["user_address"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user information: {str(e)}")
    
    # ユーザー情報変更後に /index へリダイレクト
    return RedirectResponse(url="/index", status_code=303)


""" 予定一覧の取得のエンドポイント """

@router.get("/users/{user_id}/schedules", summary="予定一覧取得", description="予定一覧を取得します")
async def get_user_schedules(
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
    
"""  予定追加のエンドポイント """

# フォームデータを取得してScheduleCreateへ渡す
def get_schedule_form_data(
    date: dt_date = Form(...),
    destination: str = Form(...),
    destination_address: str = Form(...),
) -> ScheduleCreate:
    form_data = {
        "date": date,
        "destination": destination,
        "destination_address": destination_address,
    }
    return ScheduleCreate(**form_data)

@router.post("/schedules", summary="予定の追加", description="予定を追加します")
async def add_schedule(
    schedule_data: ScheduleCreate = Depends(get_schedule_form_data),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["user_id"]
        create_schedule(user_id, schedule_data.date, schedule_data.destination, schedule_data.destination_address)

        # スケジュール追加後に /index へリダイレクト
        return RedirectResponse(url="/index", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

""" 予定変更のエンドポイント """

# フォームデータを取得してScheduleEditへ渡す
def get_editschedule_form_data(
    date: Optional[dt_date] = Form(None),
    destination: Optional[str] = Form(None),
    destination_address: Optional[str] = Form(None),
) -> ScheduleEdit:
    form_data = {
        "date": date,
        "destination": destination,
        "destination_address": destination_address,
    }
    return ScheduleEdit(**form_data)

@router.post("/schedules/{schedule_id}", summary="予定の変更", description="予定を変更します")
async def edit_schedule(
    schedule_id: int,
    schedule_data: ScheduleEdit = Depends(get_editschedule_form_data),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = current_user["user_id"]

        # スケジュールがこのユーザーに属しているかを確認
        schedules = get_schedules(user_id)
        if not any(schedule["schedule_id"] == schedule_id for schedule in schedules):
            raise HTTPException(status_code=404, detail="Schedule not found or does not belong to the user")

        # 既存のスケジュールを取得
        existing_schedule = next(schedule for schedule in schedules if schedule["schedule_id"] == schedule_id)

        # 入力がないフィールドは既存の値を使用
        updated_data = {
            "date": schedule_data.date or existing_schedule["date"],
            "destination": schedule_data.destination or existing_schedule["destination"],
            "destination_address": schedule_data.destination_address or existing_schedule["destination_address"]
        }

        # スケジュール情報を更新
        update_schedule(
            schedule_id,
            updated_data["date"],
            updated_data["destination"],
            updated_data["destination_address"]
        )

        # スケジュール変更後に /index へリダイレクト
        return RedirectResponse(url="/index", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

""" 予定削除のエンドポイント """

@router.delete("/schedules/{schedule_id}", summary="予定の削除", description="予定を削除します")
async def del_schedule(
    schedule_id: int,
    current_user: dict = Depends(get_current_user)
):
    try:  
        user_id = current_user["user_id"]

        # スケジュールがこのユーザーに属しているかを確認
        schedules = get_schedules(user_id)
        if not any(schedule["schedule_id"] == schedule_id for schedule in schedules):
            raise HTTPException(status_code=404, detail="Schedule not found or does not belong to the user")
        
        # スケジュールの削除
        delete_schedule(schedule_id)

        # 削除成功メッセージを返す
        return {"message": "Schedule deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_coordinate(address):
    try:
        geocode = gmaps.geocode(address=address, region="JP")
        result = googlemaps.convert.latlng(geocode[0]["geometry"]["location"])
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/map/{schedule_id}", summary="mapページ", description="mapページを表示します")
def route(schedule_id: int):
    try:
        # ユーザー認証をして、user_idを取得する処理に差し替え予定
        user_id = 1

        # データベースからそれぞれの住所を取得
        origin = get_user_address(user_id)[0]['user_address']
        destination = get_destination_address(schedule_id)[0]['destination_address']
        # 住所から緯度経度情報を取得
        origin_coodinate = get_coordinate(origin)
        destination_coodinate = get_coordinate(destination)

        # ルート計算リクエスト
        try:
            route_data = gmaps.directions(origin_coodinate, destination_coodinate, language="ja", region="JP")[0]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            # エラー時の処理要検討 "HTTPSConnectionPool" これは通信エラーの場合

        # レスポンスデータ作成
        time = route_data["legs"][0]["duration"]["text"]
        copyrights = route_data["copyrights"]
        polyline = repr(route_data["overview_polyline"]["points"])[1:-1]
        proxy_url = os.getenv("GMAPS_PROXY_URL")
        request = {"time": time, "polyline": polyline, "proxy_url": proxy_url, "copyrights": copyrights}

        return templates.TemplateResponse(name="map.html", request=request)
    except Exception as e:
        return templates.TemplateResponse(name="error.html", request={"error": e})


@router.get("/maps-proxy", summary="APIキー付加用プロキシ", description="リクエストにAPIキーを追加して代理リクエストします")
def maps_api_proxy(libraries: str, v: str, callback: str):
# フロントエンドからリクエストパラメータを受け取りAPIキーを追加してリクエストを送信、レスポンスはスクリプトデータ
    params = {"libraries": libraries, "v": v, "callback": callback}
    params["key"] = GMAPS_API_KEY

    response = requests.get('https://maps.googleapis.com/maps/api/js', params=params)

    return Response(content=response.content, media_type="application/javascript")
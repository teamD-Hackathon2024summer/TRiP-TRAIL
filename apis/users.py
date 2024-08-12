# データベースからのユーザー情報の取得

from fastapi import HTTPException
from database import DatabaseHandler
from security import verify_password
import logging

# ユーザーを取得する汎用関数
def get_user(query: str, params: tuple):
    with DatabaseHandler() as db:
        result = db.get_data(query=query, params=params)
        logging.debug(f"Database query result: {result}")  # クエリ結果をログに出力

        if not result or len(result) == 0:
            logging.error("User not found in the database.")
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = result[0]
        logging.debug(f"User data structure: {user_data}")  # user_dataの内容を確認

        if isinstance(user_data, dict):
            return user_data
        elif isinstance(user_data, tuple):
            if len(user_data) < 5:
                logging.error("Unexpected database result format.")
                raise HTTPException(status_code=500, detail="Unexpected database result format")
            return {
                "user_id": user_data[0],
                "user_name": user_data[1],
                "email": user_data[2],
                "password": user_data[3],
                "user_address": user_data[4]
            }
        else:
            logging.error("Unexpected result type from database.")
            raise HTTPException(status_code=500, detail="Unexpected result type from database")


# user_id でユーザーを取得する関数を追加
def get_user_by_id(user_id: str):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE user_id = %s'
    params = (user_id,)
    return get_user(query, params)

# メールアドレスでユーザーを取得する関数
def get_user_by_email(email: str):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE email = %s'
    params = (email,)
    return get_user(query, params)

# ユーザー認証を行う関数
def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        logging.debug("User not found or password incorrect.")  # ユーザーが見つからないか、パスワードが間違っている場合のログ
        return None
    if not verify_password(password, user["password"]):
        logging.debug("Password verification failed.")  # パスワード検証失敗のログ
        return None
    logging.debug("User authenticated successfully.")  # ユーザー認証成功のログ
    return user
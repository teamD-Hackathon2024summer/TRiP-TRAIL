# データベースからのユーザー情報の取得

from database import DatabaseHandler

# ユーザーをでユーザー名で検索する関数
def get_user_by_username(user_name):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE user_name = %s'
    params = (user_name,)
    with DatabaseHandler() as db:
        return db.get_data(query = query, params = params)

# ユーザーをメールアドレスで検索する関数
def get_user_by_email(email):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE email = %s'
    params = (email,)
    with DatabaseHandler() as db:
        result = db.get_data(query=query, params=params)
        if result:
            return result[0]  # 結果が存在する場合、最初のユーザーを返す
        return None

# ユーザーIDでユーザー情報を取得する関数
def get_user_by_id(user_id):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE user_id = %s'
    params = (user_id,)
    with DatabaseHandler() as db:
        result = db.get_data(query=query, params=params)
        if result:
            return result[0]
        return None


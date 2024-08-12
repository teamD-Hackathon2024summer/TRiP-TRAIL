from database import DatabaseHandler

# 受け取る引数、query、params、操作関数の使い分けで各関数を作り分けている
def create_user(user_name, email, password, user_address):
    query = 'INSERT INTO users (user_name, email, password, user_address) VALUES (%s, %s, %s, %s)'
    params = (user_name, email, password, user_address)
    with DatabaseHandler() as db:
        db.update_database(query = query, params = params)

def create_schedule(user_id, date, destination, destination_address):
    query = 'INSERT INTO schedules (user_id, date, destination, destination_address) VALUES (%s, %s, %s, %s)'
    params = (user_id, date, destination, destination_address)
    with DatabaseHandler() as db:
        db.update_database(query = query, params = params)

def delete_schedule(schedule_id):
    query = 'DELETE FROM schedules WHERE schedule_id = %s'
    params = (schedule_id,)
    with DatabaseHandler() as db:
        db.update_database(query = query, params = params)

def update_schedule(schedule_id, date, destination, destination_address):
    query = 'UPDATE schedules SET date = %s, destination = %s, destination_address = %s WHERE schedule_id = %s'
    params = (date, destination, destination_address, schedule_id)
    with DatabaseHandler() as db:
        db.update_database(query = query, params = params)

def update_user(user_id, user_name, email, password, user_address):
    query = 'UPDATE users SET user_name = %s, email = %s, password = %s, user_address = %s WHERE user_id = %s'
    params = (user_name, email, password, user_address, user_id)
    with DatabaseHandler() as db:
        db.update_database(query = query, params = params)

def get_user_address(user_id):
    query = 'SELECT user_address FROM users WHERE user_id = %s'
    params = (user_id,)
    with DatabaseHandler() as db:
        return db.get_data(query = query, params = params)

def get_schedules(user_id):
    query = 'SELECT schedule_id, date, destination FROM schedules WHERE user_id = %s'
    params = (user_id,)
    with DatabaseHandler() as db:
        return db.get_data(query = query, params = params)
    
# ユーザー名でユーザーを取得する関数
def get_user_by_username(user_name: str):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE user_name = %s'
    params = (user_name,)
    with DatabaseHandler() as db:
        return db.get_data(query = query, params = params)

# メールアドレスでユーザーを取得する関数
def get_user_by_email(email: str):
    query = 'SELECT user_id, user_name, email, password, user_address FROM users WHERE email = %s'
    params = (email,)
    with DatabaseHandler() as db:
        return db.get_data(query = query, params = params)
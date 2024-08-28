import pymysql.cursors
import os

# withを使ってインスタンス化すると自動実行される__の３つのメソッドで接続関連を制御、通常のメソッドの実行でデータの取得や操作を行う
class DatabaseHandler:
    def __init__(self):
        self.host = "mysql_fast"
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DB_FAST")
        self.charset = 'utf8mb4'
        self.connection =  None
    
    def __enter__(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor
            )
            return self
        except Exception as e:
            print(f'Error: {e}, 接続エラーです')
            raise e
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        if exc_type:
            print(f'Exception type: {exc_type}, Exception value: {exc_value}, Traceback: {traceback}')
        return False
    
    def get_data(self, query, params = None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f'{e} により失敗')
    
    def update_database(self, query, params = None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except Exception as e:
            print(f'{e} により失敗')
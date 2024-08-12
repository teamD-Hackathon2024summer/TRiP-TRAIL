class Signup:
    endpoint = "/signup"
    summary = "ユーザー登録"
    description = """ユーザーを登録します"""

class Login:
    endpoint = "/login"
    summary = "ログイン"
    description = """ログイン"""

class Signout:
    endpoint = "/logout"
    summary = "ログアウト"
    description = """ログアウト"""

class EditUser:
    endpoint = "/users"
    summary = "ユーザー情報変更"
    description = """ユーザー情報を変更します"""

class GetSchedules:
    endpoint = "/users/{user_id}/schedules"
    summary = "予定一覧取得"
    description = """予定一覧を取得します"""

class AddSchedule:
    endpoint = "/schedules"
    summary = "予定の追加"
    description = """予定を追加します"""

class EditSchedule:
    endpoint = "/schedules"
    summary = "予定の変更"
    description = """予定を変更します"""

class DelSchedule:
    endpoint = "/schedules"
    summary = "予定の削除"
    description = """予定を削除します"""
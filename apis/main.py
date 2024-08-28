from fastapi import FastAPI, Request, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from routers.routes import router as routes_router
from routers.views import router as views_router
from pymysql import MySQLError

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ルーターをインクルード
app.include_router(routes_router)
app.include_router(views_router)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
def exception_handler_http(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login")
    body = {"messages": [str(exc)]}
    return templates.TemplateResponse(name="error.html", request=body)

@app.exception_handler(RequestValidationError)
def exception_handler_request_validation_error(request: Request, exc: RequestValidationError):
    body = {"messages": []}
    for error in exc.errors():
        loc = error["loc"][1]
        msg = error["msg"]
        body["messages"].append(f"{loc} {msg}")
    return templates.TemplateResponse(name="error.html", request=body)

@app.exception_handler(MySQLError)
def exception_handler_mysql_error(request: Request, exc: MySQLError):
    body = {"messages": ["データベース接続エラーです"]}
    return templates.TemplateResponse(name="error.html", request=body)

@app.exception_handler(ValueError)
def exception_handler_value_error(request: Request, exc: ValueError):
    body = {"messages": ["間違った値を入力していませんか？"]}
    return templates.TemplateResponse(name="error.html", request=body)
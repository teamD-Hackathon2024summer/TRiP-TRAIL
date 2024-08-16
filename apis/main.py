from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.routes import router as routes_router
from routers.views import router as views_router

app = FastAPI()

# ルーターをインクルード
app.include_router(routes_router)
app.include_router(views_router)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

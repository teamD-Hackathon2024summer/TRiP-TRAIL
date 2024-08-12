from fastapi import FastAPI
from routers.routes import router as routes_router
from routers.views import router as views_router

app = FastAPI()

# ルーターをインクルード
app.include_router(routes_router)
app.include_router(views_router)

# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

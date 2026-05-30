from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat, chat_history

app = FastAPI(title="Swaddle Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(chat_history.router)


@app.get("/health")
async def health():
    return {"status": "ok"}

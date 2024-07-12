from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import news
import news.route

app = FastAPI()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"]
)


app.include_router(news.route.router)

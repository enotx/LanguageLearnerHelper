# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    PROJECT_NAME: str = "C3PO Linguist"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js开发服务器
        "http://localhost:8000",
        "https://enotx.com",  # 生产环境域名
    ]
    
    # AI服务配置
    AI_API_URL: str = os.getenv("AI_API_URL", "")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")

settings = Settings()

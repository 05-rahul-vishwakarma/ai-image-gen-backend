from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
from app.core.config import settings
from app.core.database import init_db, close_db
from app.routers import router

# load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI Image Generator API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    await init_db()
    print(f"\n🚀 Server running at http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs available at http://{settings.HOST}:{settings.PORT}/docs\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    await close_db()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

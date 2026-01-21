from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# from dotenv import load_dotenv
from app.core.config import settings
from app.core.database import init_db, close_db
from app.routers import router
from app.schemas.response import error_response

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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPException and return wrapped error response"""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail)
    )


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
    return {
        "success": True,
        "message": "Service is healthy",
        "data": {"status": "healthy"}
    }

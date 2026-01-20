from fastapi import APIRouter

from app.routers import auth, generation, user

router = APIRouter()


router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(generation.router, prefix="/generations", tags=["Generations"])
router.include_router(user.router, prefix="/user", tags=["User"])

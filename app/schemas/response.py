from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel


DataT = TypeVar('DataT')


class ApiResponse(BaseModel, Generic[DataT]):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[DataT] = None


def success_response(message: str, data=None):
    """Helper to create success response"""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str):
    """Helper to create error response"""
    return {
        "success": False,
        "message": message,
        "data": None
    }

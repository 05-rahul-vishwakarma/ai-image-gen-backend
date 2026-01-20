from typing import TypeVar, Generic, Optional
from pydantic import BaseModel


DataT = TypeVar('DataT')


class ApiResponse(BaseModel, Generic[DataT]):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[DataT] = None

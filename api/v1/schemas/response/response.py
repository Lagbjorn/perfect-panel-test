from enum import Enum
from typing import Union

from pydantic import BaseModel

from .data import PostData, ProfileData, ProfilePostsData


class Status(str, Enum):
    SUCCESS = 'success'
    ERROR = 'error'


class BasicResponse(BaseModel):
    status: Status
    code: int


class ErrorResponse(BasicResponse):
    message: str


class Response(BasicResponse):
    data: Union[ProfileData, PostData, ProfilePostsData]

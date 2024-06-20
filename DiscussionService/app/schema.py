from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    name: str


class CommentCreate(BaseModel):
    text: str


class ReplieCreate(BaseModel):
    text: str


class RepliesDTO(BaseModel):
    id: int
    text: str
    created_on: Optional[datetime]
    user_id: int
    user: UserDTO
    comment_id: int

class CommentLikeDTO(BaseModel):
    id: int
    user_id:int
    user:str

class LikeDTO(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_on: Optional[datetime]
    user: UserDTO


class CommentDTO(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str
    created_on: Optional[datetime]
    likes: List[CommentLikeDTO]
    total_likes: int
    replies: Optional[List[RepliesDTO]]
    user: UserDTO


class PostResponse(BaseModel):
    id: int
    text: str
    image_url: Optional[str]
    hashtags: List[str]
    created_on: datetime
    view_count: int
    user_id: int
    user: UserDTO
    comments: List[CommentDTO]
    likes: List[LikeDTO]
    total_likes: int

    class Config:
        orm_mode = True

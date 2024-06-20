from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str = None
    mobile_no: str = None
    email: EmailStr = None


class UserDTO(BaseModel):
    id: int
    name: str
    mobile_no: str
    email: EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class FollowBase(BaseModel):
    follower_id: int
    followed_id: int


class FollowDTO(FollowBase):
    follower: UserDTO

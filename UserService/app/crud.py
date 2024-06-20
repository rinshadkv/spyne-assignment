from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .auth import get_password_hash
from .models import Follow, User
from .schema import *
from .schema import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_mobile(db: Session, mobile_no: str):
    return db.query(User).filter(User.mobile_no == mobile_no).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_users(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    ex_user = get_user_by_mobile(db, mobile_no=user.mobile_no)
    if ex_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    db_user = User(name=user.name, mobile_no=user.mobile_no, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_users(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.mobile_no = user.mobile_no
        db_user.email = user.email
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    if search:
        return db.query(User).filter(User.name.ilike(f'%{search}%')).all()
    return db.query(User).offset(skip).limit(limit).all()


def follow_user(db: Session, follower_id: int, followed_id: int):
    if follower_id == followed_id:
        raise ValueError("User cannot follow themselves")
    follow = Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow


def unfollow_user(db: Session, follower_id: int, followed_id: int):
    follow = db.query(Follow).filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow


def get_followers(db: Session, user_id: int):
    followers = db.query(User).join(Follow, Follow.follower_id == User.id).filter(Follow.followed_id == user_id).all()
    return [UserDTO(
        id=user.id,
        name=user.name,
        mobile_no=user.mobile_no,
        email=user.email
    ) for user in followers]


def get_following(db: Session, user_id: int):
    following = db.query(User).join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return [UserDTO(
        id=user.id,
        name=user.name,
        mobile_no=user.mobile_no,
        email=user.email
    ) for user in following]

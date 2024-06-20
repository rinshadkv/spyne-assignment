from typing import Annotated, Optional

from fastapi import HTTPException, Depends, FastAPI, Query
from sqlalchemy.orm import Session

from .auth import authenticate_user, create_access_token, get_current_user
from .crud import *
from .database import SessionLocal, engine
from .models import *
from .schema import *

app = FastAPI()

# Create all database tables
User.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_users(db, user)


@app.post("/users/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": authenticated_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, search: Optional[str] = Query(None),
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_users(db, skip=skip, limit=limit,search=search)


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, current_user: Annotated[User, Depends(get_current_user)],
                db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return update_users(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}")
def delete_users(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return delete_user(db=db, user_id=user_id)


@app.get("/users/{user_id}", response_model=UserDTO)
def read_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/follow")
def follow_users(follow: FollowBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return follow_user(db=db, follower_id=follow.follower_id, followed_id=follow.followed_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/users/unfollow")
def unfollow_users(follow: FollowBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return unfollow_user(db=db, follower_id=follow.follower_id, followed_id=follow.followed_id)


@app.get("/users/{user_id}/followers")
def get_followers_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_followers(db=db, user_id=user_id)


@app.get("/users/{user_id}/following")
def get_following_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_following(db=db, user_id=user_id)


@app.get("/user/get_current_user")
def get_current_user_details(current_user: User = Depends(get_current_user)):
    return current_user

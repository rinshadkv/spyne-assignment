from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status, Query, APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .crud import *
from .database import SessionLocal, engine
from .schema import *
from .utils import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

Post.metadata.create_all(bind=engine)
router = APIRouter(prefix="/discussion")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/posts")
def create_posts(text: str = Form(...),
                 hashtags: Optional[str] = Form(...),
                 image: UploadFile = File(None),
                 db: Session = Depends(get_db),
                 token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)

    image_url = None
    if image:
        try:
            image_url = upload_to_imgbb(image)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return create_post(db=db, text=text, hashtags=hashtags, user_id=int(current_user['id']), image_url=image_url)


@router.get("/posts")
def get_all_posts(
        tags: Optional[List[str]] = Query(None),
        search_text: Optional[str] = Query(None),
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    return get_posts(db=db, token=token, skip=skip, limit=limit, tags=tags, search_text=search_text)


@router.put("/posts/{post_id}")
def update_posts(post_id: int,
                 text: Optional[str] = Form(None),
                 hashtags: Optional[str] = Form(None),
                 image: UploadFile = File(None),
                 db: Session = Depends(get_db),
                 token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    image_url = None
    if image:
        try:
            image_url = upload_to_imgbb(image)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return update_post(post_id=post_id, text=text, hashtags=hashtags, image_url=image_url, db=db,
                       user_id=int(current_user['id']))


@router.get("/posts/{post_id}")
def get_post_by_id(post_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    return get_single_post_by_id(db=db, post_id=post_id, user_id=int(current_user['id']), token=token)


@router.delete("/posts/{post_id}")
def delete_posts(post_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    return delete_post(db=db, post_id=post_id, user_id=int(current_user['id']))


@router.post("/posts/{post_id}/comments")
def create_comment(post_id: int,
                   data: CommentCreate,
                   db: Session = Depends(get_db),
                   token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    return create_comments(db=db, post_id=post_id, text=data, user_id=int(current_user['id']))


@router.put("/posts/{post_id}/comments/{comment_id}")
def update_comment(post_id: int,
                   comment_id: int,
                   data: CommentCreate,
                   db: Session = Depends(get_db),
                   token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    return update_comments(db=db, post_id=post_id, comment_id=comment_id, text=data, user_id=int(current_user['id']))


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if current_user['id'] != comment.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}


@router.post("/comments/{comment_id}/like")
def like_comment(comment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)

    existing_like = db.query(CommentLike).filter(CommentLike.comment_id == comment_id,
                                                 CommentLike.user_id == current_user['id']).first()
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this comment")

    new_like = CommentLike(user_id=current_user['id'], comment_id=comment_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@router.post("/posts/{post_id}/like")
def like_posts(post_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)

    existing_like = db.query(PostLike).filter(PostLike.post_id == post_id,
                                              PostLike.user_id == current_user['id']).first()
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already liked this post")

    new_like = PostLike(user_id=current_user['id'], post_id=post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@router.post("/comments/{comment_id}/replies")
def create_reply(comment_id: int, reply: ReplieCreate, db: Session = Depends(get_db),
                 token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    new_reply = Replies(user_id=current_user['id'], text=reply.text, comment_id=comment_id)
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


@router.delete("/replies/{replies_id}")
def delete_reply(replies_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user_from_user_service(token)
    reply = db.query(Replies).filter(Replies.id == replies_id).first()
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply not found")
    if current_user['id'] != reply.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to delete this reply")

    db.delete(reply)
    db.commit()
    return {"message": "Reply deleted successfully"}


app.include_router(router)

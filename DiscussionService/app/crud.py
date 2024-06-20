from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .database import logger
from .models import *
from .schema import PostResponse, UserDTO, CommentCreate, CommentDTO, LikeDTO, RepliesDTO, CommentLikeDTO
from .utils import get_user_by_id


def create_post(db: Session, text: str, hashtags: str, user_id: int, image_url: Optional[str]):
    db_post = Post(
        user_id=user_id,
        text=text,
        image_url=image_url,
        created_on=datetime.now(),
        view_count=0
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    if hashtags:
        process_hashtags(db, db_post.id, hashtags.split(','))

    return {
        "id": db_post.id,
        "user_id": db_post.user_id,
        "text": db_post.text,
        "image_url": db_post.image_url,
        "created_on": db_post.created_on,
        "view_count": db_post.view_count,
        "hashtags": [tag for tag in hashtags.split(',')]
    }


def get_posts(db: Session, token: str, tags: Optional[List[str]] = None, search_text: Optional[str] = None,
              skip: int = 0, limit: int = 20) -> List[PostResponse]:
    query = db.query(Post)

    if search_text:
        query = query.filter(Post.text.ilike(f"%{search_text}%"))

    if tags:
        logger.debug(tags)
        query = query.join(PostHashtag).join(Hashtag).filter(Hashtag.tag.in_(tags))

    posts = query.offset(skip).limit(limit).all()

    post_responses = []

    for post in posts:
        post_responses.append(fetch_post_details(post, token, db))

    return post_responses


def update_post(post_id: int, db: Session, text: str, hashtags: str, user_id: int, image_url: Optional[str]):
    db_post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or not authorized to update")
    if text:
        db_post.text = text

    if hashtags:
        update_hashtags(db, post_id, hashtags.split(','))

    if image_url:
        db_post.image_url = image_url

    db.commit()
    db.refresh(db_post)

    return {
        "id": db_post.id,
        "user_id": db_post.user_id,
        "text": db_post.text,
        "image_url": db_post.image_url,
        "created_on": db_post.created_on,
        "view_count": db_post.view_count,
        "hashtags": [h.hashtag.tag for h in db_post.hashtags]
    }


def delete_post(db: Session, post_id: int, user_id: int):
    db_post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or not authorized to delete")

    db.delete(db_post)
    db.commit()
    return {"status": "success", "message": f"Post with id {post_id} deleted successfully"}


def process_hashtags(db: Session, post_id: int, hashtags: list):
    for tag in hashtags:
        logger.debug(f"Processing hashtag: {tag}")
        hashtag = db.query(Hashtag).filter(Hashtag.tag == tag).first()
        if not hashtag:
            hashtag = Hashtag(tag=tag)
            db.add(hashtag)
            db.commit()
            db.refresh(hashtag)
        db_post_hashtag = PostHashtag(post_id=post_id, hashtag_id=hashtag.id)
        db.add(db_post_hashtag)
    db.commit()


def update_hashtags(db: Session, post_id: int, new_hashtags: list):
    current_hashtags = {h.hashtag.tag for h in db.query(PostHashtag).filter(PostHashtag.post_id == post_id).all()}
    new_hashtags_set = set(new_hashtags)

    # Remove old hashtags
    for tag in current_hashtags - new_hashtags_set:
        hashtag = db.query(Hashtag).filter(Hashtag.tag == tag).first()
        if hashtag:
            post_hashtag = db.query(PostHashtag).filter(PostHashtag.post_id == post_id,
                                                        PostHashtag.hashtag_id == hashtag.id).first()
            if post_hashtag:
                db.delete(post_hashtag)

    # Add new hashtags
    for tag in new_hashtags_set - current_hashtags:
        hashtag = db.query(Hashtag).filter(Hashtag.tag == tag).first()
        if not hashtag:
            hashtag = Hashtag(tag=tag)
            db.add(hashtag)
            db.commit()
            db.refresh(hashtag)
        post_hashtag = PostHashtag(post_id=post_id, hashtag_id=hashtag.id)
        db.add(post_hashtag)

    db.commit()


def create_comments(post_id: int, db: Session, text: CommentCreate, user_id: int):
    result = Comment(
        user_id=user_id,
        text=text.text,
        post_id=post_id
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return {
        "id": result.id,
        "user_id": result.user_id,
        "text": result.text,
        "post_id": result.post_id}


def update_comments(post_id: int, comment_id: int, db: Session, text: CommentCreate, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or not exist")
    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to update")

    comment.text = text.text
    db.commit()
    db.refresh(comment)
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "text": comment.text,
        "post_id": comment.post_id}


def get_single_post_by_id(post_id: int, token: str, db: Session, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or not exist")

    result = fetch_post_details(post, token, db)

    if post.user_id != user_id:
        update_post_views(post, user_id, db)
        result.view_count += 1

    return result


def fetch_post_details(post: Post, token: str, db: Session):
    post_user = get_user_by_id(post.user_id, token)
    user_dto = UserDTO(id=post_user["id"], name=post_user["name"])
    comments = []
    for comment in post.comments:
        likes = get_comments_likes(comment.id, db, token)
        dto = CommentDTO(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            text=comment.text,
            created_on=comment.created_on,
            likes=likes,
            total_likes=len(likes),
            replies=get_comments_replies(comment.id, db, token),
            user=get_user_by_id(comment.user_id, token)
        )
        comments.append(dto)

    likes = [
        LikeDTO(
            id=like.id,
            post_id=like.post_id,
            user_id=like.user_id,
            created_on=like.created_on,
            user=get_user_by_id(like.user_id, token)
        )
        for like in post.post_likes
    ]

    post_response = PostResponse(
        id=post.id,
        user=user_dto,
        text=post.text,
        created_on=post.created_on,
        image_url=post.image_url,
        hashtags=[],
        view_count=post.view_count,
        user_id=post.user_id,
        comments=comments,
        likes=likes,
        total_likes=len(likes)
    )

    hashtags = db.query(Hashtag.tag).join(PostHashtag, PostHashtag.hashtag_id == Hashtag.id) \
        .filter(PostHashtag.post_id == post.id).all()

    post_response.hashtags = [tag[0] for tag in hashtags]
    return post_response


def update_post_views(post, user_id, db):
    ex_views = db.query(PostViews).filter(PostViews.post_id == post.id, PostViews.user_id == user_id).first()
    if not ex_views:
        new_view = PostViews(post_id=post.id, user_id=user_id)
        db.add(new_view)
        db.commit()
        db.refresh(new_view)
        post.view_count = post.view_count + 1
        db.commit()
        db.refresh(post)


def get_comments_likes(id: int, db: Session, token: str):
    likes = db.query(CommentLike).filter(CommentLike.comment_id == id).all()
    results = []
    for like in likes:
        user = get_user_by_id(like.user_id, token)
        results.append(
            CommentLikeDTO(
                id=like.id,
                user_id=like.user_id,
                user=user['name']

            )
        )
    return results


def get_comments_replies(id: int, db: Session, token: str):
    replies = db.query(Replies).filter(Replies.comment_id == id).all()
    results = []
    for reply in replies:
        reply_user = get_user_by_id(reply.user_id, token)
        user_dto = UserDTO(id=reply_user["id"], name=reply_user["name"])
        dto = RepliesDTO(
            id=reply.id,
            comment_id=reply.comment_id,
            user_id=reply.user_id,
            text=reply.text,
            created_on=reply.created_on,
            user=user_dto
        )
        results.append(dto)
    return results

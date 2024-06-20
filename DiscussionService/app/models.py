from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(String)
    image_url = Column(String)
    created_on = Column(DateTime, default=datetime.now())
    view_count = Column(Integer, default=0)
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    post_likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    hashtags = relationship("PostHashtag", back_populates="post", cascade="all, delete-orphan")
    post_views = relationship("PostViews", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    created_on = Column(DateTime, default=datetime.now())
    post = relationship("Post", back_populates="comments")
    replies = relationship("Replies", back_populates="comment", cascade="all, delete-orphan")
    comment_likes=relationship("CommentLike", back_populates="comment", cascade="all, delete-orphan")


class PostLike(Base):
    __tablename__ = "post_likes"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_on = Column(DateTime, default=datetime.now())
    post = relationship("Post", back_populates="post_likes")


class Hashtag(Base):
    __tablename__ = "hashtags"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, unique=True)


class PostHashtag(Base):
    __tablename__ = "post_hashtags"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    hashtag_id = Column(Integer, ForeignKey('hashtags.id'))
    post = relationship("Post", back_populates="hashtags")
    hashtag = relationship("Hashtag")


class PostViews(Base):
    __tablename__ = "post_views"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_on = Column(DateTime, default=datetime.now())
    post = relationship("Post", back_populates="post_views")


class Replies(Base):
    __tablename__ = "replies"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)
    created_on = Column(DateTime, default=datetime.now())
    comment = relationship("Comment", back_populates="replies")


class CommentLike(Base):
    __tablename__ = "comment_likes"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_on = Column(DateTime, default=datetime.now())
    comment = relationship("Comment", back_populates="comment_likes")

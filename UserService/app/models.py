from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile_no = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    followers = relationship("Follow", back_populates="followed", foreign_keys="[Follow.followed_id]")
    followings = relationship("Follow", back_populates="follower", foreign_keys="[Follow.follower_id]")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobile_no": self.mobile_no
        }


class Follow(Base):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    followed_id = Column(Integer, ForeignKey('users.id'))
    follower = relationship("User", back_populates="followings", foreign_keys=[follower_id])
    followed = relationship("User", back_populates="followers", foreign_keys=[followed_id])

    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='_follower_followed_uc'),)

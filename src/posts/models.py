from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Integer, DateTime, Boolean, func, ARRAY


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    creator_id = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_private = mapped_column(Boolean, default=False)
    tags = mapped_column(ARRAY(String), nullable=True)


class Comment(Base):
    __tablename__ = "comments"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, nullable=False)
    comment = mapped_column(String, nullable=False)
    creator_id = mapped_column(String, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())


class Like(Base):
    __tablename__ = "likes"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id = mapped_column(Integer, nullable=False)
    creator_id = mapped_column(String, nullable=False)

from sqlalchemy.orm import Session
from models import Post


def create_post(db: Session, title: str, description: str, creator_id: str, is_private: bool, tags: list):
    post = Post(title=title, description=description, creator_id=creator_id, is_private=is_private, tags=tags)
    db.add(post)
    db.commit()
    return post


def delete_post(db: Session, post_id: int, creator_id: str):
    post = db.query(Post).filter(Post.id == post_id, Post.creator_id == creator_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False


def update_post(
    db: Session,
    post_id: int,
    creator_id: str,
    title: str = None,
    description: str = None,
    is_private: bool = None,
    tags: list = None,
):
    post = db.query(Post).filter(Post.id == post_id, Post.creator_id == creator_id).first()
    if post:
        if title is not None:
            post.title = title

        if description is not None:
            post.description = description

        if is_private is not None:
            post.is_private = is_private

        if tags is not None:
            post.tags = tags

        db.commit()
        return post
    return None


def get_post(db: Session, post_id: int, creator_id: str):
    return (
        db.query(Post).filter(Post.id == post_id, (Post.creator_id == creator_id) | (Post.is_private == False)).first()
    )


def list_posts(db: Session, page_number: int, page_size: int, creator_id: str, author_id: str):
    return (
        db.query(Post)
        .filter((Post.creator_id == author_id) & ((Post.is_private == False) | (Post.creator_id == creator_id)))
        .order_by(Post.id)
        .offset(page_number * page_size)
        .limit(page_size)
        .all()
    )

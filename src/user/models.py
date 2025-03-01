from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Date, DateTime, func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    username = mapped_column(String, primary_key=True, index=True)
    hashed_password = mapped_column(String, nullable=False)
    first_name = mapped_column(String)
    last_name = mapped_column(String)
    birth_date = mapped_column(String)
    email = mapped_column(String, nullable=False)
    phone_number = mapped_column(String)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

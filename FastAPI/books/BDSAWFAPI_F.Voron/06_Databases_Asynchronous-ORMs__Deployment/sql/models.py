from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    # SQLAlchemy object contains database schema information
    pass


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    # ForeignKey type automatically handles the column type and constraint by
    # referencing the table and column names.
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False
    )
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Define ORM relationship between Comment and Post objects without creating
    # a new column in SQL definition (ForeignKey's role)
    # Forward reference: Type hint for property set to Post class inside
    # quotes to avoid Python error when accessing something not yet defined.
    post: Mapped["Post"] = relationship(
        "Post",
        # get list of comments from a post
        back_populates="comments",
        lazy="joined",
    )


class Post(Base):
    __tablename__ = "posts"
    # Define Post class, inherits from Base. Define columns as class properties
    # using mapped_column function to specify column type and properties.
    # Type hints added to properties correspond to Python types of columns.
    # Wrapping each type with the Mapped class allows the type checker to
    # comprehend the data's underlying type when assigned to a MappedColumn object.
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    publication_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    # mirror relationship, naming same as back_populates
    comments: Mapped[list[Comment]] = relationship(
        "Comment",
        # ORM behavior when deleting a post: delete comments as well
        cascade="all, delete",
        lazy="joined",
    )

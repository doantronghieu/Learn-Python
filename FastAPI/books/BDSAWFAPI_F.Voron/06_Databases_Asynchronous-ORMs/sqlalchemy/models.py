import add_packages
from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Pydantic models (schemas) validates data, helps with ORM model (models) 
# interaction, serializes data, ORM model handles database communication.

class Base(DeclarativeBase):
  # Base class inherits from DeclarativeBase. 
  # All models will inherit from this class. 
  # SQLAlchemy uses it to keep information about the database schema together. 
  # Create it once in project and always use the same one.
  pass

class Post(Base):
  __tablename__ = "posts"
  # Define Post class, inherits from Base. Define columns as class properties 
  # using mapped_column function to specify column type and properties.
  # Type hints added to properties correspond to Python types of columns. 
  # Wrapping each type with the Mapped class allows the type checker to 
  # comprehend the data's underlying type when assigned to a MappedColumn object.
  id: Mapped[int] = mapped_column(
    Integer, primary_key=True, autoincrement=True,
  )
  publication_date: Mapped[datetime] = mapped_column(
    DateTime, nullable=False, default=datetime.now,
  )
  title: Mapped[str] = mapped_column(
    String(255), nullable=False,
  )
  content: Mapped[str] = mapped_column(
    Text, nullable=False,
  )
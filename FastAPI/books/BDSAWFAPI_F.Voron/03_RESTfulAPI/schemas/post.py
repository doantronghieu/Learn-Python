from pydantic import BaseModel


class Post(BaseModel):
    title: str
    # The nb_views property is in the output. We don’t want this.
    nb_views: int


class PublicPost(BaseModel):
    title: str

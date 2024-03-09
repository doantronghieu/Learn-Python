from typing import Dict
from schemas.post import Post
from schemas.user import User


# Dummy DB
posts = {
    1: Post(title="Hello", nb_views=100)
}

users: Dict[int, User] = {
    1: {"name": "John Doe", "age": 25},
    2: {"name": "Jane Smith", "age": 30},
    3: {"name": "Bob Johnson", "age": 22},
}



from typing import Dict
from schemas import post

posts: Dict[int, post.Post] = {
    1: {"id": 1, "title": "First Post", "content": "This is the content of the first post.", "nb_views": 10},
    2: {"id": 2, "title": "Second Post", "content": "Content for the second post goes here.", "nb_views": 5},
    3: {"id": 3, "title": "Third Post", "content": "Here's the content for the third post.", "nb_views": 15},
}

from enum import Enum


class PostSorting(str, Enum):
    new = "new"
    old = "old"
    most_likes = "most_likes"

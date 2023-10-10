from models.posts import post_table


def find_post(post_id: int):
    return post_table.get(post_id)

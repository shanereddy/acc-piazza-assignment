from datetime import datetime

def is_post_live(now: datetime, expires_at: datetime) -> bool:
    return now < expires_at
  
def user_is_author(post_author_id: int, user_id: int) -> bool:
    return post_author_id == user_id
  
def user_wants_different_reaction(existing_reaction, new_reaction) -> bool:
    existing_reaction != new_reaction
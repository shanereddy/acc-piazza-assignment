from datetime import datetime

def is_post_live(now: datetime, expires_at: datetime) -> bool:
    return now < expires_at
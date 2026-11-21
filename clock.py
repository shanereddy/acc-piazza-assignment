from datetime import datetime, timezone

# Returns the current UTC time
def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)
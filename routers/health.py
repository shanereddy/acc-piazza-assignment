from fastapi import APIRouter

router = APIRouter()

@router.get("/health", status_code=200)
def health():
    return {"message": "This is the Piazza app, everything is ok"}
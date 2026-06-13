from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/")
def get_forecast(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

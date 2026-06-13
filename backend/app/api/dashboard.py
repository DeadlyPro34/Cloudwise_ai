from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {
        "total_spend": 0,
        "potential_savings": 0,
        "health_score": 0,
        "resource_count": 0,
        "cost_trend": []
    }

@router.get("/health-score")
def get_health_score(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {
        "score": 0,
        "resource_efficiency": 0,
        "cost_efficiency": 0,
        "storage_efficiency": 0,
        "forecast_risk": 0
    }

@router.get("/recommendations")
def get_recommendations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

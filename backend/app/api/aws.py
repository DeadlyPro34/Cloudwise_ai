from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/aws", tags=["AWS"])

@router.post("/connect")
def connect_aws(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"account_id": "123456789012", "account_name": "Demo Account", "status": "CONNECTED"}

@router.post("/scan")
def scan_aws(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"ec2_count": 0, "ebs_count": 0, "total_resources": 0, "status": "SUCCESS"}

@router.get("/resources")
def get_resources(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

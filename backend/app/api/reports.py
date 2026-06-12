from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.report_service import generate_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/generate")
def generate(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pdf_bytes = generate_report(db, None)
    return Response(content=pdf_bytes, media_type="application/pdf")

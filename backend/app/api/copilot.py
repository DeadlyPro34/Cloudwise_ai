from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.copilot_service import chat
from app.services.auth_service import get_user_organization
from app.core.limiter import limiter

router = APIRouter(prefix="/copilot", tags=["Copilot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
@limiter.limit("30/minute")
def copilot_chat(request: Request, payload: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    org = get_user_organization(db, current_user.id)
    response, conv_id = chat(db, org.id, payload.message)
    return {"response": response, "conversation_id": str(conv_id)}

@router.get("/history")
def copilot_history(conversation_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

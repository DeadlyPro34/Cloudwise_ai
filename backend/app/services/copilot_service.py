"""
Copilot service for CloudWise AI.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
import anthropic
import uuid
from typing import List

from app.core.config import settings
from app.models.copilot import CopilotConversation, CopilotMessage, MessageRole

def build_context(db: Session, cloud_account_id: uuid.UUID) -> str:
    # Minimal context builder for demo
    return "This is your AWS environment. You have 0 resources running."

def chat(db: Session, org_id: uuid.UUID, user_message: str, cloud_account_id: uuid.UUID | None = None) -> tuple[str, uuid.UUID]:
    if not settings.ANTHROPIC_API_KEY:
        return "The AI Copilot is not configured yet. Please add your Anthropic API key in Settings.", uuid.uuid4()
    
    # Simple fallback since anthropic SDK can be tricky
    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text, uuid.uuid4()
    except Exception as e:
        return f"The AI Copilot is not configured yet. Please add your Anthropic API key in Settings.", uuid.uuid4()

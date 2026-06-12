"""
Report service.
"""

from sqlalchemy.orm import Session
import uuid

def generate_report(db: Session, cloud_account_id: uuid.UUID) -> bytes:
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"

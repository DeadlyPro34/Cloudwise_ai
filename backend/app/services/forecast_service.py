"""
Forecast service.
"""

from sqlalchemy.orm import Session
import uuid

def generate_forecast(db: Session, cloud_account_id: uuid.UUID):
    pass

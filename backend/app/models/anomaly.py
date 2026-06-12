"""
Anomaly model - ML-generated anomaly flags (Isolation Forest output).
"""

import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID


class AnomalySeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Anomaly(Base):
    __tablename__ = "anomalies"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("resource_inventory.id"), nullable=False
    )

    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False)
    # Examples: COST_SPIKE, UNUSUAL_USAGE_PATTERN
    severity: Mapped[AnomalySeverity] = mapped_column(
        SQLEnum(AnomalySeverity, name="anomaly_severity_enum"), nullable=False, index=True
    )
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

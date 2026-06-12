"""
CloudHealthScore model - the "hero metric" per UI/UX brief.
Formula (per TRD):
  Resource Efficiency (35%) + Cost Efficiency (25%) +
  Storage Efficiency (20%) + Forecast Risk (20%) = 0-100 score
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID


class CloudHealthScore(Base):
    __tablename__ = "cloud_health_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    cloud_account_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("cloud_accounts.id"), nullable=False
    )

    score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    resource_efficiency: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    cost_efficiency: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    storage_efficiency: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    forecast_risk: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

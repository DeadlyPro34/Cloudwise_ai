"""
ResourceCost model - historical daily cost snapshots per resource.
Critical for forecasting (Prophet) and Cloud Health Score.
"""

import uuid
from datetime import datetime, date, timezone

from sqlalchemy import Date, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID


class ResourceCost(Base):
    __tablename__ = "resource_costs"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("resource_inventory.id"), nullable=False
    )

    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    daily_cost: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False, default=0)
    monthly_estimate: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False, default=0)
    service_cost: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

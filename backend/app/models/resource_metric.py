"""
ResourceMetric model - CloudWatch utilization metrics.
Used by recommendation engine (e.g., idle EC2 = CPUUtilization < 5%).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID


class ResourceMetric(Base):
    __tablename__ = "resource_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("resource_inventory.id"), nullable=False
    )

    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Examples: CPUUtilization, NetworkIn, NetworkOut, DiskReadOps, DiskWriteOps
    metric_value: Mapped[float] = mapped_column(Numeric, nullable=False)
    metric_unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

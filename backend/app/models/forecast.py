"""
Forecast model - Prophet-generated spending predictions.
"""

import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID


class ForecastType(str, enum.Enum):
    SEVEN_DAY = "7_DAY"
    THIRTY_DAY = "30_DAY"
    NINETY_DAY = "90_DAY"


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    cloud_account_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("cloud_accounts.id"), nullable=False
    )

    forecast_type: Mapped[ForecastType] = mapped_column(
        SQLEnum(ForecastType, name="forecast_type_enum"), nullable=False
    )
    current_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    predicted_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    confidence_interval_low: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    confidence_interval_high: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )

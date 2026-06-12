"""
ResourceInventory model - master inventory of discovered cloud resources.
"""

import uuid
import enum
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.db.types import GUID, JSONB_COMPAT


class ResourceType(str, enum.Enum):
    EC2 = "EC2"
    EBS = "EBS"
    RDS = "RDS"
    S3 = "S3"


class ResourceStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    AVAILABLE = "AVAILABLE"  # for EBS volumes (unattached)
    IN_USE = "IN_USE"        # for EBS volumes (attached)
    TERMINATED = "TERMINATED"
    UNKNOWN = "UNKNOWN"


class ResourceInventory(Base):
    __tablename__ = "resource_inventory"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    cloud_account_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("cloud_accounts.id"), nullable=False
    )

    resource_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resource_type: Mapped[ResourceType] = mapped_column(
        SQLEnum(ResourceType, name="resource_type_enum"), nullable=False, index=True
    )
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    arn: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[ResourceStatus] = mapped_column(
        SQLEnum(ResourceStatus, name="resource_status_enum"),
        nullable=False,
        default=ResourceStatus.UNKNOWN,
    )
    tags: Mapped[dict | None] = mapped_column(JSONB_COMPAT(), nullable=True)

    # Extra metadata specific to resource type (instance_type, volume_size, etc.)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB_COMPAT(), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

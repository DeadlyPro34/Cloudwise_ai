"""
Import all models here so Alembic's autogenerate can discover them
via Base.metadata.
"""

from app.models.user import User
from app.models.organization import Organization
from app.models.cloud_account import CloudAccount, CloudProvider, CloudAccountStatus
from app.models.resource_inventory import ResourceInventory, ResourceType, ResourceStatus
from app.models.resource_cost import ResourceCost
from app.models.resource_metric import ResourceMetric
from app.models.anomaly import Anomaly, AnomalySeverity
from app.models.recommendation import (
    Recommendation,
    RecommendationType,
    RiskLevel,
    Priority,
    RecommendationStatus,
)
from app.models.cloud_health_score import CloudHealthScore
from app.models.forecast import Forecast, ForecastType
from app.models.copilot import CopilotConversation, CopilotMessage, MessageRole

__all__ = [
    "User",
    "Organization",
    "CloudAccount",
    "CloudProvider",
    "CloudAccountStatus",
    "ResourceInventory",
    "ResourceType",
    "ResourceStatus",
    "ResourceCost",
    "ResourceMetric",
    "Anomaly",
    "AnomalySeverity",
    "Recommendation",
    "RecommendationType",
    "RiskLevel",
    "Priority",
    "RecommendationStatus",
    "CloudHealthScore",
    "Forecast",
    "ForecastType",
    "CopilotConversation",
    "CopilotMessage",
    "MessageRole",
]

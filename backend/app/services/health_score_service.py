"""
Health Score service - calculates the Cloud Health Score (0-100).

Formula:
  resource_efficiency (35%) + cost_efficiency (25%) +
  storage_efficiency (20%) + forecast_risk (20%)
"""

import uuid

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.resource_inventory import ResourceInventory, ResourceType, ResourceStatus
from app.models.recommendation import Recommendation, RecommendationStatus
from app.models.resource_cost import ResourceCost
from app.models.forecast import Forecast, ForecastType
from app.models.cloud_health_score import CloudHealthScore


def calculate_health_score(db: Session, cloud_account_id: uuid.UUID) -> dict:
    """Calculate the cloud health score (0-100) and persist it."""

    # Helper subquery: resource IDs belonging to this account
    account_resource_ids = select(ResourceInventory.id).where(
        ResourceInventory.cloud_account_id == cloud_account_id
    )

    # ---- Resource Efficiency (35%) ----
    total_resources = (
        db.execute(
            select(func.count(ResourceInventory.id)).where(
                ResourceInventory.cloud_account_id == cloud_account_id
            )
        ).scalar()
        or 0
    )

    resources_with_recs = (
        db.execute(
            select(func.count(func.distinct(Recommendation.resource_id))).where(
                Recommendation.resource_id.in_(account_resource_ids),
                Recommendation.status == RecommendationStatus.OPEN,
            )
        ).scalar()
        or 0
    )

    if total_resources > 0:
        resource_efficiency = max(
            0.0, 100.0 - (resources_with_recs / total_resources * 100)
        )
    else:
        resource_efficiency = 100.0

    # ---- Cost Efficiency (25%) ----
    total_savings = float(
        db.execute(
            select(func.sum(Recommendation.estimated_monthly_savings)).where(
                Recommendation.resource_id.in_(account_resource_ids),
                Recommendation.status == RecommendationStatus.OPEN,
            )
        ).scalar()
        or 0
    )

    total_spend = float(
        db.execute(
            select(func.sum(ResourceCost.daily_cost)).where(
                ResourceCost.resource_id.in_(account_resource_ids)
            )
        ).scalar()
        or 0
    )

    if total_spend > 0:
        cost_efficiency = max(0.0, 100.0 - (total_savings / total_spend * 100))
    else:
        cost_efficiency = 100.0

    # ---- Storage Efficiency (20%) ----
    total_ebs = (
        db.execute(
            select(func.count(ResourceInventory.id)).where(
                ResourceInventory.cloud_account_id == cloud_account_id,
                ResourceInventory.resource_type == ResourceType.EBS,
            )
        ).scalar()
        or 0
    )

    unattached_ebs = (
        db.execute(
            select(func.count(ResourceInventory.id)).where(
                ResourceInventory.cloud_account_id == cloud_account_id,
                ResourceInventory.resource_type == ResourceType.EBS,
                ResourceInventory.status == ResourceStatus.AVAILABLE,
            )
        ).scalar()
        or 0
    )

    if total_ebs > 0:
        storage_efficiency = max(0.0, 100.0 - (unattached_ebs / total_ebs * 100))
    else:
        storage_efficiency = 100.0

    # ---- Forecast Risk (20%) ----
    latest_forecast = db.execute(
        select(Forecast)
        .where(
            Forecast.cloud_account_id == cloud_account_id,
            Forecast.forecast_type == ForecastType.THIRTY_DAY,
        )
        .order_by(Forecast.generated_at.desc())
    ).scalar_one_or_none()

    if latest_forecast:
        current = float(latest_forecast.current_cost)
        predicted = float(latest_forecast.predicted_cost)
        if current > 0:
            change_pct = ((predicted - current) / current) * 100
            forecast_risk = max(0.0, min(100.0, 100.0 - change_pct * 2))
        else:
            forecast_risk = 100.0
    else:
        forecast_risk = 100.0

    # ---- Weighted Score ----
    score = (
        resource_efficiency * 0.35
        + cost_efficiency * 0.25
        + storage_efficiency * 0.20
        + forecast_risk * 0.20
    )
    score = max(0.0, min(100.0, score))

    # Persist
    health_score = CloudHealthScore(
        cloud_account_id=cloud_account_id,
        score=round(score, 2),
        resource_efficiency=round(resource_efficiency, 2),
        cost_efficiency=round(cost_efficiency, 2),
        storage_efficiency=round(storage_efficiency, 2),
        forecast_risk=round(forecast_risk, 2),
    )
    db.add(health_score)
    db.commit()
    db.refresh(health_score)

    return {
        "score": round(score, 2),
        "resource_efficiency": round(resource_efficiency, 2),
        "cost_efficiency": round(cost_efficiency, 2),
        "storage_efficiency": round(storage_efficiency, 2),
        "forecast_risk": round(forecast_risk, 2),
    }

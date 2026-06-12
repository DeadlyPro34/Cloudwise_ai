from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services import aws_service

router = APIRouter(prefix="/aws", tags=["AWS"])


class AWSConnectRequest(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str = "us-east-1"


@router.post("/connect")
def connect_aws(
    payload: AWSConnectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Validate AWS credentials using STS. Rejects invalid/fake keys."""
    try:
        result = aws_service.connect_aws(
            access_key=payload.aws_access_key_id,
            secret_key=payload.aws_secret_access_key,
            region=payload.region,
        )
        return {
            "account_id": result["account_id"],
            "account_name": result.get("arn", "").split(":")[-1],
            "status": "CONNECTED",
        }
    except Exception as e:
        error_msg = str(e)
        # Give a clean user-facing message for auth errors
        if "InvalidClientTokenId" in error_msg or "AuthFailure" in error_msg or "SignatureDoesNotMatch" in error_msg:
            raise HTTPException(status_code=400, detail="Invalid AWS credentials. Please check your Access Key ID and Secret Access Key.")
        if "AccessDenied" in error_msg:
            raise HTTPException(status_code=400, detail="Access denied. Ensure the IAM user has at least read-only permissions.")
        if "ExpiredToken" in error_msg:
            raise HTTPException(status_code=400, detail="Your AWS credentials have expired. Please generate new credentials.")
        raise HTTPException(status_code=400, detail=f"AWS connection failed: {error_msg}")


@router.post("/scan")
def scan_aws(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"ec2_count": 0, "ebs_count": 0, "total_resources": 0, "status": "SUCCESS"}


@router.get("/resources")
def get_resources(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return []

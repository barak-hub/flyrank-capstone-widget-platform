from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Submission

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

TEMPORARY_TENANT_ID = 1


@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
):
    total_submissions = (
        db.query(func.count(Submission.id))
        .filter(Submission.tenant_id == TEMPORARY_TENANT_ID)
        .scalar()
    )

    membership_inquiries = (
        db.query(func.count(Submission.id))
        .filter(
            Submission.tenant_id == TEMPORARY_TENANT_ID,
            Submission.request_type == "membership_inquiry",
        )
        .scalar()
    )

    general_inquiries = (
        db.query(func.count(Submission.id))
        .filter(
            Submission.tenant_id == TEMPORARY_TENANT_ID,
            Submission.request_type == "general_inquiry",
        )
        .scalar()
    )

    return {
        "tenant_id": TEMPORARY_TENANT_ID,
        "total_submissions": total_submissions,
        "membership_inquiries": membership_inquiries,
        "general_inquiries": general_inquiries,
    }

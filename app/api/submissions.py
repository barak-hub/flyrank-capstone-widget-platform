from app.workers.notification_worker import process_notification
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Submission, Widget
from app.schemas.submission import SubmissionCreate
from app.services.geo_service import get_geo_from_ip
from app.limiter import limiter


router = APIRouter(
    prefix="/api/submissions",
    tags=["Submissions"],
)


@router.get("/{widget_id}")
def get_submissions(
    widget_id: int,
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(Widget.id == widget_id)
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    submissions = (
        db.query(Submission)
        .filter(Submission.widget_id == widget_id)
        .order_by(Submission.id.desc())
        .all()
    )

    return submissions


@router.post(
    "/{widget_id}",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def create_submission(
    widget_id: int,
    data: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(Widget.id == widget_id)
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    # Honeypot spam protection
    if data.honeypot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid submission",
        )

    # Idempotency protection
    if data.idempotency_key:
        existing_submission = (
            db.query(Submission)
            .filter(
                Submission.widget_id == widget_id,
                Submission.idempotency_key == data.idempotency_key,
            )
            .first()
        )

        if existing_submission:
            return {
                "id": existing_submission.id,
                "status": "already_submitted",
            }

    # Get visitor IP address
    ip_address = (
        request.client.host
        if request.client
        else None
    )

    # Get geographic information
    geo = (
        get_geo_from_ip(ip_address)
        if ip_address
        else None
    )

    submission = Submission(
        tenant_id=widget.tenant_id,
        widget_id=widget.id,
        request_type=data.request_type,
        visitor_name=data.visitor_name,
        email=data.email,
        phone=data.phone,
        membership_id=data.membership_id,
        room_number=data.room_number,
        message=data.message,
        ip_address=ip_address,
        geo_country=geo.get("country") if geo else None,
        idempotency_key=data.idempotency_key,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Process notification after successful database storage
    try:
        process_notification(submission.id)
    except Exception:
        # Notification failure must not block the submission response
        pass

    return {
        "id": submission.id,
        "status": "submitted",
    }
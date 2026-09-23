from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.limiter import limiter

from app.database import get_db
from app.models import Submission, Widget
from app.schemas import SubmissionCreate

router = APIRouter(
    prefix="/api/submissions",
    tags=["Submissions"],
)


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
    widget = db.query(Widget).filter(Widget.id == widget_id).first()

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    if data.honeypot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid submission",
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
        ip_address=request.client.host if request.client else None,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return {
        "id": submission.id,
        "status": "submitted",
    }

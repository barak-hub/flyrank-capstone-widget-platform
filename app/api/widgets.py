from app.models import Submission
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import WidgetCreate, WidgetResponse, WidgetUpdate
from app.services import (
    create_widget,
    delete_widget,
    get_widget,
    get_widgets,
    update_widget,
)

router = APIRouter(
    prefix="/api/widgets",
    tags=["Widgets"],
)

TEMPORARY_TENANT_ID = 1


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
):
    total_submissions = (
        db.query(Submission)
        .filter(Submission.tenant_id == TEMPORARY_TENANT_ID)
        .count()
    )

    membership_inquiries = (
        db.query(Submission)
        .filter(
            Submission.tenant_id == TEMPORARY_TENANT_ID,
            Submission.request_type == "membership_inquiry",
        )
        .count()
    )

    general_inquiries = (
        db.query(Submission)
        .filter(
            Submission.tenant_id == TEMPORARY_TENANT_ID,
            Submission.request_type == "general_inquiry",
        )
        .count()
    )

    return {
        "total_submissions": total_submissions,
        "membership_inquiries": membership_inquiries,
        "general_inquiries": general_inquiries,
    }

@router.get("/{widget_id}/config")
def get_public_widget_config(
    widget_id: int,
    response: Response,
    db: Session = Depends(get_db),
):
    widget = get_widget(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
        widget_id=widget_id,
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    response.headers["Cache-Control"] = "public, max-age=300"

    return {
        "id": widget.id,
        "name": widget.name,
        "widget_type": widget.widget_type,
        "status": widget.status,
        "version": widget.version,
    }

@router.post(
    "",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_widget_endpoint(
    data: WidgetCreate,
    db: Session = Depends(get_db),
):
    return create_widget(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
        data=data,
    )


@router.get(
    "",
    response_model=list[WidgetResponse],
)
def list_widgets_endpoint(
    db: Session = Depends(get_db),
):
    return get_widgets(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
    )


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget_endpoint(
    widget_id: int,
    db: Session = Depends(get_db),
):
    widget = get_widget(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
        widget_id=widget_id,
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    return widget


@router.put(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def update_widget_endpoint(
    widget_id: int,
    data: WidgetUpdate,
    db: Session = Depends(get_db),
):
    widget = get_widget(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
        widget_id=widget_id,
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    return update_widget(
        db=db,
        widget=widget,
        data=data,
    )


@router.delete(
    "/{widget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_widget_endpoint(
    widget_id: int,
    db: Session = Depends(get_db),
):
    widget = get_widget(
        db=db,
        tenant_id=TEMPORARY_TENANT_ID,
        widget_id=widget_id,
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    delete_widget(db=db, widget=widget)

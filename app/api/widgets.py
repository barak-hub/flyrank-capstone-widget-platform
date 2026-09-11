from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tenant, Widget
from app.schemas import WidgetCreate, WidgetUpdate, WidgetResponse

router = APIRouter(
    prefix="/api/widgets",
    tags=["Widgets"],
)


def get_current_tenant(db: Session) -> Tenant:
    tenant = db.query(Tenant).first()

    if tenant is None:
        tenant = Tenant(name="Demo Hotel Gym")
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    return tenant


@router.post(
    "",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_widget(
    payload: WidgetCreate,
    db: Session = Depends(get_db),
):
    tenant = get_current_tenant(db)

    widget = Widget(
        tenant_id=tenant.id,
        name=payload.name,
        widget_type=payload.widget_type,
        status="active",
        version=1,
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return widget


@router.get(
    "",
    response_model=list[WidgetResponse],
)
def list_widgets(
    db: Session = Depends(get_db),
):
    tenant = get_current_tenant(db)

    return (
        db.query(Widget)
        .filter(Widget.tenant_id == tenant.id)
        .order_by(Widget.id)
        .all()
    )


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget(
    widget_id: int,
    db: Session = Depends(get_db),
):
    tenant = get_current_tenant(db)

    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.tenant_id == tenant.id,
        )
        .first()
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
def update_widget(
    widget_id: int,
    payload: WidgetUpdate,
    db: Session = Depends(get_db),
):
    tenant = get_current_tenant(db)

    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.tenant_id == tenant.id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    if payload.name is not None:
        widget.name = payload.name

    if payload.widget_type is not None:
        widget.widget_type = payload.widget_type

    if payload.status is not None:
        widget.status = payload.status

    widget.version += 1

    db.commit()
    db.refresh(widget)

    return widget

@router.delete("/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_widget(
    widget_id: int,
    db: Session = Depends(get_db),
):
    tenant = get_current_tenant(db)

    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.tenant_id == tenant.id,
        )
        .first()
    )

    if widget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    db.delete(widget)
    db.commit()

    return None

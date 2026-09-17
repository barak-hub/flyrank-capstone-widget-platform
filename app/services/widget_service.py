from sqlalchemy.orm import Session

from app.models import Widget
from app.schemas import WidgetCreate, WidgetUpdate


def create_widget(
    db: Session,
    tenant_id: int,
    data: WidgetCreate,
) -> Widget:
    widget = Widget(
        tenant_id=tenant_id,
        name=data.name,
        widget_type=data.widget_type,
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return widget


def get_widgets(
    db: Session,
    tenant_id: int,
) -> list[Widget]:
    return (
        db.query(Widget)
        .filter(Widget.tenant_id == tenant_id)
        .order_by(Widget.id)
        .all()
    )


def get_widget(
    db: Session,
    tenant_id: int,
    widget_id: int,
) -> Widget | None:
    return (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.tenant_id == tenant_id,
        )
        .first()
    )


def update_widget(
    db: Session,
    widget: Widget,
    data: WidgetUpdate,
) -> Widget:
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(widget, field, value)

    if "name" in updates or "status" in updates:
        widget.version += 1

    db.commit()
    db.refresh(widget)

    return widget


def delete_widget(
    db: Session,
    widget: Widget,
) -> None:
    db.delete(widget)
    db.commit()

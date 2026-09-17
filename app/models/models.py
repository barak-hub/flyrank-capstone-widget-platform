from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    widgets = relationship("Widget", back_populates="tenant")
    submissions = relationship("Submission", back_populates="tenant")


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    widget_type = Column(String(50), nullable=False)
    status = Column(String(20), default="active", nullable=False)
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    tenant = relationship("Tenant", back_populates="widgets")
    submissions = relationship("Submission", back_populates="widget")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    widget_id = Column(Integer, ForeignKey("widgets.id"), nullable=False, index=True)

    request_type = Column(String(30), nullable=False)
    visitor_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    membership_id = Column(String(100), nullable=True)
    room_number = Column(String(50), nullable=True)
    message = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    geo_country = Column(String(100), nullable=True)
    idempotency_key = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("Tenant", back_populates="submissions")
    widget = relationship("Widget", back_populates="submissions")

    __table_args__ = (
        UniqueConstraint(
            "widget_id",
            "idempotency_key",
            name="uq_widget_idempotency_key",
        ),
    )

import sqlalchemy as sa
from sqlalchemy.sql import func
from src.entities.base import Base


class User(Base):

    __table_args__ = (
        sa.UniqueConstraint('email'),
    )
    email = sa.Column(sa.String(255), index=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
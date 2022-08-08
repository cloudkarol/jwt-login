import sqlalchemy as sa
from src.entities.base import Base


class User(Base):

    __table_args__ = (
        sa.UniqueConstraint('email'),
    )
    email = sa.Column(sa.String(255), index=True, nullable=False)
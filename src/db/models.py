import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base, TimestampMixin


class MentionEdge(Base, TimestampMixin):
    __tablename__ = 'mention_edges'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    source_username: Mapped[str] = mapped_column(
        sa.String
    )
    target_username: Mapped[str] = mapped_column(
        sa.String
    )
    weight: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, default=1
    )

    __table_args__ = (
        UniqueConstraint(
            'source_username','target_username',
                       name='_source_target_uc'
        ),
    )
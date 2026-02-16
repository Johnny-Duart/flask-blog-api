import sqlalchemy as sa
from basic_deploy.models.base import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(
        sa.ForeignKey("role.id"), nullable=False
    )
    role: Mapped["Role"] = relationship(back_populates="user")
    post: Mapped[list["Post"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}), username={self.username!r}"

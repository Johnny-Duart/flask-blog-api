import sqlalchemy as sa
from basic_deploy.models.base import db
from basic_deploy.models.user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

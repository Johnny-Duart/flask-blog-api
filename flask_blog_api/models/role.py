import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_blog_api.models.base import db
from flask_blog_api.models.user import User


class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

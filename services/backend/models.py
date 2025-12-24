from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Boolean, Integer


Base = declarative_base()


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[bool] = mapped_column(Boolean, primary_key=True, default=True)
    count: Mapped[int] = mapped_column(Integer, default=0)

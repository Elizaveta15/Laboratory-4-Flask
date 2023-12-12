from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class Doctor(Base):
    __tablename__ = 'doctors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(unique=True, nullable=False)
    spec: Mapped[Optional[str]] = mapped_column(unique=True, nullable=False)
    phone: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Doctor (id={self.id!r}, name={self.name!r}, phone={self.phone!r}, spec={self.spec!r})"

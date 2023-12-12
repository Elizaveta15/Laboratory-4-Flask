from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'
    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctor.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    slot: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Doctor (id={self.id!r}, doctor_id={self.doctor_id!r}, user_id={self.user_id!r}, slot={self.slot!r})"

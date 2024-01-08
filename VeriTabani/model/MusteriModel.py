from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from VeriTabani.model.TemelVeriModeli import TemelVeriModeli


class MusteriModel(TemelVeriModeli):
    __tablename__ = "musteri"

    musteri_adi: Mapped[str] = mapped_column(String(50),nullable=False)
    musteri_soyadi: Mapped[str] = mapped_column(String(50),nullable=False)
    musteri_hesabi: Mapped[str] = mapped_column(String(50),nullable=False)
    musteri_cinsiyeti: Mapped[str] = mapped_column(nullable=False)

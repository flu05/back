from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from VeriTabani.model.TemelVeriModeli import TemelVeriModeli


class UrunSatisModel(TemelVeriModeli):
    __tablename__ = "satis_hareketleri"

    urun_id: Mapped[int] = mapped_column(ForeignKey('urunler.id'))
    miktar: Mapped[float] = mapped_column(nullable=False)
    birim_fiyat: Mapped[float] = mapped_column(nullable=False)
    tarih: Mapped[date] = mapped_column(default=date.today())

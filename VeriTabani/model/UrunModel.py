from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from VeriTabani.model.TemelVeriModeli import TemelVeriModeli
from VeriTabani.model.UrunAlisModel import UrunAlisModel
from VeriTabani.model.UrunSatisModel import UrunSatisModel


class UrunModel(TemelVeriModeli):
    __tablename__ = 'Urun'

    urun_adi: Mapped[str] = mapped_column(String(50),nullable=False)
    urun_kodu: Mapped[str] = mapped_column(nullable=False)
    urun_fiyati: Mapped[float] = mapped_column(nullable=False)
    urun_aciklamasi: Mapped[str] = mapped_column(String(250),nullable=False)

    alislar: Mapped[list['UrunAlisModel']] = relationship()
    satislar: Mapped[list['UrunSatisModel']] = relationship()

    @property
    def stokMiktari(self):
        return sum([alis.miktar for alis in self.alislar]) - sum([satis.miktar for satis in self.satislar])
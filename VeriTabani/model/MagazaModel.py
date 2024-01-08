from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from VeriTabani.model.TemelVeriModeli import TemelVeriModeli


class MagazaModel(TemelVeriModeli):
    __tablename__ = 'magaza'

    # magaza_id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    magaza_adi: Mapped[str] = mapped_column(String(50),nullable=False)
    magaza_adresi: Mapped[str] = mapped_column(String(255),nullable=False)
    magaza_tel: Mapped[str] = mapped_column(String(50),nullable=False)
    magaza_yetkilikisi: Mapped[str] = mapped_column(String(50),nullable=False)

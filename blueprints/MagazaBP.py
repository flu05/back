import bp
from flask import Blueprint, request
from sqlalchemy import select
from VeriTabani import MagazaModel,db

magaza_bp=Blueprint('magaza_bp',__name__)

@magaza_bp.route('/',methods=['GET'])
@magaza_bp.route('',methods=['GET'])
def index():
    sorgu=select(MagazaModel)

    cevap =db.session.scalars(sorgu).all()
    return [magaza.to_dict() for magaza in cevap]

@magaza_bp.route('/',methods=['POST'])
@magaza_bp.route('',methods=['POST'])
def ekle():
    magaza=MagazaModel()
    magaza.magaza_adi=request.json['adi']
    magaza.magaza_adresi=request.json['adresi']
    magaza.magaza_tel=request.json['tel']
    magaza.magaza_yetkilikisi=request.json['yetkili']

    db.session.add(magaza)
    db.session.commit()

    return magaza.to_dict()

@magaza_bp.route('/',methods=['GET'])
def getir(id:int):
    sorgu=select(MagazaModel).where(MagazaModel.id==id)
    cevap =db.session.scalars(sorgu).one()
    return cevap.to_dict()

@bp.route("/<int:id>", methods=['PUT', 'PATCH'])
def duzenle(id: int):
    sorgu=select(MagazaModel).where(MagazaModel.id==id)
    magaza =db.session.scalars(sorgu).one()

    magaza.magaza_adi=request.json['adi']
    magaza.magaza_adresi=request.json['adresi']
    magaza.magaza_tel=request.json['tel']
    magaza.magaza_yetkilikisi=request.json['yetkili']

    db.session.commit()
    return magaza.to_dict()

@bp.route("/<int:id>", methods=['DELETE'])
def sil(id:int):
    sorgu=select(MagazaModel).where(MagazaModel.id==id)
    magaza=db.session.scalars(sorgu).one()
    db.session.delete(magaza)
    db.session.commit()

    return {'silinen':magaza.to_dict()}
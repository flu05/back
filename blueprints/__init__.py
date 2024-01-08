from flask import Blueprint

from blueprints.GenelBP import genel_bp
from VeriTabani import MagazaModel, MusteriModel, SiparisModel, UrunModel,UrunAlisModel, UrunSatisModel

v1_bp = Blueprint('v1_bp', __name__)

v1_bp.register_blueprint(genel_bp(MagazaModel, 'magaza_bp'), url_prefix='/magaza')
v1_bp.register_blueprint(genel_bp(MusteriModel, 'musteri_bp'), url_prefix='/musteri')
v1_bp.register_blueprint(genel_bp(SiparisModel, 'siparis_bp'), url_prefix='/siparis')
v1_bp.register_blueprint(genel_bp(UrunModel, 'urun_bp'), url_prefix='/urun')
v1_bp.register_blueprint(genel_bp(UrunAlisModel, 'urun_alis_bp'), url_prefix='/urun_alis')
v1_bp.register_blueprint(genel_bp(UrunSatisModel, 'urun_satis_bp'), url_prefix='/urun_satis')

api_bp = Blueprint('api_bp', __name__)
api_bp.register_blueprint(v1_bp, url_prefix='/v1')
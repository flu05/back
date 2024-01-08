from flask_sqlalchemy import SQLAlchemy

from VeriTabani.model.TemelVeriModeli import TemelVeriModeli

from .model import *

db=SQLAlchemy(model_class=TemelVeriModeli)
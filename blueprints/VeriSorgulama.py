from datetime import date

from flask import request, abort
from sqlalchemy import Select, inspect


def sorgula(sorgu: Select, veri_sinifi: type, sayfa_no: int = 0, kayit_sayisi: int = 10):
    """
    Sorgulama fonksiyonunu çalıştıracak fonksiyon

    1- sayfalama ve kayıt sayısı:
    bu bilgiler parametrik olarak gelecek ve url içinde
    https://xyz.com/api/v1/eticaret/<sayfa_no>/<kayit_sayisi>
    şeklinde yer alacaktır.
    :return:
    """
    sorgu = sorgu.limit(kayit_sayisi)
    sorgu = sorgu.offset(sayfa_no * kayit_sayisi)
    """
    2- Sıralama 
    Sıralama query string ile yapılır. 
    https://xyz.com/api/v1/eticaret?sirala=ar_<alanadi1>&sirala=az_<alanadi2>
    Eğer alan adı ar_ ile başlarsa artan, az_ile başlarsa azalan sıralama demektir. 
    """
    siralama_alanlari = request.args.getlist('sirala')

    sutunlar = [col.key for col in inspect(veri_sinifi).mapper.column_attrs]

    for alan_adi in siralama_alanlari:
        if alan_adi.startswith('ar_'):
            gercek_alan_adi = alan_adi[3:]
            sorgu = sorgu.order_by(getattr(veri_sinifi, gercek_alan_adi).asc())
        elif alan_adi.startswith('az_'):
            gercek_alan_adi = alan_adi[3:]
            sorgu = sorgu.order_by(getattr(veri_sinifi, gercek_alan_adi).desc())

    # Filtreleme

    filtre = request.args.getlist('f')
    if len(filtre) > 0:
        operator_karakterleri = list('<>=|~!')

        ayrilmis_filtreler = []

        for filtre_metni in filtre:
            alan_adi = []
            operator = []
            deger = []

            adim = 0
            for karakter in filtre_metni:
                if adim == 0 and karakter not in operator_karakterleri:
                    alan_adi.append(karakter)
                elif adim == 0 and karakter in operator_karakterleri:
                    adim = 1
                    operator.append(karakter)
                elif adim == 1 and karakter in operator_karakterleri:
                    operator.append(karakter)
                elif adim == 1 and karakter in operator_karakterleri:
                    adim = 2
                    deger.append(karakter)
                else:
                    deger.append(karakter)

            alan_adi_str = "".join(alan_adi)
            operator_str = "".join(operator)
            deger_str = "".join(deger)

            ayrilmis_filtreler.append((alan_adi_str, operator_str, deger_str))

        # filtreyi calıstırma
        tablo_alanlari = inspect(veri_sinifi).mapper.column_attrs

        for alan, op, deger in ayrilmis_filtreler:
            tablo_alani = tablo_alanlari[alan].class_attribute
            if tablo_alani.type.python_type in [int, float]:
                # tamsayı filtrelemesi
                kabul_edilen_operatorler = ['>', '>=', '<', '<=', '=', '~']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '~':
                        degerler = [float(d) for d in deger.split(',')]
                        sorgu = sorgu.where(tablo_alani.between(degerler[0], degerler[1]))
                    else:
                        if op == '>':
                            sorgu = sorgu.where(tablo_alani > float(deger))
                        elif op == '<':
                            sorgu = sorgu.where(tablo_alani < float(deger))
                        elif op == '>=':
                            sorgu = sorgu.where(tablo_alani >= float(deger))
                        elif op == '<=':
                            sorgu = sorgu.where(tablo_alani <= float(deger))
                        else:
                            sorgu = sorgu.where(tablo_alani == float(deger))
            elif tablo_alani.type.python_type in [str]:
                # metin filtrelemesi
                kabul_edilen_operatorler = ['|=', '=|', '|=|', '!=', '=!', '!=!']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '|=':
                        sorgu = sorgu.where(tablo_alani.startswith(deger))
                    elif op == '=|':
                        sorgu = sorgu.where(tablo_alani.endswith(deger))
                    elif op == '|=|':
                        sorgu = sorgu.where(tablo_alani.contains(deger))
                    elif op == '!=':
                        sorgu = sorgu.where(tablo_alani.istartswith(deger))
                    elif op == '=!':
                        sorgu = sorgu.where(tablo_alani.iendswith(deger))
                    else:
                        sorgu = sorgu.where(tablo_alani.icontains(deger))
            elif tablo_alani.type.python_type in [date]:
                # tarih filtrelemesi
                kabul_edilen_operatorler = ['>', '<', '~', '=']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '~':
                        degerler = [date(d) for d in deger.split(',')]
                        sorgu = sorgu.where(tablo_alani.between(degerler[0], degerler[1]))
                    else:
                        if op == '>':
                            sorgu = sorgu.where(tablo_alani > date(deger))
                        elif op == '<':
                            sorgu = sorgu.where(tablo_alani < date(deger))
                        else:
                            sorgu = sorgu.where(tablo_alani == date(deger))

    return sorgu

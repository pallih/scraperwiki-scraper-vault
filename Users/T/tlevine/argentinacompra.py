from requests import session
 
s = session()

url = u'https://www.argentinacompra.gov.ar/prod/onc/sitio/Perfiles/PUB/mcc_consulta_vig.asp'

# Sök
s.get(url, verify = False)
r = s.post(url, {
    'slcAgrupacion': 0,
    'slcOrganismo': 24,
    'slcRubros': 0,
    'txtObjeto': '',
    'txtFechaDesde': '',
    'txtFechaHasta': '',
    'slcTipo': 0,
    'txtNroContratacion': '',
    'txtAnoContratacion': '',
    'lista': 'si',
    'NumeroFiltro': '',
    'page': '',
}, verify = False)

print r.text
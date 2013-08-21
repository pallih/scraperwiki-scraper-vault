import scraperwiki
import requests
import lxml.html
import re

for region in range(1,20): # there are 19 regions numbered 1-19
    params = {'codCCAA': region, 'codZona': '', 'provinciaMapa': '', 'actionProcedencia': '', 'codProvincia': '', 'codMunicipio': '', 'denZona': ''}
    html = requests.post('http://nayade.msc.es/Splayas/ciudadano/ciudadanoListaZonaAction.do', params=params)
    dom = lxml.html.fromstring(html.text)
    for a in dom.cssselect('a.valorCampo'):
        zone = re.findall(r'\d+', a.get('href'))[0] # pull the number out of the hideous javascript:… url
        params = {'codCCAA': region, 'codZona': zone, 'actionProcedencia': 'ciudadanoListaZonaAction', 'codProvincia': '', 'codMunicipio': ''}
        html2 = requests.post('http://nayade.msc.es/Splayas/ciudadano/ciudadanoVerZonaAction.do', params=params)
        print html2.text # horrible HTML table layout to be parsed in here


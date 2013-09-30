import scraperwiki

import requests
from lxml import etree


class Renfe(object):
    def __init__(self):
        self.nucleos = {}
        params_config = {'action': 'CONFIG', 'lang': 'ES'}
        api_url = 'http://api.mo2o.com/apps/RenfeApp/'
        config_req = requests.get(api_url, params=params_config)
        config_tree = etree.fromstring(config_req.content)
        self.content = config_tree.find('contents')

        self._parse_config_nucleos()
        # self._parse_config_tarifas()
        #incidencias = content.find('incidencias')
        self._parse_nucleos()

    def _parse_nucleo(self, nucleo):
        nucleo_keys = ('name', 'dateTimeUpdate', 'estaciones', 'lineas', 'mapaesquematico', 'mapaesquematicoimg', 'tarifas')
        nucleo_data = {key: nucleo.find(key).text for key in nucleo_keys}
        nucleo_id = int(nucleo.find('id').text)
        self.nucleos[nucleo_id].update({'content': nucleo_data})

    def _parse_nucleos(self):
        nucleos = self.content.find('nucleos')
        map(self._parse_nucleo, nucleos)

    def _parse_config_nucleo(self, nucleo):
        config_keys = ('Descripcion', 'Lon', 'Lat', 'IconoMapa', 'Tarifas', 'Incidencias')
        nucleo_config = {key.lower(): nucleo.find(key).text for key in config_keys}
        nucleo_codigo = int(nucleo.find('Codigo').text)
        nucleo = {nucleo_codigo: {'config': nucleo_config}}
        self.nucleos.update(nucleo)

    def _parse_config_nucleos(self):
        config_url = self.content.find('config_nucleos').find('file').text
        config_req = requests.get(config_url)
        config_tree = etree.fromstring(config_req.content)
        map(self._parse_config_nucleo, config_tree)

    def _parse_config_tarifa(self, tarifa):
        nc = int(tarifa.find('NC').text)
        tarifa_data = {}
        cr_list = tarifa.findall('CR')
        for cr in cr_list:
            ncr = int(cr.find('NCR').text)
            p_l = float(cr.find('P_L').text)
            p_f = float(cr.find('P_F').text)
            tarifa_data.update({ncr: {'p_l': p_l, 'p_f': p_f}})
        # self.nucleos[nc].update({'tarifa': tarifa_data})

    def _parse_config_tarifas(self):
        # http://api.mo2o.com/apps/RenfeApp/contents/maestra_tarifas.xml.gz
        config_url = self.content.find('config_tarifas').find('file').text
        config_req = requests.get(config_url)
        config_tree = etree.fromstring(config_req.content)
        map(self._parse_config_tarifa, config_tree[0])

r = Renfe()

import pprint
pprint.pprint(r.nucleos)

# http://horarios.renfe.com/cer/horarios/horarios.jsp?nucleo=10&d=60103&df=20130129&hd=24&ho=13&o=60107
import scraperwiki

import requests
from lxml import etree


class Renfe(object):
    def __init__(self):
        self.nucleos = {}
        params_config = {'action': 'CONFIG', 'lang': 'ES'}
        api_url = 'http://api.mo2o.com/apps/RenfeApp/'
        config_req = requests.get(api_url, params=params_config)
        config_tree = etree.fromstring(config_req.content)
        self.content = config_tree.find('contents')

        self._parse_config_nucleos()
        # self._parse_config_tarifas()
        #incidencias = content.find('incidencias')
        self._parse_nucleos()

    def _parse_nucleo(self, nucleo):
        nucleo_keys = ('name', 'dateTimeUpdate', 'estaciones', 'lineas', 'mapaesquematico', 'mapaesquematicoimg', 'tarifas')
        nucleo_data = {key: nucleo.find(key).text for key in nucleo_keys}
        nucleo_id = int(nucleo.find('id').text)
        self.nucleos[nucleo_id].update({'content': nucleo_data})

    def _parse_nucleos(self):
        nucleos = self.content.find('nucleos')
        map(self._parse_nucleo, nucleos)

    def _parse_config_nucleo(self, nucleo):
        config_keys = ('Descripcion', 'Lon', 'Lat', 'IconoMapa', 'Tarifas', 'Incidencias')
        nucleo_config = {key.lower(): nucleo.find(key).text for key in config_keys}
        nucleo_codigo = int(nucleo.find('Codigo').text)
        nucleo = {nucleo_codigo: {'config': nucleo_config}}
        self.nucleos.update(nucleo)

    def _parse_config_nucleos(self):
        config_url = self.content.find('config_nucleos').find('file').text
        config_req = requests.get(config_url)
        config_tree = etree.fromstring(config_req.content)
        map(self._parse_config_nucleo, config_tree)

    def _parse_config_tarifa(self, tarifa):
        nc = int(tarifa.find('NC').text)
        tarifa_data = {}
        cr_list = tarifa.findall('CR')
        for cr in cr_list:
            ncr = int(cr.find('NCR').text)
            p_l = float(cr.find('P_L').text)
            p_f = float(cr.find('P_F').text)
            tarifa_data.update({ncr: {'p_l': p_l, 'p_f': p_f}})
        # self.nucleos[nc].update({'tarifa': tarifa_data})

    def _parse_config_tarifas(self):
        # http://api.mo2o.com/apps/RenfeApp/contents/maestra_tarifas.xml.gz
        config_url = self.content.find('config_tarifas').find('file').text
        config_req = requests.get(config_url)
        config_tree = etree.fromstring(config_req.content)
        map(self._parse_config_tarifa, config_tree[0])

r = Renfe()

import pprint
pprint.pprint(r.nucleos)

# http://horarios.renfe.com/cer/horarios/horarios.jsp?nucleo=10&d=60103&df=20130129&hd=24&ho=13&o=60107

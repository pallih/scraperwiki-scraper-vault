import scraperwiki
import lxml.html

class Ciklus(object):
    MAPPING = {1990: 34,
                1994: 35,
                1998: 36,
                2002: 37,
                2006: 38,
                2010: 39}

    ELEMENTS = {1990: {'napok': 379,
                       'felszolalasok': 'http://www.parlament.hu/naplo34/379/379tart.html',
                        'szoveg' : 'http://www.parlament.hu/naplo35/001/0010042.htm',
                        'eleje': '<p>',
                        'vege': '<a href="http://www.mkogy.hu">Homepage</a>'],
                1994: {'napok': 346,
                        'felszolalasok': 'http://www.parlament.hu/naplo35/346/346tart.htm',
                        'szoveg': 'http://www.parlament.hu/naplo35/001/0010042.htm',
                1998: 36,
                2002: 37,
                2006: 38,
                2010: 39}


    def __init__(self,evszam):
        self.evszam = evszam

    def url(self):
        return 'http://www.mkogy.hu/internet/plsql/ogy_naplo.naplo_ujnapok_ckl?p_ckl=%s' % MAPPING[self.evszam]

class Ulesnap(object):
    def url(self):
        import scraperwiki
import lxml.html

class Ciklus(object):
    MAPPING = {1990: 34,
                1994: 35,
                1998: 36,
                2002: 37,
                2006: 38,
                2010: 39}

    ELEMENTS = {1990: {'napok': 379,
                       'felszolalasok': 'http://www.parlament.hu/naplo34/379/379tart.html',
                        'szoveg' : 'http://www.parlament.hu/naplo35/001/0010042.htm',
                        'eleje': '<p>',
                        'vege': '<a href="http://www.mkogy.hu">Homepage</a>'],
                1994: {'napok': 346,
                        'felszolalasok': 'http://www.parlament.hu/naplo35/346/346tart.htm',
                        'szoveg': 'http://www.parlament.hu/naplo35/001/0010042.htm',
                1998: 36,
                2002: 37,
                2006: 38,
                2010: 39}


    def __init__(self,evszam):
        self.evszam = evszam

    def url(self):
        return 'http://www.mkogy.hu/internet/plsql/ogy_naplo.naplo_ujnapok_ckl?p_ckl=%s' % MAPPING[self.evszam]

class Ulesnap(object):
    def url(self):
        
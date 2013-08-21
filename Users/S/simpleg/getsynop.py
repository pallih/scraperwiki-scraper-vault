import scraperwiki
import urllib, urllib2
import chardet

def decode_string(key, value):
    enc = chardet.detect(value)
    if enc['encoding']:
        value = value.decode(enc['encoding'])

#    lambda k, v: (k,v.decode(chardet.detect(v)['encoding']))
    return (key, value)
    


### Je bosse la dedans
SYNOP_BASE_URL = "http://stationmeteo.meteorologic.net/synop/your-synop.php" # On met en maj vu que c'est une globale

def get_synop_for_day(**kwargs):
    """
    Get synop file handler
    @param wmo : ...
    @param day : ...
    @see params of get_synop
    """
    kwargs.update({"type":"mes", "mode":"day"})
    return get_synop(**kwargs)

def get_synop(method='POST',**kwargs):
    enc = urllib.urlencode(kwargs)
    if method == 'POST':
        return urllib2.urlopen(SYNOP_BASE_URL, enc)
    else:
        return urllib2.urlopen(SYNOP_BASE_URL + "?" + enc)
###

print "will start"

sourcescraper = 'scrap_synop_id'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('* from %s.swdata' % (sourcescraper,))

"""
Find doc format here http://blogdev.meteorologic.net/index.php?2008/03/19/10-synop-api-d-acces-aux-donnees
"""


base_url = "http://stationmeteo.meteorologic.net/synop/your-synop.php?wmo=%(wmo)s&type=mes&mode=day&day=080311"



synop_keys = ["date","temp","point_rose","humidite","vent_v","rafale_v",
                "vent_d","vent_d_text","pression","delta_p","precip","precip_duree","precip_24",
                "visi","h_base_nuage","nebulosite","temp_min_jour","temp_max_jour","neige_txt","couche_neige",
                "etat_mer", "temp_mer","h_vague","obs_station"
            ]

for row in data:
    print "treat ", row
    response = get_synop_for_day(wmo = row["wmo"], day = "080311", method='GET') #urllib2.urlopen(base_url%row)
    html = response.read()
    if html != "No data":
        splited_rows = html.split("\n")
        for data_row in splited_rows:
            splited_data = data_row.split("#")
            if len(splited_data) == 25:
                dict_data = dict(map(decode_string, synop_keys, splited_data[:24]))
                dict_data["city"] = row["city"]
                dict_data["wmo"] = row["wmo"]
                scraperwiki.sqlite.save(unique_keys=["wmo","date"], data= dict_data)



        
    
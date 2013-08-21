# -*- coding: utf-8 -*-

import lxml.html 
import datetime
import pprint

import scraperwiki


def intorzero(v):
    "Converts value to int. Returns 0 on failure."
    try:
        return int(v)
    except:
        return 0

def parse_raw(raw):
    "Parse input HTML. Returns dict indexed with tuple (hour, direction) with counters in values."
    d = {}
    root = lxml.html.fromstring(raw)
    for (id, value) in [(el.attrib['id'], el.text) for el in root.cssselect('td.noedit')]:
        if 'hour_time_local' in id: 
            hour = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif 'detection_count' in id: 
            direction = id.split('_', 1)[1].split('*')[0]
            d[(hour, direction)] = intorzero(value)
        elif 'temperature' in id:
            pass 
            #d[(hour, 'temp')] = intorzero(value)
        else:
            pass
            #d[hour][id] = value
    return d
 

def load_counters():
    "Returns list of counter ids. TODO: Load from sqlite."
    return [
        "BC_DU-KRST",
        "BC_KJ-HRHO",
        "BC_KO-VYHO",
        "BC_PN-VYBR",
        "BC_RN-JK",
        "BC_SU-VS",
        "BC_ST-RABA",
        "BC_TL-TRHO",
        "BC_VR-ST",
        "BC_SU-KRKA",
        "BC_PT-ZOVO",
        "BC_HZ-CE",
        "BC_DS-KJVL",
        "BC_VK-HRUP",
        "BC_VF-ARUE",
        "BC_VK-MOKO",
        "BC_DE-EVSA",
        "BC_CB-CHTU",
        "BC_NS-PAVL",
        "BC_PP-ROJP",
        "BC_KO-LEPR",
        "BC_JG-PNPC",
        "BC_VS-CE",
        "BC_SH-SEKU",
        "BC_BS-BMZL",
        "BC_KR-RAZB",
        "BC_NM-CEKV",
        "BC_CT-OTPB",
    ]

def get_raw(start, end, counter):
    "Given start and end datetimes and counter id, returns URL to parse."
    url = 'https://unicam.camea.cz/Discoverer/StatsReports/bike-counter/stats-customer-hour-content/df/%s%%2000:00:00/dt/%s%%2000:00:00/sn/%s/sel/1' % (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), counter)
    return scraperwiki.scrape(url)

def load_data(start, end, counters=[]):
    "Parse and load counters in given datetime interval."
    out = {}
    if not counters:
         counters = load_counters()
    for counter in counters:
         raw = get_raw(start, end, counter)
         parsed = parse_raw(raw)
         out.update(parsed)
    return out

def save_or_update(data):
    "Given retun values from load_data, updates swdata sqlite table."
    for ((dt, direction), value) in data.items():
        if direction == 'temp':
            continue
        scraperwiki.sqlite.save(
            unique_keys=["datetime", "direction"],
            data={"datetime": dt, "direction": direction, 'count': value}
        )


# Load data
data = load_data(
    datetime.date.today() - datetime.timedelta(days=2),
    datetime.date.today(),
)
# Save
save_or_update(data)
        






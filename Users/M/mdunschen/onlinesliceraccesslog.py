import scraperwiki
import urllib2

import re, datetime

url = r"http://www.freesteel.co.uk/sliceserver.out.txt"

def geolocate(ip):
    try:
        r = urllib2.urlopen('http://www.geoplugin.net/json.gp?ip=%s' % ip).read()
    except urllib2.HTTPError, e:
        return 'unknown', 'unknown'
    latm = re.match('.*"geoplugin_latitude":([0-9\.+-]*)', r, re.DOTALL)
    lonm = re.match('.*"geoplugin_longitude":([0-9\.+-]*)', r, re.DOTALL)
    return float(latm.group(1)), float(lonm.group(1))

f = urllib2.urlopen(url).read()

allips = re.findall('\d{1,3}?\.\d{1,3}?\.\d{1,3}?\.\d*', f)
uniques = []
for ip in allips:
    if ip not in uniques:
        uniques.append(ip)

pat1 = '.*?(\d\d\.\d\d\.\d\d\d\d) (\d\d\:\d\d\:\d\d) %s, lat=([\d+-\.]*|unknown), lon=([\d+-\.]*|unknown)'
pat2 = '.*(\d\d\.\d\d\.\d\d\d\d) (\d\d\:\d\d\:\d\d) %s, lat=([\d+-\.]*|unknown), lon=([\d+-\.]*|unknown)'
for ip in uniques:
    # find first and last appearance

    m = re.match(pat1 % ip, f, re.DOTALL)
    if not m:
        continue

    sD, sM, sY = tuple([int(v) for v in m.group(1).split('.')])
    sh, sm, ss = tuple([int(v) for v in m.group(2).split(':')])
    m = re.match(pat2 % ip, f, re.DOTALL)
    eD, eM, eY = tuple([int(v) for v in m.group(1).split('.')])
    eh, em, es = tuple([int(v) for v in m.group(2).split(':')])

    # try some geolocation
    if m.group(3) == 'unknown':
        lat, lon = geolocate(ip)
    else:
        lat = float(m.group(3))
        lon = float(m.group(4))
    scraperwiki.sqlite.save(['IP', 'startdate'], {'IP': ip, 'startdate': datetime.date(sY, sM, sD), 'starttime': datetime.time(sh, sm, ss), 'enddate': datetime.date(eY, eM, eD), 'endtime': datetime.time(eh, em, es), 'Latitude':lat, 'Longitude':lon})

import scraperwiki
import urllib2

import re, datetime

url = r"http://www.freesteel.co.uk/sliceserver.out.txt"

def geolocate(ip):
    try:
        r = urllib2.urlopen('http://www.geoplugin.net/json.gp?ip=%s' % ip).read()
    except urllib2.HTTPError, e:
        return 'unknown', 'unknown'
    latm = re.match('.*"geoplugin_latitude":([0-9\.+-]*)', r, re.DOTALL)
    lonm = re.match('.*"geoplugin_longitude":([0-9\.+-]*)', r, re.DOTALL)
    return float(latm.group(1)), float(lonm.group(1))

f = urllib2.urlopen(url).read()

allips = re.findall('\d{1,3}?\.\d{1,3}?\.\d{1,3}?\.\d*', f)
uniques = []
for ip in allips:
    if ip not in uniques:
        uniques.append(ip)

pat1 = '.*?(\d\d\.\d\d\.\d\d\d\d) (\d\d\:\d\d\:\d\d) %s, lat=([\d+-\.]*|unknown), lon=([\d+-\.]*|unknown)'
pat2 = '.*(\d\d\.\d\d\.\d\d\d\d) (\d\d\:\d\d\:\d\d) %s, lat=([\d+-\.]*|unknown), lon=([\d+-\.]*|unknown)'
for ip in uniques:
    # find first and last appearance

    m = re.match(pat1 % ip, f, re.DOTALL)
    if not m:
        continue

    sD, sM, sY = tuple([int(v) for v in m.group(1).split('.')])
    sh, sm, ss = tuple([int(v) for v in m.group(2).split(':')])
    m = re.match(pat2 % ip, f, re.DOTALL)
    eD, eM, eY = tuple([int(v) for v in m.group(1).split('.')])
    eh, em, es = tuple([int(v) for v in m.group(2).split(':')])

    # try some geolocation
    if m.group(3) == 'unknown':
        lat, lon = geolocate(ip)
    else:
        lat = float(m.group(3))
        lon = float(m.group(4))
    scraperwiki.sqlite.save(['IP', 'startdate'], {'IP': ip, 'startdate': datetime.date(sY, sM, sD), 'starttime': datetime.time(sh, sm, ss), 'enddate': datetime.date(eY, eM, eD), 'endtime': datetime.time(eh, em, es), 'Latitude':lat, 'Longitude':lon})


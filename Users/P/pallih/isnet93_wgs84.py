# Blank Python

import os, cgi
import math
import simplejson

#qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def isnet93_to_wgs84(xx,yy):
    x = xx;
    y = yy;
    a = 6378137.0;
    f = 1/298.257222101;
    lat1 = 64.25;
    lat2 = 65.75;
    latc = 65.00;
    lonc = 19.00;
    eps = 0.00000000001;   
    def fx(p):
        return  a * math.cos(p/rho)/math.sqrt(1 - math.pow(e*math.sin(p/rho),2));
    def f1(p):
        return math.log( (1 - p)/(1 + p) )
    def f2(p):
        return f1(p) - e * f1(e * p)
    def f3(p):
        return pol1*math.exp( (f2(math.sin(p/rho)) - f2sin1)*sint/2)
    rho = 45/math.atan2(1.0,1.0)
    e = math.sqrt(f * (2 - f))
    dum = f2(math.sin(lat1/rho)) - f2(math.sin(lat2/rho))
    sint = 2 * ( math.log(fx(lat1)) - math.log(fx(lat2)) ) / dum
    f2sin1 = f2(math.sin(lat1/rho))
    pol1 = fx(lat1)/sint
    polc = f3(latc) + 500000.0
    peq = a * math.cos(latc/rho)/(sint*math.exp(sint*math.log((45-latc/2)/rho)))
    pol = math.sqrt( math.pow(x-500000,2) + math.pow(polc-y,2))
    lat = 90 - 2 * rho * math.atan( math.exp( math.log( pol / peq ) / sint ) )
    lon = 0
    fact = rho * math.cos(lat / rho) / sint / pol
    fact = rho * math.cos(lat / rho) / sint / pol
    delta = 1.0
    while( math.fabs(delta) > eps ):
        delta = ( f3(lat) - pol ) * fact
        lat += delta
    lon = -(lonc + rho * math.atan( (500000 - x) / (polc - y) ) / sint)

    #return round(lat,5), round(lon,5)
    latlon = {}
    latlon['lat'] = round(lat,5)
    latlon['lon'] = round(lon,5)
    #return latlon
    printjson(latlon)

def printjson(wgs84):
    json = simplejson.dumps(wgs84)
    print json
    exit()

def num (s):
    try:
        return int(s)
    except ValueError:
        return float(s.replace(',', '.'))

if qsenv:
    x = str(qsenv['x'])
    y = str(qsenv['y'])
    isnet93_to_wgs84(num(x),num(y))

print 'Pass in a <a href="http://spatialreference.org/ref/epsg/3057/">ISNET93</a> x,y location, like this:<br /><br />'
print 'https://views.scraperwiki.com/run/isnet93_wgs84/?x=X&y=Y<br />'
print '<br />'
print 'Response is in JSON'
print '<br />'
print 'Example: <a href="https://views.scraperwiki.com/run/isnet93_wgs84/?x=357895.3&y=407970.4">https://views.scraperwiki.com/run/isnet93_wgs84/?x=357895.3&y=407970.4</a><br />'
print ' Response: {"lat": 64.14503, "lon": -21.92025} <br /><br />'
print 'Based on <a href="https://gist.github.com/585850">this code</a> by <a href="https://github.com/avar">Ævar Arnfjörð Bjarmason</a>'



# Blank Python

import os, cgi
import math
import simplejson

#qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))

qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

def isnet93_to_wgs84(xx,yy):
    x = xx;
    y = yy;
    a = 6378137.0;
    f = 1/298.257222101;
    lat1 = 64.25;
    lat2 = 65.75;
    latc = 65.00;
    lonc = 19.00;
    eps = 0.00000000001;   
    def fx(p):
        return  a * math.cos(p/rho)/math.sqrt(1 - math.pow(e*math.sin(p/rho),2));
    def f1(p):
        return math.log( (1 - p)/(1 + p) )
    def f2(p):
        return f1(p) - e * f1(e * p)
    def f3(p):
        return pol1*math.exp( (f2(math.sin(p/rho)) - f2sin1)*sint/2)
    rho = 45/math.atan2(1.0,1.0)
    e = math.sqrt(f * (2 - f))
    dum = f2(math.sin(lat1/rho)) - f2(math.sin(lat2/rho))
    sint = 2 * ( math.log(fx(lat1)) - math.log(fx(lat2)) ) / dum
    f2sin1 = f2(math.sin(lat1/rho))
    pol1 = fx(lat1)/sint
    polc = f3(latc) + 500000.0
    peq = a * math.cos(latc/rho)/(sint*math.exp(sint*math.log((45-latc/2)/rho)))
    pol = math.sqrt( math.pow(x-500000,2) + math.pow(polc-y,2))
    lat = 90 - 2 * rho * math.atan( math.exp( math.log( pol / peq ) / sint ) )
    lon = 0
    fact = rho * math.cos(lat / rho) / sint / pol
    fact = rho * math.cos(lat / rho) / sint / pol
    delta = 1.0
    while( math.fabs(delta) > eps ):
        delta = ( f3(lat) - pol ) * fact
        lat += delta
    lon = -(lonc + rho * math.atan( (500000 - x) / (polc - y) ) / sint)

    #return round(lat,5), round(lon,5)
    latlon = {}
    latlon['lat'] = round(lat,5)
    latlon['lon'] = round(lon,5)
    #return latlon
    printjson(latlon)

def printjson(wgs84):
    json = simplejson.dumps(wgs84)
    print json
    exit()

def num (s):
    try:
        return int(s)
    except ValueError:
        return float(s.replace(',', '.'))

if qsenv:
    x = str(qsenv['x'])
    y = str(qsenv['y'])
    isnet93_to_wgs84(num(x),num(y))

print 'Pass in a <a href="http://spatialreference.org/ref/epsg/3057/">ISNET93</a> x,y location, like this:<br /><br />'
print 'https://views.scraperwiki.com/run/isnet93_wgs84/?x=X&y=Y<br />'
print '<br />'
print 'Response is in JSON'
print '<br />'
print 'Example: <a href="https://views.scraperwiki.com/run/isnet93_wgs84/?x=357895.3&y=407970.4">https://views.scraperwiki.com/run/isnet93_wgs84/?x=357895.3&y=407970.4</a><br />'
print ' Response: {"lat": 64.14503, "lon": -21.92025} <br /><br />'
print 'Based on <a href="https://gist.github.com/585850">this code</a> by <a href="https://github.com/avar">Ævar Arnfjörð Bjarmason</a>'




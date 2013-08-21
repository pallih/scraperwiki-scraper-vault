import scraperwiki

# Blank Python

import suds

from suds.client import Client
url = 'http://graphical.weather.gov/xml/DWMLgen/wsdl/ndfdXML.wsdl'
client = Client(url)
print client

d = dict(listLatLon='39.965506,-77.997048 39.916268,-77.947228 39.867004,-77.897454 39.817714,-77.847728 39.768398,-77.798049 39.719057,-77.748417 39.669689,-77.698831 39.620295,-77.649293 39.570876,-77.599802 39.521430,-77.550357 39.471959,-77.500959 39.422463,-77.451608 39.372940,-77.402303 39.323393,-77.353045 39.273819,-77.303834 39.224220,-77.254669 39.174596,-77.205550 39.124946,-77.156478 39.075271,-77.107452 39.025571,-77.058473 38.975845,-77.009539', product='time-series', startTime='2012-01-01T00:00:00', endTime='2012-02-12T00:00:0', Unit='e', weatherParameters='[maxt = TRUE, mint = FALSE, temp = FALSE, dew = FALSE, appt = FALSE, pop12 = FALSE, qpf = FALSE, snow = FALSE, iceaccum = FALSE, sky = FALSE, rh = FALSE, wspd = FALSE, wdir = FALSE, wx = FALSE, icons = FALSE, waveh = FALSE, incw34 = FALSE, incw50 = FALSE, incw64 = FALSE, cumw34 = FALSE, cumw50 = FALSE, cum64 = FALSE, wgust = FALSE, critfireo = FALSE, dryfireo = FALSE, conhazo = FALSE, ptornado = FALSE, phail = FALSE, ptstmwinds = FALSE, ptotsvrtstm = FALSE, pxtosvrtstm = FALSE, tmpabv14d = FALSE, tmpblw14d = FALSE, tmpabv30d = FALSE, tmpblw30d = FALSE, tmpabv90d = FALSE, tmpblw90d = FALSE, prcabv14d = FALSE, prcpblw14d = FALSE, prcpabv30d = FALSE, prcpblw30d = FALSE, prcpabv90d = FALSE, prcablw90d = FALSE, precipa_r = FALSE, sky_r = FALSE, td_r = FALSE, temp_r = FALSE, wdir_r = FALSE, wspd_r = FALSE, wwa = FALSE]')
result = client.service.NDFDgenLatLonList(**d)
print result
#scraperwiki.sqlite.save(unique_keys=['location'], data=data)
print scraperwiki.sqlite.show_tables()
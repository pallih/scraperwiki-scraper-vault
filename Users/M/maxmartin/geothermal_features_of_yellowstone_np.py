# Geothermal Features of Yellowstone National Park
# Source (tabular data): 
#    http://en.wikipedia.org/wiki/List_of_Yellowstone_geothermal_features

# Max Martin

import scraperwiki
import urllib
import lxml.html
import string

html = scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_Yellowstone_geothermal_features")
print html

root = lxml.html.fromstring(html)

for hotspots in root.cssselect("div.id tr"):
#for hotspots in root.cssselect("th.class tr")
    tds = hotspots.cssselect("td")

    name = tds[0].cssselect("a")[0].text
    namelink = tds[0].cssselect("a")[0].attrib['href']
    location = tds[1].cssselect("a")[0].text
    loclink = tds[1].cssselect("a")[0].attrib['href']
    lat = tds[1].cssselect("a")[1].cssselect("span")[2].text
    lng = tds[1].cssselect("a")[1].cssselect("span")[3].text

#       image =

    print name
    print namelink
    print location
    print loclink
    print lat
    print lng

    data = {
        'Hotspot': name,
        'Details': namelink,
        'Basin': location,
        'Details': loclink,
        'Latitude': lat,
        'Longitude': lng,     
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)



# SCRATCH:
# Split lat/long from coords

#<td><a href="/wiki/A-0_Geyser" title="A-0 Geyser">A-0 Geyser</a></td>
#<td><a href="/wiki/Geothermal_areas_of_Yellowstone#Lower_Geyser_Basin" title="Geothermal areas of Yellowstone">Lower Geyser Basin</a><br />
#<small><span class="plainlinks nourlexpansion"><a rel="nofollow" class="external text" href="//toolserver.org/~geohack/geohack.php?pagename=List_of_Yellowstone_geothermal_features&amp;params=44.543109_N_-110.796341_E_&amp;title=A-0+Geyser"> <span class="geo-nondefault"><span class="geo-dms" title="Maps, aerial photos, and other data for this location"><span class="latitude">44°32′35″N</span> <span class="longitude">110°47′47″W</span></span></span><span class="geo-multi-punct">﻿ / ﻿</span><span class="geo-default"><span class="vcard"><span class="geo-dec" title="Maps, aerial photos, and other data for this location">44.543109°N 110.796341°W</span><span style="display:none">﻿ / <span class="geo">44.543109; -110.796341</span></span><span style="display:none">﻿ (<span class="fn org">A-0 Geyser</span>)</span></span></span></a></span></small></td>

# Geothermal Features of Yellowstone National Park
# Source (tabular data): 
#    http://en.wikipedia.org/wiki/List_of_Yellowstone_geothermal_features

# Max Martin

import scraperwiki
import urllib
import lxml.html
import string

html = scraperwiki.scrape("http://en.wikipedia.org/wiki/List_of_Yellowstone_geothermal_features")
print html

root = lxml.html.fromstring(html)

for hotspots in root.cssselect("div.id tr"):
#for hotspots in root.cssselect("th.class tr")
    tds = hotspots.cssselect("td")

    name = tds[0].cssselect("a")[0].text
    namelink = tds[0].cssselect("a")[0].attrib['href']
    location = tds[1].cssselect("a")[0].text
    loclink = tds[1].cssselect("a")[0].attrib['href']
    lat = tds[1].cssselect("a")[1].cssselect("span")[2].text
    lng = tds[1].cssselect("a")[1].cssselect("span")[3].text

#       image =

    print name
    print namelink
    print location
    print loclink
    print lat
    print lng

    data = {
        'Hotspot': name,
        'Details': namelink,
        'Basin': location,
        'Details': loclink,
        'Latitude': lat,
        'Longitude': lng,     
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)



# SCRATCH:
# Split lat/long from coords

#<td><a href="/wiki/A-0_Geyser" title="A-0 Geyser">A-0 Geyser</a></td>
#<td><a href="/wiki/Geothermal_areas_of_Yellowstone#Lower_Geyser_Basin" title="Geothermal areas of Yellowstone">Lower Geyser Basin</a><br />
#<small><span class="plainlinks nourlexpansion"><a rel="nofollow" class="external text" href="//toolserver.org/~geohack/geohack.php?pagename=List_of_Yellowstone_geothermal_features&amp;params=44.543109_N_-110.796341_E_&amp;title=A-0+Geyser"> <span class="geo-nondefault"><span class="geo-dms" title="Maps, aerial photos, and other data for this location"><span class="latitude">44°32′35″N</span> <span class="longitude">110°47′47″W</span></span></span><span class="geo-multi-punct">﻿ / ﻿</span><span class="geo-default"><span class="vcard"><span class="geo-dec" title="Maps, aerial photos, and other data for this location">44.543109°N 110.796341°W</span><span style="display:none">﻿ / <span class="geo">44.543109; -110.796341</span></span><span style="display:none">﻿ (<span class="fn org">A-0 Geyser</span>)</span></span></span></a></span></small></td>


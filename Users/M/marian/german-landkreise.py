url = 'http://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland'

from scrapemark import scrape
import scraperwiki
import urllib

data = scrape("""
{*
<tr>
<td>{{ [kreise].kreis_id}}</td>
<td><a href="" title="{{ [kreise].name }}"/></td>
<td><a href="" title="{{ [kreise].state }}"/></td>
<td><a href="" title="{{ [kreise].capital }}"/></td>
<td align="right">{{ [kreise].inhabitants }}</td>
<td align="right">{{ [kreise].area }}</td>
<td align="center">{{ [kreise].inhab_density }}</td>
</tr>
*}
""", url=url)

if data != None:
    if 'kreise' in data:
        print len(data['kreise']), "items found"
        print data['kreise']
        for k in data['kreise']:
            k['inhabitants'] = int(k['inhabitants'].replace('.', ''))
            k['inhab_density'] = int(k['inhab_density'])
            k['area'] = k['area'].replace(',', '.')
            scraperwiki.sqlite.save(unique_keys=["kreis_id"], data=k)url = 'http://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland'

from scrapemark import scrape
import scraperwiki
import urllib

data = scrape("""
{*
<tr>
<td>{{ [kreise].kreis_id}}</td>
<td><a href="" title="{{ [kreise].name }}"/></td>
<td><a href="" title="{{ [kreise].state }}"/></td>
<td><a href="" title="{{ [kreise].capital }}"/></td>
<td align="right">{{ [kreise].inhabitants }}</td>
<td align="right">{{ [kreise].area }}</td>
<td align="center">{{ [kreise].inhab_density }}</td>
</tr>
*}
""", url=url)

if data != None:
    if 'kreise' in data:
        print len(data['kreise']), "items found"
        print data['kreise']
        for k in data['kreise']:
            k['inhabitants'] = int(k['inhabitants'].replace('.', ''))
            k['inhab_density'] = int(k['inhab_density'])
            k['area'] = k['area'].replace(',', '.')
            scraperwiki.sqlite.save(unique_keys=["kreis_id"], data=k)url = 'http://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland'

from scrapemark import scrape
import scraperwiki
import urllib

data = scrape("""
{*
<tr>
<td>{{ [kreise].kreis_id}}</td>
<td><a href="" title="{{ [kreise].name }}"/></td>
<td><a href="" title="{{ [kreise].state }}"/></td>
<td><a href="" title="{{ [kreise].capital }}"/></td>
<td align="right">{{ [kreise].inhabitants }}</td>
<td align="right">{{ [kreise].area }}</td>
<td align="center">{{ [kreise].inhab_density }}</td>
</tr>
*}
""", url=url)

if data != None:
    if 'kreise' in data:
        print len(data['kreise']), "items found"
        print data['kreise']
        for k in data['kreise']:
            k['inhabitants'] = int(k['inhabitants'].replace('.', ''))
            k['inhab_density'] = int(k['inhab_density'])
            k['area'] = k['area'].replace(',', '.')
            scraperwiki.sqlite.save(unique_keys=["kreis_id"], data=k)
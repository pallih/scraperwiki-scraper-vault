from __future__ import unicode_literals
import scraperwiki
import lxml.html
import dateutil.parser

# scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`datum` text, `suppe` text, `hauptspeise1` text, `hauptspeise2` text, `hauptspeise3` text, `indisch` text, `dessert1` text, `dessert2` text)")

html = scraperwiki.scrape('http://restaurant-ginko.at/menueplan/')
root = lxml.html.fromstring(html.decode('utf-8'))

for daily_menu in root.cssselect('div.menu div.inner'):
    menu_items = {}
    menu_items['datum'] = dateutil.parser.parse(daily_menu.find('p[@class="date"]').text, dayfirst=True).date()
    
    menu_items_element = daily_menu.find('pre')
    if menu_items_element is not None:
        menu_items_string = lxml.html.tostring(menu_items_element, encoding=unicode)
        menu_items_raw = menu_items_string.replace('<pre>', '').replace('</pre>', '').split('<br>')

        counter = 0
        for menu_item in menu_items_raw:
            counter += 1
            menu_item = menu_item.strip()
            
            if counter == 1:
                menu_items['suppe'] = menu_item
            elif counter == 2:
                menu_items['hauptspeise1'] = menu_item
            elif counter == 3:
                menu_items['hauptspeise2'] = menu_item
            elif counter == 4:
                menu_items['hauptspeise3'] = menu_item
            elif 'INDISCH: ' in menu_item:
                menu_items['indisch'] = menu_item.replace('INDISCH: ', '')
            elif counter == 6 and 'DESSERT: ' not in menu_item:
                menu_items['indisch'] += ' ' + menu_item
            elif 'DESSERT: ' in menu_item:
                desserts = menu_item.split(', ')
                menu_items['dessert1'] = desserts[0].replace('DESSERT: ', '')
                menu_items['dessert2'] = desserts[1]

        scraperwiki.sqlite.save(unique_keys=['datum'], data=menu_items)
from __future__ import unicode_literals
import scraperwiki
import lxml.html
import dateutil.parser

# scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`datum` text, `suppe` text, `hauptspeise1` text, `hauptspeise2` text, `hauptspeise3` text, `indisch` text, `dessert1` text, `dessert2` text)")

html = scraperwiki.scrape('http://restaurant-ginko.at/menueplan/')
root = lxml.html.fromstring(html.decode('utf-8'))

for daily_menu in root.cssselect('div.menu div.inner'):
    menu_items = {}
    menu_items['datum'] = dateutil.parser.parse(daily_menu.find('p[@class="date"]').text, dayfirst=True).date()
    
    menu_items_element = daily_menu.find('pre')
    if menu_items_element is not None:
        menu_items_string = lxml.html.tostring(menu_items_element, encoding=unicode)
        menu_items_raw = menu_items_string.replace('<pre>', '').replace('</pre>', '').split('<br>')

        counter = 0
        for menu_item in menu_items_raw:
            counter += 1
            menu_item = menu_item.strip()
            
            if counter == 1:
                menu_items['suppe'] = menu_item
            elif counter == 2:
                menu_items['hauptspeise1'] = menu_item
            elif counter == 3:
                menu_items['hauptspeise2'] = menu_item
            elif counter == 4:
                menu_items['hauptspeise3'] = menu_item
            elif 'INDISCH: ' in menu_item:
                menu_items['indisch'] = menu_item.replace('INDISCH: ', '')
            elif counter == 6 and 'DESSERT: ' not in menu_item:
                menu_items['indisch'] += ' ' + menu_item
            elif 'DESSERT: ' in menu_item:
                desserts = menu_item.split(', ')
                menu_items['dessert1'] = desserts[0].replace('DESSERT: ', '')
                menu_items['dessert2'] = desserts[1]

        scraperwiki.sqlite.save(unique_keys=['datum'], data=menu_items)

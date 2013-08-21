# -*- coding: utf8 -*-
import scraperwiki
import lxml.html
import re
from datetime import *

EVENTS_PER_PAGE = 10

# Open main page          
html = scraperwiki.scrape("http://www.csn.es/index.php?option=com_content&view=category&layout=blog&id=47&Itemid=120&lang=es")
root = lxml.html.fromstring(html)

# Get total number of events and number of pages, and save them as vars
p_counter = root.cssselect("p[class='counter']")

chunks = p_counter[0].text_content().split()
total_events = int(chunks[1])
pages = int(chunks[5])

scraperwiki.sqlite.save_var('pages', pages)
scraperwiki.sqlite.save_var('total_events', total_events)

limitstart = 0
n_events = 0
i_pages = 0

# Where to start ids?
id = 1
try:
    last_id = scraperwiki.sqlite.execute("select count(*) from swdata")
    id = last_id + 1
except Exception, e:
    id = 1

# Loop page by page
while n_events < total_events:

    # Get all the events of the page
    events = root.cssselect("div[class='article_column column1 cols1']")

    # Loop event by event in this page
    for event in events:
        
        # Extract 'where' and 'when'
        location_elements = event.findall('h3')
        location_element = location_elements[0]
        location = location_element.text_content()
    
        date_elements = event.find_class('iteminfo')
        date_element = date_elements[0]
        date_str = date_element.text_content()

        # Some interesting indices in the location string
        first_par = location.find("(")
        last_par = location.find(")")
        ines_pos = location.find("INES")

        # By default, name is all string
        name = location

        # Split 'where' in name of the central and city
        if first_par == -1 or last_par == -1:
            city = 'UNKNOWN'
        else:
            city = location[first_par+1:last_par]
            name = location[0:first_par - 1]
        
        # Extract INES level
        
        if ines_pos == -1:
            ines_level = -1
        else:
            if name == location:
                name = location[0: ines_pos - 1]

            l = len(location)
            try:
                # Takes from end on 'INES' to end of the string, getting rid of all non numeric characters
                ines_level = int(re.sub(r"\D", "", location[ines_pos + 5: l]))
            except ValueError, e:
                ines_level = -1


        # This is ugly, but we don't have es_ES locale installed here...
        date_str = date_str.title().replace("Lunes", "Monday")
        date_str = date_str.title().replace("Martes", "Tuesday")
        date_str = date_str.title().replace(u"Miércoles", "Wednesday").replace("Miercoles", "Wednesday")
        date_str = date_str.title().replace("Jueves", "Thursday")
        date_str = date_str.title().replace("Viernes", "Friday")
        date_str = date_str.title().replace(u"Sábado", "Saturday").replace("Sabado", "Saturday")
        date_str = date_str.title().replace("Domingo", "Sunday")

        date_str = date_str.title().replace("Enero", "January")
        date_str = date_str.title().replace("Febrero", "February")
        date_str = date_str.title().replace("Marzo", "March")
        date_str = date_str.title().replace("Abril", "April")
        date_str = date_str.title().replace("Mayo", "May")
        date_str = date_str.title().replace("Junio", "June")
        date_str = date_str.title().replace("Julio", "July")
        date_str = date_str.title().replace("Agosto", "August")
        date_str = date_str.title().replace("Septiembre", "September")
        date_str = date_str.title().replace("Octubre", "October")
        date_str = date_str.title().replace("Noviembre", "November")
        date_str = date_str.title().replace("Diciembre", "December")

        # Sanitize date string
        date_str = re.sub(r"[\t\n\r\f\v]", "", date_str)

        # Construct time object
        try:
            date = datetime.strptime(date_str, "%A, %d %B %Y").date()
        except ValueError, e:
            print e
            date = datetime(MAXYEAR, 1, 1).date()
        
    
        # Quick clean
        name = re.sub(" - Nivel", "", name)
        name = re.sub(" - No aplicable", "", name)


        # Extract info
        info_txt = ''
        
        #for element in event.iter():
        #    matches=re.findall(r'\"(.+?)\"',element.text_content())
        #    info_txt = info_txt + ".".join(matches)


        info_elements = event.cssselect("[style='text-align: justify;']")
        for info_element in info_elements:
            info_txt = info_txt + '. ' + info_element.text_content()


        info_txt = re.sub("^.", "", info_txt)

        data = {
            'event_id': id,
            'event_location': name,
            'event_city': city,
            'event_date': date,
            'event_ines_level': ines_level,
            'event_info': info_txt
        }

        id = id + 1

        # Save entry
        scraperwiki.sqlite.save(['event_id'], data = data)

    n_events = n_events + len(events)
    limitstart = limitstart + EVENTS_PER_PAGE

    # Read the next page
    html = scraperwiki.scrape("http://www.csn.es/index.php?option=com_content&view=category&layout=blog&id=47&Itemid=120&lang=es&limitstart=%d" % limitstart)
    root = lxml.html.fromstring(html)
    
    


# -*- coding: utf8 -*-
import scraperwiki
import lxml.html
import re
from datetime import *

BASE_URL = "http://www.filmaffinity.com"
date = datetime(MAXYEAR, 1, 1).date()
movie_counter = 0

# Step 0: Delete the data, to a clean insertion
scraperwiki.sqlite.execute("delete from swdata")
scraperwiki.sqlite.commit()


# Step 1: Get movie releases by date (filmaffinity)
html = scraperwiki.scrape("http://www.filmaffinity.com/es/rdcat.php?id=upc_th_es")
root = lxml.html.fromstring(html)

table = root.xpath("/html//table")

# The inner table
content_table = table[1]
rows = content_table.findall("tr")

# Step 2: loop the content table, to get the release dates and the movies
# The table has several rows. Each row has only one column. Each column contains either:
#  - The release date (div class rdate-cat)
#  - A link plus some content for a movie released that date (div class padding-list)
for row in rows:

    cols = row.findall("td")
    for col in cols:
        first_release_date = row.cssselect("div[class='rdate-cat rdate-cat-first']")
        release_date = row.cssselect("div[class='rdate-cat']")
        content = row.cssselect("div[class='padding-list']")
        
        # Is this the date column?
        if first_release_date or release_date:

            if release_date:
                first_release_date = None
            else:
                release_date = first_release_date

            date_str = release_date[0].text_content()
    
            date_str = date_str.title().replace("De", "")
        
            # This is ugly, but we don't have es_ES locale installed here...
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
                date = datetime.strptime(date_str, "%d %B %Y").date()
            except ValueError, e:
                print e
                continue

        # Is this the content column?
        elif content:
            div_info = content[0].cssselect("div[class='mc-info-container']")
            div_title = div_info[0].cssselect("div[class='mc-title']")
            title_and_year = div_title[0].text_content()

            # Sanitize
            title_and_year = re.sub(r"[\t\n\r\f\v]", "", title_and_year)

            # Split title_and_year in title and year, separated
            first_par = title_and_year.rfind("(")
            last_par = title_and_year.rfind(")")
            if first_par == -1 or last_par == -1:
                year = 9999
            else:
                try:
                    year = int(title_and_year[first_par+1:last_par])
                except ValueError, e:
                    year = 9999

            title = title_and_year[:first_par]

            # Get link to movie page
            movie_link = ""
            movie_id = ""
            #div_info[0].make_links_absolute(base_url="http://www.filmaffinity.com/es/")
            for (element, attribute, link, pos) in div_info[0].iterlinks():
                #link = re.sub(r"[\t\n\r\f\v]", "", link)
                if link.startswith("/es/film"):
                    movie_link = BASE_URL + link
                    break

            pos1 = movie_link.rfind("film") + 4
            pos2 = movie_link.rfind(".html")
            movie_id = movie_link[pos1:pos2]
            
            
            
            data = {
                'movie_id': movie_id,
                'movie_title' : title,
                'movie_year' : year,
                'movie_release_date' : date,
                'movie_info_page': movie_link
            }
            # Save entry
            scraperwiki.sqlite.save(['movie_id'], data = data)

            movie_counter = movie_counter + 1

            #print "Movie title: %s" % title
            #print "Movie year: %d" % year
            #print "Movie release date: %s" % date
            #print "Movie id: %s" % movie_id
            #print "Movie page link: %s" % movie_link

        else:
            continue 

scraperwiki.sqlite.save_var('movie_counter', movie_counter)



# Query to find a movie by title in imdb
#html = scraperwiki.scrape("http://www.imdb.com/find?q=combustion&s=tt&exact=true&ref_=fn_tt_ex")
#print html

# In the result html, we should look for table of class findList

# -*- coding: utf8 -*-
import scraperwiki
import lxml.html
import re
from datetime import *

BASE_URL = "http://www.filmaffinity.com"
date = datetime(MAXYEAR, 1, 1).date()
movie_counter = 0

# Step 0: Delete the data, to a clean insertion
scraperwiki.sqlite.execute("delete from swdata")
scraperwiki.sqlite.commit()


# Step 1: Get movie releases by date (filmaffinity)
html = scraperwiki.scrape("http://www.filmaffinity.com/es/rdcat.php?id=upc_th_es")
root = lxml.html.fromstring(html)

table = root.xpath("/html//table")

# The inner table
content_table = table[1]
rows = content_table.findall("tr")

# Step 2: loop the content table, to get the release dates and the movies
# The table has several rows. Each row has only one column. Each column contains either:
#  - The release date (div class rdate-cat)
#  - A link plus some content for a movie released that date (div class padding-list)
for row in rows:

    cols = row.findall("td")
    for col in cols:
        first_release_date = row.cssselect("div[class='rdate-cat rdate-cat-first']")
        release_date = row.cssselect("div[class='rdate-cat']")
        content = row.cssselect("div[class='padding-list']")
        
        # Is this the date column?
        if first_release_date or release_date:

            if release_date:
                first_release_date = None
            else:
                release_date = first_release_date

            date_str = release_date[0].text_content()
    
            date_str = date_str.title().replace("De", "")
        
            # This is ugly, but we don't have es_ES locale installed here...
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
                date = datetime.strptime(date_str, "%d %B %Y").date()
            except ValueError, e:
                print e
                continue

        # Is this the content column?
        elif content:
            div_info = content[0].cssselect("div[class='mc-info-container']")
            div_title = div_info[0].cssselect("div[class='mc-title']")
            title_and_year = div_title[0].text_content()

            # Sanitize
            title_and_year = re.sub(r"[\t\n\r\f\v]", "", title_and_year)

            # Split title_and_year in title and year, separated
            first_par = title_and_year.rfind("(")
            last_par = title_and_year.rfind(")")
            if first_par == -1 or last_par == -1:
                year = 9999
            else:
                try:
                    year = int(title_and_year[first_par+1:last_par])
                except ValueError, e:
                    year = 9999

            title = title_and_year[:first_par]

            # Get link to movie page
            movie_link = ""
            movie_id = ""
            #div_info[0].make_links_absolute(base_url="http://www.filmaffinity.com/es/")
            for (element, attribute, link, pos) in div_info[0].iterlinks():
                #link = re.sub(r"[\t\n\r\f\v]", "", link)
                if link.startswith("/es/film"):
                    movie_link = BASE_URL + link
                    break

            pos1 = movie_link.rfind("film") + 4
            pos2 = movie_link.rfind(".html")
            movie_id = movie_link[pos1:pos2]
            
            
            
            data = {
                'movie_id': movie_id,
                'movie_title' : title,
                'movie_year' : year,
                'movie_release_date' : date,
                'movie_info_page': movie_link
            }
            # Save entry
            scraperwiki.sqlite.save(['movie_id'], data = data)

            movie_counter = movie_counter + 1

            #print "Movie title: %s" % title
            #print "Movie year: %d" % year
            #print "Movie release date: %s" % date
            #print "Movie id: %s" % movie_id
            #print "Movie page link: %s" % movie_link

        else:
            continue 

scraperwiki.sqlite.save_var('movie_counter', movie_counter)



# Query to find a movie by title in imdb
#html = scraperwiki.scrape("http://www.imdb.com/find?q=combustion&s=tt&exact=true&ref_=fn_tt_ex")
#print html

# In the result html, we should look for table of class findList


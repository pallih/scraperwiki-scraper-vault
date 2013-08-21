# -*- coding: utf8 -*-
import scraperwiki
import lxml.html
import json
import urllib

IMDB_API_URL = 'http://www.omdbapi.com/?'

# Step 0: Delete the data, to a clean insertion
scraperwiki.sqlite.execute("delete from swdata")
scraperwiki.sqlite.commit()


# Get movies actually running in Spain from other scraper
scraperwiki.sqlite.attach("movie_releases_spain")
movie_listing = scraperwiki.sqlite.select("* from movie_releases_spain.swdata order by movie_release_date desc")

movie_counter = 0


# For each movie, get the link to filmaffinity movie page, and scrap it
for movie_dict in movie_listing:

    movie_original_title = ""
    movie_runtime = ""
    movie_country = ""
    movie_fa_rating = "N/A"
    movie_imdb_rating = "N/A"
    movie_plot = ""
    movie_poster_link = ""
    movie_official_web = ""
        
    data = {}
                
    for key, value in movie_dict.items():

        data[key] = value
        
        # Scrap time!
        if key == 'movie_info_page':
            html = scraperwiki.scrape(value)
            root = lxml.html.fromstring(html)

            
            # Get movie items for movie info page

            movie_info_el = root.cssselect("dl[class='movie-info']")
            movie_items = movie_info_el[0].findall("dd")

            # The pic
            for (element, attribute, link, pos) in root.iterlinks():
                if "large" in link:
                    movie_poster_link = link

            # The rating
            rating_div = root.cssselect("div[id='movie-rat-avg']")
            if rating_div:
                movie_fa_rating = rating_div[0].text_content().strip()

            for movie_item in movie_items:
                
                if movie_item.getprevious().text_content() == u"Título original":
                    movie_original_title = movie_item.text_content().strip()
                
                elif movie_item.getprevious().text_content() == u"Duración":
                    movie_runtime = movie_item.text_content().strip()

                elif movie_item.getprevious().text_content() == u"País":
                    movie_country = movie_item.text_content().strip()

                elif movie_item.getprevious().text_content() == "Web Oficial":
                    movie_official_web = movie_item.text_content().strip()

                elif movie_item.getprevious().text_content() == "Sinopsis":
                    movie_plot = movie_item.text_content().strip()


            # The imdb rating
            query_parameters = {'t' : movie_original_title.encode('utf-8')}
            response = urllib.urlopen(IMDB_API_URL + urllib.urlencode(query_parameters))
            data_imdb = json.load(response)
            
            if data_imdb['Response'].title() == 'True':   
                movie_imdb_rating = data_imdb['imdbRating']


        # Complete data
        data['movie_original_title'] = movie_original_title
        data['movie_runtime'] = movie_runtime
        data['movie_country'] = movie_country
        data['movie_poster_link'] = movie_poster_link
        data['movie_fa_rating'] = movie_fa_rating
        data['movie_imdb_rating'] = movie_imdb_rating
        data['movie_official_web'] = movie_official_web
        data['movie_plot'] = movie_plot 

    #print data

    # Save entry
    scraperwiki.sqlite.save(['movie_id'], data = data)
    movie_counter = movie_counter + 1      

scraperwiki.sqlite.save_var('movie_counter', movie_counter)    
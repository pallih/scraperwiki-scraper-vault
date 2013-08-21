import scraperwiki
import lxml.html
import re
from geopy import geocoders
import sys
import datetime


BASIS = 'http://www.kino.de'
START = '/kinoprogramm/'
ENCODING = 'UTF-8'

page = "null"

def parseCinemas(url, city):
    
    root = lxml.html.parse(url).getroot()

    if root is None:
        print "--> Nothing found in " + city + " [" + url + "]"
        return

    try:
        tmpPage = root.cssselect('div.innerPager a.active')[0]
        global page
        if page == tmpPage.text:
            return
    except:
        print "First Page for " + city


    lst = root.cssselect('ul.cinema-city-list > li')
    if lst is None:
        print "--> Nothing found in " + city + " [" + url + "]"
        return
    print "###### " + city + " ######"
    
    for cinema_elem in lst :
        cinema = {}
        movies = []
        elem_link = cinema_elem.cssselect('div.clearfix div.left a')[0]
        cinema["name"] = elem_link.cssselect('strong')[0].text
        try:
            cinema["url"] = BASIS + elem_link.attrib['href']
        except:
            print "Can't get link for cinema [" + cinema["name"] + "]"
            
        cinema["date_scraped"] = datetime.datetime.today()
        split_content = cinema_elem.text_content().strip().split("\n");

        address = cinema_elem.cssselect('div.clearfix div.left')[0].text_content().split('\n')[6].strip()
        if address == "":
            address = cinema_elem.cssselect('div.clearfix div.left')[0].text_content().split('\n')[7].strip()
        cinema["address"] = address
        cinema["city"] = city
        try:
            g = geocoders.Google(domain='maps.google.de')
            x, (cinema["lat"], cinema["lon"]) = g.geocode(address)
            print cinema["name"] + " - (lat, lon): %.5f, %5f" % (cinema["lat"], cinema["lon"])
        except Exception:
            print "-> Cinema [" + cinema["name"] + ", " + address + "] skipped. Can't get geodata..."
        
        for movie_elem in cinema_elem.cssselect('ul.cinema-movie-list'):
            movie = {}
            try:
                movie["title"] = movie_elem.cssselect('li div.movie-title a')[0].text
                try:
                    movie["url"] = BASIS + movie_elem.cssselect('li div.movie-title a')[0].attrib['href']
                except IndexError:
                    print "Can't get link for movie [" + movie["title"] + "]"
            except IndexError:
                movie["title"] = movie_elem.cssselect('li div.movie-title')[0].text_content().strip()

            

            movie["time"] =  movie_elem.cssselect('li div.movie-showtimes')[0].text_content()
            movies.append(movie)
        
        cinema["movies"] = movies
        scraperwiki.sqlite.save(unique_keys=["name"], data=cinema, verbose=2)
        
    try:
        tmpPage = root.cssselect('div.innerPager a.active')[0]
        nextPage = root.cssselect('div#boxcinemacitytabscity-list a.arrow-forward')[0]
        page = tmpPage.text
        print "Next page for " + city
        parseCinemas(BASIS + nextPage.attrib['href'], city)
    except IndexError:
        print "No more pages for " + city
        return

def main():
    #parseCinemas('http://www.kino.de/kinoprogramm/billerbeck/', 'Billerbeck')
    root = lxml.html.parse(BASIS + START).getroot()
    for cityElem in root.cssselect('div#boxcinemaprogrammallcities div.columns-3 ul li > a'):
        global page
        page = 0
        parseCinemas(BASIS + cityElem.attrib['href'], cityElem.text.strip())
    

main()

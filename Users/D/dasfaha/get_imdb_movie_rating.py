import lxml.html
import scraperwiki

#Ge the data
html = scraperwiki.scrape("http://www.imdb.com/title/tt2103264/")

#The request to IMDB returns plain text so the line below processes this text and turns it into a format that can be queried
root = lxml.html.fromstring(html)


#The rating of a movie is within a div with class: "titlePageSprite star-box-giga-star" like this:
#
#<div class="titlePageSprite star-box-giga-star">
#    7.7
#</div>
#

#Use CSS selector to get the div html element that has class="titlePageSprite"
el = root.cssselect("div.titlePageSprite")

#el is a list as there could be several div elements with the same class. In our case we know there is only one div with that class
print "Number of elements in el: {0}".format(len(el))


#Create a python 'dictionary' to store the two fields of the data we just scraped: 'movie title' and 'rating'
data = {
    'movie title': 'Emperor', #exercise: is it possible to scrape the movie name from the page? :p
    'rating' : el[0].text
}

print "Movie rating: {0}".format(data['rating']) #The fields in 'data' can be accessed by their names

#Save into a databaase. Completely pointless in this case but useful if the data changes...
scraperwiki.sqlite.save(unique_keys=['movie title'], data=data)
import lxml.html
import scraperwiki

#Ge the data
html = scraperwiki.scrape("http://www.imdb.com/title/tt2103264/")

#The request to IMDB returns plain text so the line below processes this text and turns it into a format that can be queried
root = lxml.html.fromstring(html)


#The rating of a movie is within a div with class: "titlePageSprite star-box-giga-star" like this:
#
#<div class="titlePageSprite star-box-giga-star">
#    7.7
#</div>
#

#Use CSS selector to get the div html element that has class="titlePageSprite"
el = root.cssselect("div.titlePageSprite")

#el is a list as there could be several div elements with the same class. In our case we know there is only one div with that class
print "Number of elements in el: {0}".format(len(el))


#Create a python 'dictionary' to store the two fields of the data we just scraped: 'movie title' and 'rating'
data = {
    'movie title': 'Emperor', #exercise: is it possible to scrape the movie name from the page? :p
    'rating' : el[0].text
}

print "Movie rating: {0}".format(data['rating']) #The fields in 'data' can be accessed by their names

#Save into a databaase. Completely pointless in this case but useful if the data changes...
scraperwiki.sqlite.save(unique_keys=['movie title'], data=data)

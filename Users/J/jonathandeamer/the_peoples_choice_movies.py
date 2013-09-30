sourcescraper = 'rotten_tomatoes_movies'

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select(           
    '''* from rotten_tomatoes_movies.swdata
    where audience_score - critics_score >= 20
    and critics_score > 0
    order by audience_score - critics_score desc limit 100'''
)

count = scraperwiki.sqlite.select(           
    '''count(id) from rotten_tomatoes_movies.swdata'''
)

print "<h3>Of " + str(count[0]['count(id)']) + " films scraped from <a href='http://rottentomatoes.com'>Rotten Tomatoes</a>, the most under-rated by critics are:</h3>"
print "<OL>"

for each in data:
    print "<LI>'" + each['title'] + "' (" + str(each['year']) + ") was rated " + str(each['critics_score']) + " by critics but audiences gave it " + str(each['audience_score']) + ".</LI>"

print "</OL>"sourcescraper = 'rotten_tomatoes_movies'

import scraperwiki           
scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select(           
    '''* from rotten_tomatoes_movies.swdata
    where audience_score - critics_score >= 20
    and critics_score > 0
    order by audience_score - critics_score desc limit 100'''
)

count = scraperwiki.sqlite.select(           
    '''count(id) from rotten_tomatoes_movies.swdata'''
)

print "<h3>Of " + str(count[0]['count(id)']) + " films scraped from <a href='http://rottentomatoes.com'>Rotten Tomatoes</a>, the most under-rated by critics are:</h3>"
print "<OL>"

for each in data:
    print "<LI>'" + each['title'] + "' (" + str(each['year']) + ") was rated " + str(each['critics_score']) + " by critics but audiences gave it " + str(each['audience_score']) + ".</LI>"

print "</OL>"
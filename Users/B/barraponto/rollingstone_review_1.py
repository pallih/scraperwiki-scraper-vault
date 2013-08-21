import scraperwiki
import lxml.html 

# Blank Python
html = scraperwiki.scrape("http://www.rollingstone.com/music/albumreviews/the-great-escape-artist-20111018")

root = lxml.html.fromstring(html)

data = {
    'artist': root.cssselect('[itemtype="http://schema.org/MusicGroup"] [itemprop="name"]')[0].text_content(),
    'album': root.cssselect('[itemtype="http://schema.org/MusicAlbum"] [itemprop="name"]')[1].text_content(),
    'publisher': root.cssselect('[itemtype="http://schema.org/MusicAlbum"] [itemprop="publisher"]')[0].text_content(),
    'thumbnail': root.cssselect('[itemtype="http://schema.org/MusicAlbum"] img')[0].get('src'),
    'rating': root.cssselect('[itemtype="http://schema.org/AggregateRating"] [itemprop="ratingValue"]')[0].text_content(),
    'max-rating': root.cssselect('[itemtype="http://schema.org/AggregateRating"] [itemprop="bestRating"]')[0].text_content(),
    'review': {
        'author':root.cssselect('[itemtype="http://schema.org/Review"] [itemprop="author"]')[0].text_content(),
        'date': root.cssselect('[itemtype="http://schema.org/Review"] [itemprop="publishDate"]')[0].text_content()
    } 
   

}

print data


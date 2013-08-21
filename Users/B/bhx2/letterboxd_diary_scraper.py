import scraperwiki
import lxml.html

username = "bhx2"

url = scraperwiki.scrape("http://letterboxd.com/" + username +  "/films/diary/")
root = lxml.html.fromstring(url)

for film_page in root.cssselect("h3.film-title a"):

    relative_link = film_page.get("href")

    sub_url = scraperwiki.scrape("http://letterboxd.com" + relative_link)
    sub_root = lxml.html.fromstring(sub_url)
    
    title_link = sub_root.cssselect("span.film-title-wrapper a")[0]
    title = title_link.text
    link = "http://letterboxd.com" + title_link.get("href")
    year = sub_root.cssselect("small a")[0].text
    rating = sub_root.cssselect("span.rating meta")[0].get("content")
    poster = sub_root.cssselect("div.poster img")[0].get("src")
    
    if len(sub_root.cssselect("div.review div p")) > 0:
        review = sub_root.cssselect("div.review div p")[0].text
    else:
        review = ""

    scraperwiki.sqlite.save(unique_keys=["title"], data={"title":title, "year":year, "link":link, "rating":rating, "poster":poster, "review":review})
    


import scraperwiki
from bs4 import BeautifulSoup
# Blank Python

url = "http://catphotos.org/" # loading your url from the csv/database
html = scraperwiki.scrape(url) # download the html content of the page
soup = BeautifulSoup(html) # load the html into beautifulsoup

images = [] # start with an empty list
for imgtag in soup.find_all('img'): # for each <img>...
    images.append(imgtag['src']) # put the URL of that image, the src attribute, into the list
scraperwiki.sqlite.save(unique_keys=["url"], data={"url": url, "images": images}) # save the list of images under the url of the whole page
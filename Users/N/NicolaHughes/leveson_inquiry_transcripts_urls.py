import scraperwiki
from bs4 import BeautifulSoup
import time

def local_scrape(url):
    # To work around leveson side always returning 404.
    import urllib2
    
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    
    return contents

stem = "http://www.levesoninquiry.org.uk"

main_url = "http://www.levesoninquiry.org.uk/evidence/"
main_html = local_scrape(main_url)
main_soup = BeautifulSoup(main_html)

links= []

info = main_soup.find("div", "sidebar")

list_of_links = info.find_all("a")
for a in list_of_links:
    link = stem + a['href']
    links.append(link)
    
for url in links:
    time.sleep(0.5) # sleep for half a second
    #print url
    try:
        html = local_scrape(url)
    except:
        print 'FAILED ' + url
        continue
    soup = BeautifulSoup(html)
    table = soup.find("table", "wide golden-one-two")
    if table:
        list_links = table.find_all("a")
        for a in list_links:
            branch = a["href"]
            if ".txt" in branch and branch != "/wp-content/uploads/2012/03/Transcript-of-Morning-Hearing-20-March.txt":
                final_link = stem + branch
                print final_link
                html = local_scrape(final_link)
                transcription = html.decode('utf-8', 'ignore')
                print transcription
                data = {"Page": url, "URL": final_link, "Transcription": transcription}
                scraperwiki.sqlite.save(["URL"], data)
    



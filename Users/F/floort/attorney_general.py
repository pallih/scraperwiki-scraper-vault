import scraperwiki
from BeautifulSoup import BeautifulSoup


page = BeautifulSoup(scraperwiki.scrape("http://www.attorneygeneral.gov.uk/NewsCentre/Speeches/Pages/default.aspx"))
for speech in page.find("div", {"class":"cc-wpInner"}).findAll("li"):
    date = speech.find("strong").text
    url = speech.find("a")["href"]
    title = speech.find("a").text
    if title[:16] == "Attorney General":
        name = "The Rt Hon Dominic Grieve QC MP"
        title = title[17:].strip()
    elif title[:17] == "Solicitor General":
        name = "Edward Garnier QC MP"
        title = title[18:].strip()
    else:
        name = "?"
    speech_page = BeautifulSoup(scraperwiki.scrape(url))
    text =  speech_page.find("div", {"id": "contentMain"}).text
    scraperwiki.sqlite.save(["permalink"], {
        "permalink": url,
        "body": text,
        "given_on": date,
        "minister_name": name,
        "title": title,
        "department": "Attorney General's Office",
    })
    
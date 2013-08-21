import lxml.html
import datetime
import scraperwiki

today = (datetime.datetime.now() + datetime.timedelta(hours=4)).date()

url = "http://www.dubaicityguide.com/site/entertainment/movies.asp"
root = lxml.html.parse(url).getroot()
table = root.cssselect("div#container div#container_left div#content_area div#double_area table")[1]
lastUpdated = table.cssselect("tr td strong")[0].text[10:50]
print lastUpdated
for row in table:
    if row.attrib != {}:
        cells = row.getchildren()
        dataCinema = cells[0].text
        dataMovie = cells[1].cssselect("a")[0].text
        dataTime = cells[2].text
        dataAll = {"Cinema": dataCinema, "Movie": dataMovie, "Time": dataTime, "City": "Dubai", "Date": today, "Source": "dubaiCityGuide"}
        scraperwiki.sqlite.save(unique_keys=["Cinema", "Movie", "Source"], data=dataAll, table_name= "CinemaDubai")


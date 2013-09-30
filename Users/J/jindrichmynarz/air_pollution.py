####################################
# Informace o kvalitě ovzduší v ČR #
####################################

import datetime, re, scraperwiki, urlparse
from BeautifulSoup import BeautifulSoup

def getEvaluation(node):
    evaluation = re.match(
        "\d+(\.\d+)?",
        node.find("span").text.encode("utf8").replace(",", ".").replace(" ", "")
    )
    if evaluation:
        evaluation = evaluation.group()
    else:
        style = node["style"]
        if style == "background-color: white":
            evaluation = "Neúplná data"
        elif style == "background-color: #CFCFCF":
            evaluation = "Veličina se na uvedené stanici neměří"
        else:
            evaluation = ""
    return evaluation

def reformatDate(text):
    match = re.match(
        "(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s+(?P<hours>\d{2}):(?P<minutes>\d{2})",
        text
    )
    date = "{0[0]}-{0[1]}-{0[2]}T{0[3]}:{0[4]}:00+01:00".format(
        map(match.group, ["year", "month", "day", "hours", "minutes"])
    )
    return date

def reformatCoords(text):
    latitude, longitude = text.encode("utf-8").replace(" sš ", "N\n").replace(" vd", "E").replace("°", "").replace("´", "'").split("\n")
    return latitude, longitude

def scrapeWeatherStation(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    tds = soup.find("table").findAll("td")
    altitude = re.match("\d+", tds[-1].text).group()
    latitude, longitude = reformatCoords(tds[-3].text)
    return latitude, longitude, altitude

# Vytvoření záhlaví ukládaných dat
scraperwiki.sqlite.save_var(
    "data_columns",
    [
        "code", "name", "owner",
        "province", # Kraj
        "latitude", "longitude", "altitude",
        "time", "airquality", "SO2_1h",
        "NO2_1h", "CO_1h", "O3_1h", "PM10_1h",
        "PM10_24h"
    ]
)

# Získání stránky
startingUrl = "http://portal.chmi.cz/files/portal/docs/uoco/web_generator/actual_hour_data_CZ.html"
html = scraperwiki.scrape(startingUrl)
soup = BeautifulSoup(html)

# Najdi první tabulku
table = soup.find("table")
trs = table.findAll("tr")

for tr in trs:
    ths = tr.findAll("th")
    tds = tr.findAll("td")
    rowSignature = (len(tds), len(ths))
    if rowSignature == (0, 9):
        th = tr.find("th")
        province = th.text.replace("Kraj: ", "")
        th = th.findNext().text
        date = reformatDate(th)
    elif rowSignature == (0, 10):
        pass
    elif rowSignature == (10, 1):
        pass
    elif rowSignature == (11, 0):
        td = tr.find("td")
        identifier = td.find("a")
        code = identifier.text
        weatherStationUrl = urlparse.urljoin(startingUrl, identifier["href"])
        latitude, longitude, altitude = scrapeWeatherStation(weatherStationUrl)
        td = td.findNext().findNext()
        name = td.text
        td = td.findNext()
        owner = td.text
        td = td.findNext()
        airquality = getEvaluation(td)
        td = td.findNext("td")
        SO2_1h = getEvaluation(td)
        td = td.findNext("td")
        NO2_1h = getEvaluation(td)
        td = td.findNext("td")
        CO_1h = getEvaluation(td)
        td = td.findNext("td")
        O3_1h = getEvaluation(td)
        td = td.findNext("td")
        PM10_1h = getEvaluation(td)
        td = td.findNext("td").findNext("td")
        PM10_24h = getEvaluation(td)
        scraperwiki.datastore.save(["code"], {
            "code" : code,
            "name" : name,
            "owner" : owner,
            "province" : province,
            "latitude" : latitude,
            "longitude" : longitude,
            "altitude" : altitude,
            "time" : date,
            "airquality" : airquality,
            "SO2_1h" : SO2_1h,
            "NO2_1h" : NO2_1h,
            "CO_1h" : CO_1h,
            "O3_1h" : O3_1h,
            "PM10_1h" : PM10_1h,
            "PM10_24h" : PM10_24h,
        }, date = datetime.datetime(*map(int, re.split('[^\d]', date)[:-2])))
    else:
        raise Exception
####################################
# Informace o kvalitě ovzduší v ČR #
####################################

import datetime, re, scraperwiki, urlparse
from BeautifulSoup import BeautifulSoup

def getEvaluation(node):
    evaluation = re.match(
        "\d+(\.\d+)?",
        node.find("span").text.encode("utf8").replace(",", ".").replace(" ", "")
    )
    if evaluation:
        evaluation = evaluation.group()
    else:
        style = node["style"]
        if style == "background-color: white":
            evaluation = "Neúplná data"
        elif style == "background-color: #CFCFCF":
            evaluation = "Veličina se na uvedené stanici neměří"
        else:
            evaluation = ""
    return evaluation

def reformatDate(text):
    match = re.match(
        "(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s+(?P<hours>\d{2}):(?P<minutes>\d{2})",
        text
    )
    date = "{0[0]}-{0[1]}-{0[2]}T{0[3]}:{0[4]}:00+01:00".format(
        map(match.group, ["year", "month", "day", "hours", "minutes"])
    )
    return date

def reformatCoords(text):
    latitude, longitude = text.encode("utf-8").replace(" sš ", "N\n").replace(" vd", "E").replace("°", "").replace("´", "'").split("\n")
    return latitude, longitude

def scrapeWeatherStation(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    tds = soup.find("table").findAll("td")
    altitude = re.match("\d+", tds[-1].text).group()
    latitude, longitude = reformatCoords(tds[-3].text)
    return latitude, longitude, altitude

# Vytvoření záhlaví ukládaných dat
scraperwiki.sqlite.save_var(
    "data_columns",
    [
        "code", "name", "owner",
        "province", # Kraj
        "latitude", "longitude", "altitude",
        "time", "airquality", "SO2_1h",
        "NO2_1h", "CO_1h", "O3_1h", "PM10_1h",
        "PM10_24h"
    ]
)

# Získání stránky
startingUrl = "http://portal.chmi.cz/files/portal/docs/uoco/web_generator/actual_hour_data_CZ.html"
html = scraperwiki.scrape(startingUrl)
soup = BeautifulSoup(html)

# Najdi první tabulku
table = soup.find("table")
trs = table.findAll("tr")

for tr in trs:
    ths = tr.findAll("th")
    tds = tr.findAll("td")
    rowSignature = (len(tds), len(ths))
    if rowSignature == (0, 9):
        th = tr.find("th")
        province = th.text.replace("Kraj: ", "")
        th = th.findNext().text
        date = reformatDate(th)
    elif rowSignature == (0, 10):
        pass
    elif rowSignature == (10, 1):
        pass
    elif rowSignature == (11, 0):
        td = tr.find("td")
        identifier = td.find("a")
        code = identifier.text
        weatherStationUrl = urlparse.urljoin(startingUrl, identifier["href"])
        latitude, longitude, altitude = scrapeWeatherStation(weatherStationUrl)
        td = td.findNext().findNext()
        name = td.text
        td = td.findNext()
        owner = td.text
        td = td.findNext()
        airquality = getEvaluation(td)
        td = td.findNext("td")
        SO2_1h = getEvaluation(td)
        td = td.findNext("td")
        NO2_1h = getEvaluation(td)
        td = td.findNext("td")
        CO_1h = getEvaluation(td)
        td = td.findNext("td")
        O3_1h = getEvaluation(td)
        td = td.findNext("td")
        PM10_1h = getEvaluation(td)
        td = td.findNext("td").findNext("td")
        PM10_24h = getEvaluation(td)
        scraperwiki.datastore.save(["code"], {
            "code" : code,
            "name" : name,
            "owner" : owner,
            "province" : province,
            "latitude" : latitude,
            "longitude" : longitude,
            "altitude" : altitude,
            "time" : date,
            "airquality" : airquality,
            "SO2_1h" : SO2_1h,
            "NO2_1h" : NO2_1h,
            "CO_1h" : CO_1h,
            "O3_1h" : O3_1h,
            "PM10_1h" : PM10_1h,
            "PM10_24h" : PM10_24h,
        }, date = datetime.datetime(*map(int, re.split('[^\d]', date)[:-2])))
    else:
        raise Exception

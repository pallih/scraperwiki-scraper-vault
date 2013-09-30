#-*- coding:utf-8 -*-
####################################
# Informace o kvalitě ovzduší v ČR #
####################################

import datetime, re, scraperwiki, urlparse
from BeautifulSoup import BeautifulSoup


class Scraper (object):
    
    def __init__(self):
        self.startingUrl = "http://portal.chmi.cz/files/portal/docs/uoco/web_generator/actual_hour_data_CZ.html"
        self.header = [
            {
                "pollutant" : "Kvalita ovzduší",
                "period" : 3600,
            },
            {
                "pollutant" : "SO2",
                "period" : 3600,
            },
            {
                "pollutant" : "NO2",
                "period" : 3600,
            },
            {
                "pollutant" : "CO",
                "period" : 28800,
            },
            {
                "pollutant" : "O3",
                "period" : 3600,
            },
            {
                "pollutant" : "PM10",
                "period" : 3600,
            },
            {}, # Prázdný sloupec v tabulce
            {
                "pollutant" : "PM10",
                "period" : 86400,
            },
        ]
        self.date = False
        self.province = False

    def getEvaluation(self, node):
        value = re.match(
            "\d+(\.\d+)?",
            node.find("span").text.encode("utf8").replace(",", ".").replace(" ", "")
        )
        if value:
            value = value.group()
            style = node["style"]
            colour = re.search("\#[0-9A-F]{6}", style)
            if colour:
                colour = colour.group()
                valueType = {
                    "#C7EAFB" : "velmi_dobra",
                    "#9BD3AE" : "dobra",
                    "#FFF200" : "uspokojiva",
                    "#FAA61A" : "vyhovujici",
                    "#ED1C24" : "spatna",
                    "#671F20" : "velmi_spatna",
                }[colour]
            else:
                valueType = "bezna"
        else:
            style = node["style"]
            if style == "background-color: white":
                value = ""
                valueType = "neuplne"
            elif style == "background-color: #CFCFCF":
                value = ""
                valueType = "nedostupne"
            else:
                value = valueType = ""
        return {
            "value" : value,
            "valueType" : valueType,
        }
    
    def reformatDate(self, text):
        match = re.match(
            "(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s+(?P<hours>\d{2}):(?P<minutes>\d{2})",
            text
        )
        date = "{0[0]}-{0[1]}-{0[2]}T{0[3]}:{0[4]}:00+01:00".format(
            map(match.group, ["year", "month", "day", "hours", "minutes"])
        )
        return date
    
    def reformatCoords(self, text):
        match = re.findall("(\d+(\.\d+)?)", text)
        match = [coord[0] for coord in match]
        latitude = match[:len(match)/2]
        latitude = int(latitude[0]) + float(latitude[1])/60 + float(latitude[2])/3600
        longitude = match[len(match)/2:]
        longitude = int(longitude[0]) + float(longitude[1])/60 + float(longitude[2])/3600
        return latitude, longitude
    
    def scrapeWeatherStation(self, url):
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        tds = soup.find("table").findAll("td")
        altitude = re.match("\d+", tds[-1].text).group()
        latitude, longitude = self.reformatCoords(tds[-3].text)
        return latitude, longitude, altitude
    
    def main(self):
        # Získání stránky
        html = scraperwiki.scrape(self.startingUrl)
        soup = BeautifulSoup(html)
        
        # Najdi první tabulku
        table = soup.find("table")
        trs = table.findAll("tr")
        
        for tr in trs:
            self.processRow(tr)
    
    def processRow(self, row):
        ths = row.findAll("th")
        tds = row.findAll("td")
        rowSignature = (len(tds), len(ths))
        if rowSignature == (0, 9):
            th = row.find("th")
            self.province = th.text.replace("Kraj: ", "")
            th = th.findNext().text
            self.date = self.reformatDate(th)
        elif rowSignature == (0, 10):
            pass
        elif rowSignature == (10, 1):
            pass
        elif rowSignature == (11, 0):
            td = row.find("td")
            identifier = td.find("a")
            code = identifier.text
            weatherStationUrl = urlparse.urljoin(self.startingUrl, identifier["href"])
            
            latitude, longitude, altitude = self.scrapeWeatherStation(weatherStationUrl)
            td = td.findNext().findNext()
            name = td.text
            td = td.findNext()
            owner = td.text
            
            scraperwiki.sqlite.save(
                unique_keys = ["code"],
                data = {
                    "altitude" : altitude,
                    "code" : code,
                    "latitude" : latitude,
                    "longitude" : longitude,
                    "name" : name,
                    "owner" : owner,
                    "province" : self.province,
                },
                table_name = "stations"
            )
            
            values = td.fetchNextSiblings(name = "td")
            for index, value in enumerate(values):
                if not index == 6:
                    evaluation = self.getEvaluation(value)
                    header = self.header[index]

                    scraperwiki.sqlite.save(
                        unique_keys = ["pollutant"],
                        data = {
                            "pollutant" : header["pollutant"],
                        },
                        table_name = "pollutants"
                    )

                    scraperwiki.sqlite.save(
                        unique_keys = ["code", "time", "pollutant"],
                        data = {
                            "code" : code,
                            "period" : header["period"],
                            "pollutant" : header["pollutant"],
                            "time" : self.date,
                            "value" : evaluation["value"],
                            "valueType" : evaluation["valueType"],
                        },
                        table_name = "measurements"
                    )

        else:
            raise Exception


def main():
    zu_imise = scraperwiki.utils.swimport("imise_-_zdravotni_ustav_ostrava")
    zu_imise.main()
    s = Scraper()
    s.main()

main()#-*- coding:utf-8 -*-
####################################
# Informace o kvalitě ovzduší v ČR #
####################################

import datetime, re, scraperwiki, urlparse
from BeautifulSoup import BeautifulSoup


class Scraper (object):
    
    def __init__(self):
        self.startingUrl = "http://portal.chmi.cz/files/portal/docs/uoco/web_generator/actual_hour_data_CZ.html"
        self.header = [
            {
                "pollutant" : "Kvalita ovzduší",
                "period" : 3600,
            },
            {
                "pollutant" : "SO2",
                "period" : 3600,
            },
            {
                "pollutant" : "NO2",
                "period" : 3600,
            },
            {
                "pollutant" : "CO",
                "period" : 28800,
            },
            {
                "pollutant" : "O3",
                "period" : 3600,
            },
            {
                "pollutant" : "PM10",
                "period" : 3600,
            },
            {}, # Prázdný sloupec v tabulce
            {
                "pollutant" : "PM10",
                "period" : 86400,
            },
        ]
        self.date = False
        self.province = False

    def getEvaluation(self, node):
        value = re.match(
            "\d+(\.\d+)?",
            node.find("span").text.encode("utf8").replace(",", ".").replace(" ", "")
        )
        if value:
            value = value.group()
            style = node["style"]
            colour = re.search("\#[0-9A-F]{6}", style)
            if colour:
                colour = colour.group()
                valueType = {
                    "#C7EAFB" : "velmi_dobra",
                    "#9BD3AE" : "dobra",
                    "#FFF200" : "uspokojiva",
                    "#FAA61A" : "vyhovujici",
                    "#ED1C24" : "spatna",
                    "#671F20" : "velmi_spatna",
                }[colour]
            else:
                valueType = "bezna"
        else:
            style = node["style"]
            if style == "background-color: white":
                value = ""
                valueType = "neuplne"
            elif style == "background-color: #CFCFCF":
                value = ""
                valueType = "nedostupne"
            else:
                value = valueType = ""
        return {
            "value" : value,
            "valueType" : valueType,
        }
    
    def reformatDate(self, text):
        match = re.match(
            "(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s+(?P<hours>\d{2}):(?P<minutes>\d{2})",
            text
        )
        date = "{0[0]}-{0[1]}-{0[2]}T{0[3]}:{0[4]}:00+01:00".format(
            map(match.group, ["year", "month", "day", "hours", "minutes"])
        )
        return date
    
    def reformatCoords(self, text):
        match = re.findall("(\d+(\.\d+)?)", text)
        match = [coord[0] for coord in match]
        latitude = match[:len(match)/2]
        latitude = int(latitude[0]) + float(latitude[1])/60 + float(latitude[2])/3600
        longitude = match[len(match)/2:]
        longitude = int(longitude[0]) + float(longitude[1])/60 + float(longitude[2])/3600
        return latitude, longitude
    
    def scrapeWeatherStation(self, url):
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        tds = soup.find("table").findAll("td")
        altitude = re.match("\d+", tds[-1].text).group()
        latitude, longitude = self.reformatCoords(tds[-3].text)
        return latitude, longitude, altitude
    
    def main(self):
        # Získání stránky
        html = scraperwiki.scrape(self.startingUrl)
        soup = BeautifulSoup(html)
        
        # Najdi první tabulku
        table = soup.find("table")
        trs = table.findAll("tr")
        
        for tr in trs:
            self.processRow(tr)
    
    def processRow(self, row):
        ths = row.findAll("th")
        tds = row.findAll("td")
        rowSignature = (len(tds), len(ths))
        if rowSignature == (0, 9):
            th = row.find("th")
            self.province = th.text.replace("Kraj: ", "")
            th = th.findNext().text
            self.date = self.reformatDate(th)
        elif rowSignature == (0, 10):
            pass
        elif rowSignature == (10, 1):
            pass
        elif rowSignature == (11, 0):
            td = row.find("td")
            identifier = td.find("a")
            code = identifier.text
            weatherStationUrl = urlparse.urljoin(self.startingUrl, identifier["href"])
            
            latitude, longitude, altitude = self.scrapeWeatherStation(weatherStationUrl)
            td = td.findNext().findNext()
            name = td.text
            td = td.findNext()
            owner = td.text
            
            scraperwiki.sqlite.save(
                unique_keys = ["code"],
                data = {
                    "altitude" : altitude,
                    "code" : code,
                    "latitude" : latitude,
                    "longitude" : longitude,
                    "name" : name,
                    "owner" : owner,
                    "province" : self.province,
                },
                table_name = "stations"
            )
            
            values = td.fetchNextSiblings(name = "td")
            for index, value in enumerate(values):
                if not index == 6:
                    evaluation = self.getEvaluation(value)
                    header = self.header[index]

                    scraperwiki.sqlite.save(
                        unique_keys = ["pollutant"],
                        data = {
                            "pollutant" : header["pollutant"],
                        },
                        table_name = "pollutants"
                    )

                    scraperwiki.sqlite.save(
                        unique_keys = ["code", "time", "pollutant"],
                        data = {
                            "code" : code,
                            "period" : header["period"],
                            "pollutant" : header["pollutant"],
                            "time" : self.date,
                            "value" : evaluation["value"],
                            "valueType" : evaluation["valueType"],
                        },
                        table_name = "measurements"
                    )

        else:
            raise Exception


def main():
    zu_imise = scraperwiki.utils.swimport("imise_-_zdravotni_ustav_ostrava")
    zu_imise.main()
    s = Scraper()
    s.main()

main()
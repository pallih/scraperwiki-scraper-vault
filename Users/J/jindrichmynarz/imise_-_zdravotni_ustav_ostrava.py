#-*- coding:utf-8 -*-
import lxml.html, re, scraperwiki

class Scraper (object):
    
    def __init__(self):
        self.startingUrl = "http://www.zuova.cz/informace/imise.php"
        self.owner = "Zdravotní ústav"
        self.valueTypes = {
            "SO2" : "",
            "NO2" : "",
            "CO" : "",
            "O3" : "",
            "PM10" : "",
        }

    def formatTimestamp(self, timestamp):
        match = re.match(
            "(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})\s(?P<time>[\d:]+)",
            timestamp
        )
        timestamp = "{0[0]}-{0[1]}-{0[2]}T{0[3]}+01:00".format(
            map(match.group, ["year", "month", "day", "time"])
        )
        return timestamp
    
    def formatName(self, name):
        return name.replace("(MS)", "").strip()
    
    def getValueType(self, value, pollutantCode):
        if self.valueTypes.has_key(pollutantCode):
            self.valueTypes["pollutantCode"]
        else:
            return "bezna"

    def main(self):
        html = scraperwiki.scrape(self.startingUrl)
        root = lxml.html.fromstring(html)
        body = root.cssselect("#stredni .vnitrni")[0]
    
        titles = body.findall("h2")[1:4]
        tables = body.findall("table")[:3]
    
        for title, table in zip(titles, tables):
            name = self.formatName(title.text)
            timestamp = self.formatTimestamp(table.cssselect("th")[0].text)
            
            scraperwiki.sqlite.save(
                unique_keys = ["name"],
                data = {
                    "name" : name,
                    "owner" : self.owner,
                },
                table_name = "stations"
            )
    
            rows = table.findall("tr")[1:]
            for row in rows:
                tds = row.findall("td")
                pollutantCode = tds[0].text
                value = tds[1].text
                if not value:
                    value = tds[1].text_content()
                match = re.match("(\*)|(\d+(,\d+)?)", value)
                if match:
                    match = match.group()
                    if match == "*":
                        value = ""
                        valueType = "nedostupne"
                    elif match == "0":
                        value = ""
                        valueType = "zavada"
                    else:
                        value = float(match.replace(",", "."))
                        valueType = self.getValueType(value, pollutantCode)
                    scraperwiki.sqlite.save(
                        unique_keys = ["name", "time", "pollutant"],
                        data = {
                            "name" : name,
                            "period" : 3600,
                            "pollutant" : pollutionCode,
                            "time" : timestamp,
                            "value" : value,
                            "valueType" : valueType,
                        },
                        table_name = "measurements"
                    )


def main():
    s = Scraper()
    s.main()

main()

# aim: parse sovereign ratings from Fitch
# see http://quant.stackexchange.com/q/739/1177

import xlrd
import scraperwiki
import datetime


class Country(object):
    def __init__(self, n=""):
        self.name = n
        self.lRatings = []
    def append(self, iRating):
        self.lRatings.append(iRating)
    def getNbRatings(self):
        return len(self.lRatings)
    def getRecords(self):
        lRecords = []
        for iRating in self.lRatings:
            record = iRating.getRecord()
            lRecords.append(record)
        return lRecords


class Rating(object):
    def __init__(self, tokens=[]):
        self.country = ""
        self.date = ""
        self.forCurrLongTerm = ""
        self.forCurrShortTerm = ""
        self.forCurrOutlook = ""
        self.locCurrLongTerm = ""
        self.locCurrOutlook = ""
        if tokens != []:
            self.load(tokens)
    def load(self, tokens):
        if tokens[0] == "":
            return
        self.country = tokens[0]
        tmp = xlrd.xldate_as_tuple(tokens[1], 0)
        self.date = datetime.date(tmp[0], tmp[1], tmp[2])
        self.forCurrLongTerm = tokens[2]
        self.forCurrShortTerm = tokens[3]
        self.forCurrOutlook = tokens[4]
        self.locCurrLongTerm = tokens[5]
        self.locCurrOutlook = tokens[6]
    def getRecord(self):
        record = {"country": self.country,
            "date": self.date.isoformat(),
            "forCurrLongTerm": self.forCurrLongTerm,
            "forCurrShortTerm": self.forCurrShortTerm,
            "forCurrOutlook": self.forCurrOutlook,
            "locCurrLongTerm": self.locCurrLongTerm,
            "locCurrOutlook": self.locCurrOutlook
        }
        return record


url = "http://www.fitchratings.com/web_content/ratings/sovereign_ratings_history.xls"

wb = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))
#print "nb sheet(s): %s" % wb.nsheets
#print "shhet name(s): %s" % wb.sheet_names()
sh = wb.sheet_by_name(u'Sovereign')


dCountries = {}
rownum = 0
recording = False
nbRecords = 0
while True:
    rownum += 1
    tokens = sh.row_values(rownum)
#    print rownum, tokens
    if tokens == []:
        break
    if tokens[0] == u"Country":
        recording = True
        continue
    if recording:
        if not dCountries.has_key(tokens[0]):
            iCountry = Country(tokens[0])
            dCountries[tokens[0]] = iCountry
        iRating = Rating(tokens)
        if iRating.country != "":
            dCountries[tokens[0]].append(iRating)
            nbRecords += 1
        else:
            break

print "nb countries: %i" % len(dCountries.keys())
print "nb records: %i" % nbRecords

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`country` text,  `date` real, `forCurrLongTerm` text, `forCurrShortTerm` text, `forCurrOutlook` text, `locCurrLongTerm` text, `locCurrOutlook` text)")
for country in dCountries.keys():
    iCountry = dCountries[country]
    lRecords = iCountry.getRecords()
    scraperwiki.sqlite.save(unique_keys=["country", "date"], data=lRecords)

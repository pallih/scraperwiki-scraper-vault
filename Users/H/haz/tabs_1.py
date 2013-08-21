import urllib2, json
from bs4 import BeautifulSoup
from twill.commands import *

WORD_OR_PHRASE = 'cycle'
COMMITTEE = ''

# Grab the voting form
go("http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare")

# Fill out the form with the id, and set it to download
fv("1", "word_or_phrase", WORD_OR_PHRASE)






# Define more search restrictions here...



submit()

soup = BeautifulSoup(show())

rows = soup.find("table", {"id": "searchResultsTable"}).find_all("tr")[1:]

agenda_items = []

for result in rows[:2]:
    meeting_date = result.find("td", {"class": "meetingDate"}).get_text()
    item_num = result.find("td", {"class": "reference"}).find("a").get_text()
    item_url = "http://app.toronto.ca" + str(result).split('(')[1].split(')')[0][1:-1]
    title = result.find("td", {"class": "agendaItemTitle"}).get_text()
    committee = result.find("td", {"class": "decisionBodyName"}).get_text()
    agenda_items.append({'meeting_date': meeting_date,
                         'item_num': item_num,
                         'item_url': item_url,
                         'title': title,
                         'committee': committee})

    print "Info: %s / %s / %s / %s / %s" % (meeting_date, item_num, item_url, title, committee)

print json.dumps(agenda_items, sort_keys=True, indent=4, separators=(',', ': '))





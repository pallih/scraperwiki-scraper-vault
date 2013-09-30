import scraperwiki
import BeautifulSoup
import re
import datetime

from scraperwiki import datastore
from datetime import datetime

def Main():
    today = datetime.today()
    start_month = {"month": today.month, "year": today.year }
    lookahead_months = 2
    for months_to_lookahead in range(0, lookahead_months + 1):
        ScrapeMonth(AddMonths(start_month, months_to_lookahead))
    
# Does Python have a better way to do this? (Will break for months values > 12.)
def AddMonths(month, months):
    if month['month'] + months > 12:
        next_month = month['month'] + months - 12
        return {"month": next_month, "year": month['year'] + 1}
    else:
        return {"month": month['month'] + months, "year": month['year']}
    
def ScrapeMonth(month):
    html = scraperwiki.scrape("http://modgov.sefton.gov.uk/moderngov/mgCalendarMonthView.aspx?M=" + str(month['month']) + "&DD=" + str(month['year']))
    page = BeautifulSoup.BeautifulSoup(html)
    for meeting_link in page.findAll("a", { "class" : "mgCalendarCellTxt" }):
        title = meeting_link['title']
        time = GetMeetingTime(title)
        title = RemoveTimeFromTitle(title)
        note = ExtractNote(title)
        title = RemoveNoteFromTitle(title)
        url = "http://modgov.sefton.gov.uk/moderngov/" + meeting_link['href']
        # I would have used url as the unique key, but the url for elections has a dynamic 'PRID' value which I need to remove
        scraperwiki.datastore.save(unique_keys = ['date', 'title'], data = { "title": title, "date": time, "note": note, "url": url })

def GetMeetingTime(meeting_title):
    if MeetingHasTime(meeting_title):
        return ExtractMeetingTime(meeting_title)
    else:
        return ExtractMeetingDate(meeting_title)
        
def MeetingHasTime(meeting_title):
    return re.search('\d{2}\/\d{2}\/\d{4} \d+\.\d+ (am|pm)', meeting_title) is not None
        
def ExtractMeetingDate(meeting_title):
    date_regex = '(\d{2})\/(\d{2})\/(\d{4})'
    match = re.search(date_regex, meeting_title)
    day = int(match.group(1))
    month = int(match.group(2)) # Month and year are already known, but best to be safe
    year = int(match.group(3))
    date = datetime(year, month, day)
    return date
        
def ExtractMeetingTime(meeting_title):
    time_regex = '(\d{2})\/(\d{2})\/(\d{4}) (\d+)\.(\d+) (am|pm)'
    match = re.search(time_regex, meeting_title)
    day = int(match.group(1))
    month = int(match.group(2)) # Month and year are already known, but best to be safe
    year = int(match.group(3))
    hour = int(match.group(4))
    minute = int(match.group(5))
    am_or_pm = match.group(6)
    if am_or_pm == "pm" and hour != 12:
        hour += 12
    time = datetime(year, month, day, hour, minute)
    return time

def RemoveTimeFromTitle(meeting_title):
    return re.sub(',.*?$', '', meeting_title)

def ExtractNote(meeting_title):
    note_regex = '(NEW|CANCELLED|MOVED|PROVISIONAL) - '
    match = re.match(note_regex, meeting_title)
    if match is None:
        return ""
    else:
        return match.group(1)
    
def RemoveNoteFromTitle(meeting_title):
    note_regex = '(NEW|CANCELLED|MOVED|PROVISIONAL) - ' # TODO: Remove duplication
    return re.sub(note_regex, '', meeting_title)
                
Main()
import scraperwiki
import BeautifulSoup
import re
import datetime

from scraperwiki import datastore
from datetime import datetime

def Main():
    today = datetime.today()
    start_month = {"month": today.month, "year": today.year }
    lookahead_months = 2
    for months_to_lookahead in range(0, lookahead_months + 1):
        ScrapeMonth(AddMonths(start_month, months_to_lookahead))
    
# Does Python have a better way to do this? (Will break for months values > 12.)
def AddMonths(month, months):
    if month['month'] + months > 12:
        next_month = month['month'] + months - 12
        return {"month": next_month, "year": month['year'] + 1}
    else:
        return {"month": month['month'] + months, "year": month['year']}
    
def ScrapeMonth(month):
    html = scraperwiki.scrape("http://modgov.sefton.gov.uk/moderngov/mgCalendarMonthView.aspx?M=" + str(month['month']) + "&DD=" + str(month['year']))
    page = BeautifulSoup.BeautifulSoup(html)
    for meeting_link in page.findAll("a", { "class" : "mgCalendarCellTxt" }):
        title = meeting_link['title']
        time = GetMeetingTime(title)
        title = RemoveTimeFromTitle(title)
        note = ExtractNote(title)
        title = RemoveNoteFromTitle(title)
        url = "http://modgov.sefton.gov.uk/moderngov/" + meeting_link['href']
        # I would have used url as the unique key, but the url for elections has a dynamic 'PRID' value which I need to remove
        scraperwiki.datastore.save(unique_keys = ['date', 'title'], data = { "title": title, "date": time, "note": note, "url": url })

def GetMeetingTime(meeting_title):
    if MeetingHasTime(meeting_title):
        return ExtractMeetingTime(meeting_title)
    else:
        return ExtractMeetingDate(meeting_title)
        
def MeetingHasTime(meeting_title):
    return re.search('\d{2}\/\d{2}\/\d{4} \d+\.\d+ (am|pm)', meeting_title) is not None
        
def ExtractMeetingDate(meeting_title):
    date_regex = '(\d{2})\/(\d{2})\/(\d{4})'
    match = re.search(date_regex, meeting_title)
    day = int(match.group(1))
    month = int(match.group(2)) # Month and year are already known, but best to be safe
    year = int(match.group(3))
    date = datetime(year, month, day)
    return date
        
def ExtractMeetingTime(meeting_title):
    time_regex = '(\d{2})\/(\d{2})\/(\d{4}) (\d+)\.(\d+) (am|pm)'
    match = re.search(time_regex, meeting_title)
    day = int(match.group(1))
    month = int(match.group(2)) # Month and year are already known, but best to be safe
    year = int(match.group(3))
    hour = int(match.group(4))
    minute = int(match.group(5))
    am_or_pm = match.group(6)
    if am_or_pm == "pm" and hour != 12:
        hour += 12
    time = datetime(year, month, day, hour, minute)
    return time

def RemoveTimeFromTitle(meeting_title):
    return re.sub(',.*?$', '', meeting_title)

def ExtractNote(meeting_title):
    note_regex = '(NEW|CANCELLED|MOVED|PROVISIONAL) - '
    match = re.match(note_regex, meeting_title)
    if match is None:
        return ""
    else:
        return match.group(1)
    
def RemoveNoteFromTitle(meeting_title):
    note_regex = '(NEW|CANCELLED|MOVED|PROVISIONAL) - ' # TODO: Remove duplication
    return re.sub(note_regex, '', meeting_title)
                
Main()

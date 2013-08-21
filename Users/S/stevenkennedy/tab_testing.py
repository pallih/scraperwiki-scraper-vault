# Testing to get info from tables
import scraperwiki
import lxml.html
from datetime import datetime, timedelta

class tab_scraper:
    def __init__(self):
        #Set date based on Australian Eastern Time, stored as string
        self.today = datetime.strftime((datetime.now() + timedelta(hours=11)),format="%Y-%m-%d")
        self.meetings = []

    def todays_meetings(self):
        """
        Returns a list of lists of today's meetings. Outer lists are the racing, greyhound and harness
        categories. Inner lists are the individual meetings, stored as a tuple of the meeting code
        and racing code - eg. ('S','R')
        """
        ret = []
        # Get html for NSW tab site for today's racing
        url = "http://www.tab.com.au/Racing/Information/DisplayMeetings.aspx?State=2&DisplayType=TodaysRacing"
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        #Split up into the three race codes
        for tab in root.xpath("//table[@id='BetGrid_DGTableOne']"):
            tmp = []
            #Find the links and split into the meeting and racing codes
            for link in tab.xpath("tr/td/a/@href"):
                if "javascript:DISPLAYRACES" in link:
                    tmp.append((link.split("'")[3],link.split("'")[1]))
            ret.append(tmp)
        return ret

    def race_times(self,meeting):
        """
        Returns a list of race numbers and race times for the given meeting, stored as a list of tuples
        """
        url = "http://www.tab.com.au/Racing/Information/DisplayRaces.aspx?State=2&MeetingCode=" + \
            "{0}&RacingCode={1}&FromDate={2}T00:00:00".format(meeting[0],meeting[1],self.today)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        race_times = []
        # find the rows of the table
        for row in root.xpath("//tr[@class='TableText']"):
            rowcells = row.getchildren()
            #race number
            num = rowcells[0].xpath("span/text()")[0]
            #race time
            tim = datetime.strptime(rowcells[5].xpath("span/text()")[0],"%I:%M %p").strftime("%H:%M")
            #append to race_times
            race_times.append((num,tim))
        return race_times

    def store_data(self,date,rc,mc,rn,rt,rtyp):
        """
        Stores the data in the datastore
        """
        data = {"date":date,"meeting_code":mc,"racing_code":rc,"race_number":rn,"race_time":rt,"race_type":rtyp}
        scraperwiki.sqlite.save(unique_keys=["date","meeting_code","racing_code","race_number"],data=data)
    
    def run_scraper(self):
        #Get the list of meetings
        self.meetings = self.todays_meetings()
        for racetype in range(len(self.meetings)):
            #Select the race type
            if racetype == 0:
                rty = "Races"
            elif racetype == 1:
                rty = "Greyhounds"
            else:
                rty = "Harness"
            for meeting in self.meetings[racetype]:
                #Get the list of race times
                rts = self.race_times(meeting)
                for tm in rts:
                    #Store the data row
                    self.store_data(self.today,meeting[0],meeting[1],tm[0],tm[1],rty)

#Main sequence
ts = tab_scraper()
ts.run_scraper()
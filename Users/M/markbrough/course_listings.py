import scraperwiki
from lxml import html

from urllib2 import urlopen, Request, URLError
import re
import string
from lxml.html.soupparser import fromstring


def make_course_code(the_code):
    return re.split("_", the_code)

urls = ["""http://www.soas.ac.uk/snorri1213/reporting/individual;module;id;153400003-A12/13%0D%0A153400011-A12/13%0D%0A153400012-A12/13%0D%0A153400013-A12/13%0D%0A153400025-A12/13%0D%0A153400031-A12/13%0D%0A153400032-A12/13%0D%0A153400100-A12/13%0D%0A153400101-A12/13%0D%0A153400102-A12/13%0D%0A153400103-A12/13%0D%0A153400106-A12/13%0D%0A153400107-A12/13%0D%0A153400108-A12/13%0D%0A153400109-A12/13%0D%0A153400115-A12/13%0D%0A153400116-A12/13%0D%0A153400117-A12/13%0D%0A153400118-A12/13%0D%0A153400119-A12/13%0D%0A153400120-A12/13%0D%0A153400121-A12/13%0D%0A153400122-A12/13%0D%0A15PECC004-A12/13%0D%0A15PECC005-A12/13%0D%0A15PECC006-A12/13%0D%0A15PECC007-A12/13%0D%0A15PECC008-A12/13%0D%0A15PECC011-A12/13%0D%0A15PECC018-A12/13%0D%0A15PECC019-A12/13%0D%0A15PECC020-A12/13%0D%0A15PECC021-A12/13%0D%0A15PECC024-A12/13%0D%0A15PECC025-A12/13%0D%0A15PECC026-A12/13%0D%0A15PECC027-A12/13%0D%0A15PECC028-A12/13%0D%0A15PECC029-A12/13%0D%0A15PECC030-A12/13%0D%0A15PECC031-A12/13%0D%0A15PECC035-A12/13%0D%0A15PECC036-A12/13%0D%0A15PECC039-A12/13%0D%0A15PECC040-A12/13%0D%0A15PECC045-A12/13%0D%0A15PECC048-A12/13%0D%0A15PECC049-A12/13%0D%0A15PECC051-A12/13%0D%0A15PECC203-A12/13%0D%0A15PECC334-A12/13%0D%0A15PECC341-A12/13%0D%0A15PECH002-A12/13%0D%0AECCOMP-A12/13%0D%0AECDEPSEM-A12/13%0D%0AECMATHSSTATS-A12/13%0D%0AECMONSEM-A12/13%0D%0AECPGRES-A12/13%0D%0ANEWECPG001-A12/13%0D%0ANEWECPG002-A12/13%0D%0ANEWECPG003-A12/13%0D%0ANEWECPG004-A12/13%0D%0ANEWECPG005-A12/13%0D%0ANEWECPG006-A12/13%0D%0ANEWECPG007-A12/13%0D%0ANEWECPG008-A12/13%0D%0ANEWECPG009-A12/13%0D%0ANEWECPG010-A12/13%0D%0ANEWECPG011-A12/13%0D%0APRESESSEC-A12/13%0D%0A?days=1-7&weeks=2;3;4;5;6;8;9;10;11;12;16;17;18;19;20;22;23;24;25;26;30;31;&periods=1-16&template=module+individual&height=100&week=100""","""http://www.soas.ac.uk/snorri1213/reporting/individual;module;id;151010001-A12/13%0D%0A151010020-A12/13%0D%0A151010021-A12/13%0D%0A151010022-A12/13%0D%0A151010024-A12/13%0D%0A151010032-A12/13%0D%0A151010033-A12/13%0D%0A151010034-A12/13%0D%0A151010035-A12/13%0D%0A151010037-A12/13%0D%0A151010039-A12/13%0D%0A151010040-A12/13%0D%0A151010041-A12/13%0D%0A151010042-A12/13%0D%0A151010043-A12/13%0D%0A15PDSC001-A12/13%0D%0A15PDSC002-A12/13%0D%0A15PDSC003-A12/13%0D%0A15PDSC005-A12/13%0D%0A15PDSC006-A12/13%0D%0A15PDSC007-A12/13%0D%0A15PDSC008-A12/13%0D%0A15PDSH001-A12/13%0D%0A15PDSH010-A12/13%0D%0A15PDSH015-A12/13%0D%0A15PDSH017-A12/13%0D%0A15PDSH018-A12/13%0D%0A15PDSH019-A12/13%0D%0A15PDSH020-A12/13%0D%0A15PDSH021-A12/13%0D%0A15PDSH022-A12/13%0D%0A15PDSH024-A12/13%0D%0A15PDSH025-A12/13%0D%0A15PDSH026-A12/13%0D%0A15PDSH027-A12/13%0D%0A15PDSH030-A12/13%0D%0A15PDSH031-A12/13%0D%0A15PDSH032-A12/13%0D%0A15PDSH033-A12/13%0D%0A15PDSH034-A12/13%0D%0ADSAGSEM-A12/13%0D%0ADSECOPB-A12/13%0D%0ADSECSEM-A12/13%0D%0ADSRESTRAIN-A12/13%0D%0ALSSPRFPRAC-A12/13%0D%0ANEWDSPG001-A12/13%0D%0ANEWDSPG002-A12/13%0D%0ANEWDSPG003-A12/13%0D%0ANEWDSPG004-A12/13%0D%0ANEWDSPG005-A12/13%0D%0ANEWDSPG006-A12/13%0D%0ANEWDSPG007-A12/13%0D%0ANEWDSPG008-A12/13%0D%0ANEWDSPG009-A12/13%0D%0ANEWDSUG001-A12/13%0D%0A?days=1-7&weeks=2;3;4;5;6;8;9;10;11;12;16;17;18;19;20;22;23;24;25;26;30;31;&periods=1-16&template=module+individual&height=100&week=100"""]

for DATA_URL in urls:
    data = scraperwiki.scrape(DATA_URL)
    
    root = html.fromstring(data)
    
    # get the first table
    table = root.cssselect("table")[0]
    #print table.text_content()
    
    # get every other table
    count = 1
    entry = {}
    for element in root.xpath('//table[following-sibling::hr]'):
        if (count ==1):
            # get the headers
            entry["title"] = element.cssselect("table")[4].cssselect("tr")[0].cssselect("td")[1].text_content()
            entry["dept"] = element.cssselect("table")[5].cssselect("tr")[0].cssselect("td")[1].text_content()
            count = 2
        elif (count ==2):
            # get the times, ignoring first (header) row
            days = element.xpath("tr")
            entry["data"] = []
            # for each day, look at each hour
            for day in days:
                day_name = day.xpath("td")[0].text_content()
                if (day_name != ""):
                    #print "day name is ", day_name
                    hours = day.xpath("td[@style='border-bottom:3px solid #000000;']")
                    this_hour = 6
                    # for each hour (1 hr = 1 td, unless colspan >1)
                    for hour in hours:
                        #hour=hour.getparent()
                        #print "got hour..."
                        hourdata = hour.cssselect("td")[0]
                        try:
                            create_course_name = make_course_code(hourdata.cssselect("td table")[0].cssselect("td")[0].text_content())
                            entry["course_code"] = create_course_name[0]
                            entry["course_part"] = create_course_name[1]
                            entry["term"] = hourdata.cssselect("td table")[0].cssselect("td")[1].text_content()
                            entry["course_name"] = hourdata.cssselect("td table")[1].cssselect("td")[0].text_content()
                            entry["course_number"] = hourdata.cssselect("td table")[1].cssselect("td")[1].text_content()
                            entry["lecturer"] = hourdata.cssselect("td table")[2].cssselect("td")[0].text_content()
                            entry["location"] = hourdata.cssselect("td table")[2].cssselect("td")[2].text_content()
                        except IndexError:
                            pass
    
                        try:
                            hdata = {}
                            hdata["day"] = day_name
                            hdata["start_time"] = this_hour
                            #print this_hour
                            hdata["duration"] = hourdata.attrib["colspan"]
                            
                            #print "Got some data!!", hour.text_content()
                            entry["data"].append(hdata)
                            this_hour = this_hour + int(hdata["duration"])
                        except KeyError:
    
                        # if the td DOES NOT contain a table, then count it...
                            this_hour = this_hour + 1
                            pass
                        # append to entry["data"]
            count = 3
        elif (count ==3):
            # write the data
            for part in entry["data"]:
                #print "Got some data..."
                oneentry = entry
                oneentry["start_time"] = part["start_time"]
                oneentry["day"] = part["day"]
                oneentry["duration"] = part["duration"]
                try:
                    del oneentry["data"]
                except KeyError:
                    pass
                scraperwiki.sqlite.save(unique_keys=['title', 'start_time', 'term'],
                            data=oneentry)
            count = 1

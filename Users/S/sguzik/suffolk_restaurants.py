import scraperwiki
import mechanize
import lxml.html
import urllib, urlparse
import re, json
import datetime
from BeautifulSoup import BeautifulSoup

url = "http://apps.suffolkcountyny.gov/health/Restaurant/Rest_Search.aspx"

zip_code = {'0': '11794', '1': '11930', '2': '11701', '3': '11931', '4': '11702', '5': '11933', '6': '11706', '7': '11705', '8': '11713', '9': '11715', '10': '11716', '11': '11717', '12': '11932', '13': '11718', '14': '11719', '15': '11933', '16': '11934', '17': '11720', '18': '11721', '19': '11722', '20': '11782', '21': '11724', '22': '11725', '23': '11726', '24': '11727', '25': '11935', '26': '11772', '27': '11729', '28': '11746', '29': '11735', '30': '11937', '31': '11730', '32': '11939', '33': '11940', '34': '11731', '35': '11772', '36': '11942', '37': '11733', '38': '11941', '39': '11717', '40': '11731', '41': '11706', '42': '11735','43': '11738', '44': '11770', '45': '11782', '46': '06390', '47': '11901', '48': '11768', '49': '11739', '50': '11740', '51': '11944', '52': '11743', '53': '11946', '54': '11788', '55': '11741', '56': '11742', '57': '11743', '58': '11746', '59': '11749', '60': '11751', '61': '11752', '62': '11947', '63': '11754', '64': '11706', '65': '11755', '66': '11779', '67': '11948', '68': '11757', '69': '11743', '70': '11949', '71': '11950', '72': '11951', '73': '11952', '74': '11763', '75': '11747', '76': '11953', '77': '11764', '78': '11954', '79': '11955', '80': '11766', '81': '11767', '82': '11956', '83': '11703', '84': '11772', '85': '11768', '86': '11702', '87': '11769', '88': '11770', '89': '11770', '90': '11957', '91': '11772', '92': '11958', '93': '11706', '94': '11777', '95': '11776', '96': '11959', '97': '11960', '98': '11961', '99': '11901', '100': '11778', '101': '11779', '102': '11963', '103': '11962', '104': '11780', '105': '11706', '106': '11782', '107': '11784', '108': '11733', '109': '11964', '110': '11965', '111': '11967', '112': '11786', '113': '11787', '114': '11789', '115': '11735', '116': '11746', '117': '11970', '118': '11733', '119': '11968', '120': '11971', '121': '11972', '122': '11790', '123': '11973', '124': '11792', '125': '11975', '126': '11976', '127': '11704', '128': '11795', '129': '11796', '130': '11977', '131': '11978', '132': '11798', '133': '11798', '134': '11980'}

cj = mechanize.CookieJar()
br = mechanize.Browser()
br.set_handle_robots(False)
br1 = mechanize.Browser()
br1.set_handle_robots(False)

def Main():
    last_town = scraperwiki.sqlite.get_var("current_town", "")
    if last_town and last_town < 134:
        print "We got interrupted during the last run. Carry on from", last_town
        i = int(last_town) + 1
    else:
        i = 0
    
    while i < 135:
        print zip_code[str(i)]
        zip = zip_code[str(i)]
        max = SetupBrowsers(zip)

        last_restaurant = scraperwiki.sqlite.get_var("current_restaurant", "")
        if last_restaurant:
            current = int(last_restaurant) + 1
        else:
            current = 2

        while current <= max:
            if current < 10:
                c = '0' + str(current)
            else:
                c = current

            GetRestaurantGrid(c, zip)
            scraperwiki.sqlite.save_var("current_restaurant", c)
            current += 1
        scraperwiki.sqlite.save_var("current_town", i)
        scraperwiki.sqlite.save_var("current_restaurant", "")
        i += 1


def SetupBrowsers(zip):
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_cookiejar(cj)
    br1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br1.set_cookiejar(cj)
    
    response = br.open(url)

    br.select_form("Form1")
    
    # fill in the form
    br["ddl_Town"] = [zip]
    response = br.submit()
    htmlI = response.read()
    #print htmlI

    br.select_form("Form1")
    br.set_all_readonly(False)
    rootI = lxml.html.fromstring(htmlI)
    rest_error = rootI.cssselect("span#errMsgs")[0].text
    if rest_error == "No Restaurants found for the selection criteria. ":
        return 0
    else:
        return max(map(int, re.findall("dgResults\$ctl(\d+)\$ctl00", htmlI)))
    

def GetRestaurantGrid(d, zip):
    br.select_form("Form1")
    br.set_all_readonly(False)
    dt = 'dgResults$ctl' + str(d) + '$ctl00'
#    print dt

    br["__EVENTTARGET"] = dt
    br["__EVENTARGUMENT"] = ''
    request = br.click()
    response1 = br1.open(request)
    
    # find the window open hidden in the script
    html1 = response1.read()
#    print html1
    root1 = lxml.html.fromstring(html1)
    rest_name = root1.cssselect("span#lblName")[0].text
    rest_address = root1.cssselect("span#lblAddress")[0].text
    cityStateZip = root1.cssselect("span#lblCityStateZip")[0].text
    city = re.split(",", cityStateZip)[0]
    rest_inspectionDate = root1.cssselect("span#lblLastInspection")[0].text
    if rest_inspectionDate == " ":
        date = ""
    else:
        date = re.split(":", rest_inspectionDate)[1].strip()
    violations = parseViolations(html1)
#    print violations

    scraperwiki.sqlite.save(unique_keys=["dt"], data={"dt": dt + "_" + zip + "_" + str(datetime.date.today()), "name": rest_name, "address": rest_address, "city": city, "state":"NY", "zip": zip, "inspection_date": date, "violations": violations, "time_scraped":datetime.datetime.now(), "page_id" : dt})

def parseViolations(t):
    soup = BeautifulSoup(t)
    table = soup.find(id="Table2")
    #print table.tr.text
    if table.tr.text == "No posted critical violations were found.&nbsp;":
        v = "{}"
        return v
    else:
        v = '{"violations": ['
        vtable = table.find(id="dgViolations")
        i = 0
        for tr in vtable:
            if i > 1:
                v += "{"
                c = 0
                for td in tr:
                    if type(td).__name__ is 'Tag':
                        if c % 2 == 0:
                            v += '"violation": "'
                        else:
                            v += '"status": "'
                        v += td.text
                        v += '"'
                        if c % 2 == 1:
                            v += ','
                    c += 1
                v+= "},"
            i += 1
        v += "]}"
        return v

Main()


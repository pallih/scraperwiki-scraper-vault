"""This doesn't work on ScraperWiki because of the SSL; run it locally instead.
Use these commands to return the appropriately formatted CSV file.

SELECT
  `date_scraped`,
  "Standard Bank" as "source",
  "Bank" as "source-type",
  "Standard Bank" as entity,
  "Bank" as "entity-type",
  `location-type` as "location-type",
  "http://locator.standardbank.co.za/Default.aspx" as "url",
  `StreetName` as "street-address",
  `TownName` as "town",
  `provinceName` as "province",
  `StreetName` || "\n" || `TownName` || "\n" || `provinceName` as "full-address",
  "South Africa" as "country"
FROM branches
LIMIT 3;

"""

from mechanize import Browser
from lxml.html import fromstring
from requests import post
from json import loads

from highwall import Highwall
h = Highwall()
def save(a, b, c):
    h.insert(b, c)

def options(parentnode,ignore_first=False,ignore_value=None,ignore_text=None,textname="text",valuename="value"):
    """
    Provide a list of option nodes. Receive parent of values and text()s.
    The node list can be an lxml nodes or a text representation.
    In either case, all child option tags will be used.

    You may specify that the first node, the node with a particular value or the node with a particular text be ignored.
    """
    if type(parentnode)==str:
        parentnode=fromstring(parentnode)

    if ignore_first!=None:
        nodes=parentnode.xpath('option[position()>1]')
    elif ignore_value!=None:
        nodes=parentnode.xpath('option[@value!="%s"]'%ignore_value)
    elif ignore_text!=None:
        nodes=parentnode.xpath('option[text()!="%s"]'%ignore_text)
    else:
        nodes=parentnode.xpath('option')

    return [{textname:node.text,valuename:node.xpath('attribute::value')[0]} for node in nodes]

from time import time, sleep
JUNK=('\t','\n','\r','$',':','.','*',',','(',')',';')
SPACES=(' ',u'\xa0')
import re

def keyify(key):
    #Long spaces
    key=re.sub(r'  +',' ',key)

    #Spaces
    for s in SPACES:
        key=key.replace(s,'_')

    #Junk
    for j in JUNK:
        key=key.replace(j,'')

    key=key.replace('#','num').replace('/','_or_').replace('&','and')

    return key


def randomsleep():
    pass

DATE=time()

def getlocations(thingId):
    b=StandardBankBrowser()
    b.open_menu(thingId)

    d=[]

    provinces=b.get_provinces()
    print provinces
    for province in provinces:
        randomsleep()
        b.select_province(province['provinceId'])
        cities=b.get_cities()
        for city in cities:
            print city
            randomsleep()
            b.select_city(city['cityId'])
            branches=get_branches(province['provinceId'],city['cityId'],thingId)
            for branch in branches:
                print branch
                randomsleep()
                branch.update(city)
                branch.update(province)
                branch['date_scraped']=DATE
                branch['locationtype'] = {
                    "1": "ATM",
                    "2": "Branch",
                    "3": "Foreign Exchange",
                }[thingId]
                del(branch['id'])
                del(branch['cityId'])
                del(branch['ProvinceId'])
                save([],branch,'branches_backup')
                d.append(branch)
    save([],d, 'branches')


class StandardBankBrowser(Browser):
    def __init__(self):
        Browser.__init__(self)
        self.addheaders=[("User-agent","Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7")]
        self._factory.is_html=True

    def easy_open(self,url):
        self.r=self.open(url).read()
        self.on_open()

    def easy_submit(self):
    # self.r=self.submit().read()
        request=self.form.click()
        self.open(request)
        self.r=self.response().read()
    # while True:
    #     try:
    #         self.r=self.submit().read()
    #     except Exception, m:
    #         print m
    #         sleep(60)
        self.on_open()

    def easy_select_form(self,*args,**kwargs):
        self.select_form(*args,**kwargs)
        self.set_all_readonly(False)

    def on_open(self,form="FormMaps"):
        self.x=fromstring(self.r)
        self.easy_select_form(form)

    def doPostBack(self,eventTarget,eventArgument):
        self['__EVENTTARGET'] = eventTarget
        self['__EVENTARGUMENT'] = eventArgument
        self.easy_submit()

    def open_menu(self, thingId = '2' ):
        self.easy_open("http://locator.standardbank.co.za/Default.aspx")

        self['LocatorDropDown']=[ thingId ] #Branch, ATM or Forex
        self.doPostBack('LocatorDropDown','')

    def asp_select(self,field,value):
        self[field]=[value]
        self.doPostBack(field,'')
        self.easy_submit()

    def get_provinces(self):
        return options(self.x.get_element_by_id("RegionDropDownList"),ignore_text="Select Province",valuename="provinceId",textname="provinceName")

    def select_province(self,provinceId):
        self.asp_select("RegionDropDownList",provinceId)

    def get_cities(self):
        return options(self.x.get_element_by_id("CityDropDownList"),ignore_text="Select City",valuename="cityId",textname="cityName")

    def select_city(self,cityId):
        self.asp_select("CityDropDownList",cityId)


def get_branches(provinceId,cityId,thingId):
    json=getMapData(provinceId,cityId,thingId).content
    try:
        d_orig=loads(loads(json)['d'])
    except ValueError:
        #No branches
        return []
    else:
        d_clean=[]
        for row_orig in d_orig:
            row_clean={}
            for key in row_orig:
                row_clean[keyify(key)]=row_orig[key]
            d_clean.append(row_clean)
        return d_clean

def getMapData(provinceId,cityId,thingId):
    "The GetMapData controller expects a plain json rather than a proper query string."
    while True:
        try:
            return post(
                "http://locator.standardbank.co.za/Default.aspx/GetMapData"
            , data='{"ProvinceValue":"%s","CityValue":"%s","SuburbValue":"","LocatorType":%s}' % (provinceId,cityId, thingId)
            , headers={
                "Content-Type":"application/json; charset=UTF-8"
            })
        except:
            sleep(60)
# Testing
#print get_branches('7','711')

if __name__ == '__main__':
    # If this is run locally, actually run it.
    getlocations('1')
    getlocations('2')
    getlocations('3')
elif __name__ == 'scraper':
    # If this is run on scraperwiki, just create the schema.
    from scraperwiki.sqlite import execute, commit
    execute('CREATE TABLE IF NOT EXISTS branches ( City TEXT, Latitude TEXT, Longitute TEXT, Status TEXT, SuburdId TEXT, TownName TEXT, Address1 TEXT, Address2 TEXT, EntityType TEXT, EntityCentreNumber TEXT, ProvinceId TEXT, RegionName TEXT, Province TEXT, EntityTypeOptionId TEXT, OperatingHoursWeekend TEXT, EntityName TEXT, EntitySwiftCode TEXT, IBTNumber TEXT, EntityTypeId TEXT, OperatingHoursWeekDay TEXT, DateAdded TEXT, EntityTypeOption TEXT, AddedBy TEXT, CityId TEXT, SuburdSuburb TEXT, EntityDescription TEXT, Guid TEXT, Id TEXT, StreetName TEXT )')
    execute('CREATE TABLE IF NOT EXISTS branches_backup ( City TEXT, Latitude TEXT, Longitute TEXT, Status TEXT, SuburdId TEXT, TownName TEXT, Address1 TEXT, Address2 TEXT, EntityType TEXT, EntityCentreNumber TEXT, ProvinceId TEXT, RegionName TEXT, Province TEXT, EntityTypeOptionId TEXT, OperatingHoursWeekend TEXT, EntityName TEXT, EntitySwiftCode TEXT, IBTNumber TEXT, EntityTypeId TEXT, OperatingHoursWeekDay TEXT, DateAdded TEXT, EntityTypeOption TEXT, AddedBy TEXT, CityId TEXT, SuburdSuburb TEXT, EntityDescription TEXT, Guid TEXT, Id TEXT, StreetName TEXT )')
    commit()
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup

# Blank Python

city_list = ['North_Carolina/Winston_Salem/27101','Pennsylvania/Chambersburg/17201','Washington/College_Place/99324','Louisiana/New_Orleans/70126','Georgia/Gainesville/30501','Louisiana/New_Orleans/70122','Maine/Augusta/04330','Pennsylvania/Lehman/18627','Tennessee/Memphis/38126','Texas/Houston/77006','Georgia/Marietta/30060','Tennessee/Nashville/37208','Virginia/Staunton/24401','South_Carolina/Denmark/29042','District_of_Columbia/Washington/20017','Missouri/Columbia/65216','Pennsylvania/York/17403','Florida/Temple_Terrace/33617','Michigan/Dearborn/48128','Indiana/Westville/46391','Maine/Fort_Kent/04743','Massachusetts/Amherst/01002','Texas/Terrell/75160','Wisconsin/Milwaukee/53222','Missouri/Point_Lookout/65726','Indiana/Hammond/46323','Colorado/Denver/80220','North_Carolina/Raleigh/27604','Vermont/Rutland/05701','Nebraska/Omaha/68108','Pennsylvania/Upper_Burrell/15068','Wisconsin/Manitowoc/54220','Pennsylvania/Bryn_Athyn/19009','Pennsylvania/Dubois/15801','California/Angwin/94508','Missouri/Columbia/65215','Louisiana/Alexandria/71302','Texas/Dallas/75241','New_York/Flushing/11369','Washington/Everett/98201','Arkansas/Little_Rock/72202','Pennsylvania/Summerdale/17093','Texas/Hawkins/75765','South_Carolina/Columbia/29204','Michigan/Grand_Rapids/49525','North_Carolina/Charlotte/28202','Nebraska/Lincoln/68506','Nevada/Incline_Village/89451','Indiana/South_Bend/46634','Tennessee/Nashville/37205','Maryland/Annapolis/21401','Connecticut/Southington/06489','New_Mexico/Espanola/87532','Indiana/Gary/46408','Ohio/Wilberforce/45384','Pennsylvania/Center_Valley/18034','Georgia/Marietta/30060','Tennessee/Memphis/38111','North_Carolina/Elizabeth_City/27909']

#print list[0]

for thisCity in city_list:
    print thisCity



#print list[1]

    try:
        page = urllib2.urlopen("http://bestplaces.net/climate/zip-code/" + thisCity)

        soup = BeautifulSoup(page)

        table_one = soup.findAll("table")[1]

        precipitation_days = table_one.findAll("td")[10] #precipitation days
        print precipitation_days

        comfort_index = table_one.findAll("td")[22] #comfort index
        print comfort_index

        

        
    
    except  (IndexError):
         print "Oops! Try again..."
    
    

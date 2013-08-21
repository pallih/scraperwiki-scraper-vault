import scraperwiki
import mechanize
import re
from lxml import etree
from lxml.cssselect import CSSSelector
import scraperwiki            

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

def testdata( ):
    data = [
            '-- Please Select Code --', 
            '9900 - Extra-territorial organizations and bodies\t\t',
            '9305 - Other service activities nec.', 
            '9304 - Physical well-being activities'
            ]
    scraperwiki.sqlite.save_var('activitiesTEST', data)
    
#testdata()

def getActivitiesData () :
    url = 'http://www.arbk.org/arbk/KerkimiBizneseve/tabid/66/language/en-US/Default.aspx?state=NY&rp='
    br = mechanize.Browser()

    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)

    html = response.read()
    doc = etree.HTML(html)
    #title = doc.xpath('//select[@name='dnn$ctr437$ViewBizneset$ddlAktivitetetTjera']0].text
    #activities = 
    #scraperwiki.sqlite.save_var('activities_list', activities)
    
    scraperwiki.sqlite.execute("delete from activities") 

    for item in doc.xpath('//tr/td/select[@name="dnn$ctr437$ViewBizneset$ddlAktivitetiKryesor"]/option/text()') :
        if item != '-- Please Select Code --':           
            m = re.search('(\d+)\s\-\s(.+)', item)
            holdActivities = {}
            holdActivities["id"]=m.group(1)
            holdActivities["name"]=m.group(2)
            scraperwiki.sqlite.save(unique_keys=["id"], table_name="activities", data=holdActivities)

#    print holdActivities
 
#def processActivities() :
    #activities = scraperwiki.sqlite.get_var('activities_list')
    #for item in activities :
#        print item
#getActivitiesData()
#processActivities()

#getActivitiesData()

#def savedata () :
##businesses 
#    scraperwiki.sqlite.save("activities",activities)


def read_buisness_type () :

    select_ViewBizneset_ddlAktivitetetTjera=  "dnn$ctr437$ViewBizneset$ddlAktivitetetTjera";

#      <select style="width: 200px;" id="dnn_ctr437_ViewBizneset_ddlAktivitetetTjera" name="dnn$ctr437$ViewBizneset$ddlAktivitetetTjera">
#                        <option value="Z" selected="selected">-- Please Select Code --</option>
#                        <option value="9900">9900 - Extra-territorial organizations and bodies                </option>


def submit_start_search_button () :
    url = 'http://www.arbk.org/arbk/KerkimiBizneseve/tabid/66/language/en-US/Default.aspx?state=NY&rp='
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.2')]
    print "going to open"    
    response = br.open(url)

    br.select_form(name='Form')
    br.form.set_all_readonly(False)
    # Post to url 
    # TODO for ardian 
    br['__EVENTTARGET'] = 'dnn$ctr437$ViewBizneset$btnKerko'
    br['__EVENTARGUMENT'] = ''


    # fill them out dnn$ctr437$ViewBizneset$txtNrReg:
    br['dnn$ctr437$ViewBizneset$txtEmriBiz']='aa' ##/// we nee dhtat
    br['dnn$ctr437$ViewBizneset$txtNrLet']=''
    br['dnn$ctr437$ViewBizneset$txtNrLetPronarit']=''
    #br['dnn$ctr437$ViewBizneset$ddlAktivitetiKryesor']='9305'
    br.find_control(name='dnn$ctr437$ViewBizneset$ddlAktivitetiKryesor').value = ['9305']
    br.find_control(name='dnn$ctr437$ViewBizneset$ddlAktivitetetTjera').value = ['Z']
    print "going to submit"    
    response = br.submit()
    html = response.read()
    print html

    scraperwiki.sqlite.save_var('examplePage', html)
    
#ScrollTop:
    #__dnnVariable:dnn$ctr437$ViewBizneset$btnKerko:Search
    #ScriptManager:dnn$ctr437$ViewBizneset_UP|dnn$ctr437$ViewBizneset$btnKerko
    #_EVENTTARGET:
    #__EVENTARGUMENT:
    #__VIEWSTATE:  MONSTER TEXT ....

    #<input
    # id="dnn_ctr437_ViewBizneset_btnKerko"
    # type="submit"
    # onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("dnn$ctr437$ViewBizneset$btnKerko", "", true, "", "", false, false))"
    # value="Search"
    # name="dnn$ctr437$ViewBizneset$btnKerko">
    



# call it
#submit_start_search_button ()

def parse_data () :
    print "going to open"    
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.2')]
  #  response = br.open('http://pastebin.com/raw.php?i=RKb9NGts')    
    html = "response.read()"
    print     html

parse_data ();

# when we get the results ..... do the for loop!
def visitpages () :    
    for pagenum in range(10):
        html = response.read()
        print "Page %d  page length %d" % (pagenum, len(html))
        print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)

        mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
        if not mnextlink:
            break

        br.select_form(name='ctl00')
        br.form.set_all_readonly(False)
        br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
        br['__EVENTARGUMENT'] = ''
        response = br.submit()


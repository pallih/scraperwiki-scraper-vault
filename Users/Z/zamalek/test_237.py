import scraperwiki
import mechanize
import cookielib
from BeautifulSoup import MinimalSoup

class PrettifyHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            #soup = BeautifulSoup(response.get_data())
            soup = MinimalSoup (response.get_data())            
            #print html
            #allHTML = soup.findAll('html')
            #print allHTML
            response.set_data(soup.prettify())
        return response

def GetContent():

    # Browser
    #br = mechanize.Browser()
    #br = mechanize.Browser(factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True))
    br = mechanize.Browser(factory=mechanize.RobustFactory())

    br.add_handler(PrettifyHandler())

    # Cookie Jar
    #cj = cookielib.LWPCookieJar()
    #br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    br.open('http://www.zvg-portal.de/index.php?button=Termine%20suchen')

    for form in br.forms():
        print "Form name:", form.name
        print form
    
    br.select_form(name='globe')
    #br.select_form("globe")         # works when form has a name
    #br.form = list(br.forms())[0]  # use when form is unnamed

    #Tests
    for control in br.form.controls:
        print control
        #print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])

    br.form["land_abk"] = "by"

    # Login
    br.submit()

    return br.response().read()

GetContent()

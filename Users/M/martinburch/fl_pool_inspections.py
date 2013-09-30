import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

uri = "http://b3.caspio.com/dp.asp?appSession=718251683844642"

class PrettifyHandler(mechanize.BaseHandler):
    """
    Shamelessly stolen from this stackoverflow answer:
    http://stackoverflow.com/questions/1782368/is-it-possible-to-hook-up-a-more-robust-html-parser-to-python-mechanize/5039584#5039584
    """
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = BeautifulSoup(response.get_data())
            response.set_data(soup.prettify())
        return response

def createBrowser():
    br = mechanize.Browser(factory=mechanize.RobustFactory())  # Create Browser
    br.add_handler(PrettifyHandler())
    cj = cookielib.LWPCookieJar()  # Create Cookie Jar
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)  # Browser Options
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(True)
    br.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(),
        max_time=1
    )
    br.set_debug_http(False)  # DEBUG settings
    br.set_debug_redirects(True)
    br.set_debug_responses(True)
    br.addheaders = [
    (
        'User-agent',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    )
    ]
    return br


br = createBrowser()

br.open(uri)
for form in br.forms():
    print form
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

uri = "http://b3.caspio.com/dp.asp?appSession=718251683844642"

class PrettifyHandler(mechanize.BaseHandler):
    """
    Shamelessly stolen from this stackoverflow answer:
    http://stackoverflow.com/questions/1782368/is-it-possible-to-hook-up-a-more-robust-html-parser-to-python-mechanize/5039584#5039584
    """
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = BeautifulSoup(response.get_data())
            response.set_data(soup.prettify())
        return response

def createBrowser():
    br = mechanize.Browser(factory=mechanize.RobustFactory())  # Create Browser
    br.add_handler(PrettifyHandler())
    cj = cookielib.LWPCookieJar()  # Create Cookie Jar
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)  # Browser Options
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(True)
    br.set_handle_refresh(
        mechanize._http.HTTPRefreshProcessor(),
        max_time=1
    )
    br.set_debug_http(False)  # DEBUG settings
    br.set_debug_redirects(True)
    br.set_debug_responses(True)
    br.addheaders = [
    (
        'User-agent',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
    )
    ]
    return br


br = createBrowser()

br.open(uri)
for form in br.forms():
    print form

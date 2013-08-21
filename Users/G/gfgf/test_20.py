import httplib2
import urllib
import urllib2
from cookielib import CookieJar
import sys
import re
from HTMLParser import HTMLParser

class miniHTMLParser( HTMLParser ):

  viewedQueue = []
  instQueue = []
  headers = {}
  opener = ""

  def get_next_link( self ):
    if self.instQueue == []:
      return ''
    else:
      return self.instQueue.pop(0)


  def gethtmlfile( self, site, page ):
    try:
        url = 'http://'+site+''+page
        response = self.opener.open(url)
        return response.read()
    except Exception, err:
        print " Error retrieving: "+page
        sys.stderr.write('ERROR: %s\n' % str(err))
    return "" 

    return resppage

  def loginSite( self, site_url ):
    try:
     cj = CookieJar()
     self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

     url = 'http://'+site_url 
     params = {'name': 'customer_admin', 'pass': 'customer_admin123', 'opt': 'Log in', 'form_build_id': 'form-3560fb42948a06b01d063de48aa216ab', 'form_id':'user_login_block'}
     user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
     self.headers = { 'User-Agent' : user_agent }

     data = urllib.urlencode(params)
     response = self.opener.open(url, data)
     print "Logged in"
     return response.read() 

    except Exception, err:
     print " Error logging in"
     sys.stderr.write('ERROR: %s\n' % str(err))

    return 1

  def handle_starttag( self, tag, attrs ):
    if tag == 'a':
      newstr = str(attrs[0][1])
      print newstr
      if re.search('http', newstr) == None:
        if re.search('mailto', newstr) == None:
          if re.search('#', newstr) == None:
            if (newstr in self.viewedQueue) == False:
              print "  adding", newstr
              self.instQueue.append( newstr )
              self.viewedQueue.append( newstr )
          else:
            print "  ignoring", newstr
        else:
          print "  ignoring", newstr
      else:
        print "  ignoring", newstr


def main():

  if len(sys.argv)!=3:
    print "usage is ./minispider.py site link"
    sys.exit(2)

  mySpider = miniHTMLParser()

  site = sys.argv[1]
  link = sys.argv[2]

  url_login_link = site+"/node?destination=node"
  print "\nLogging in", url_login_link
  x = mySpider.loginSite( url_login_link )

  while link != '':

    print "\nChecking link ", link

    # Get the file from the site and link
    retfile = mySpider.gethtmlfile( site, link )

    # Feed the file into the HTML parser
    mySpider.feed(retfile)

    # Search the retfile here

    # Get the next link in level traversal order
    link = mySpider.get_next_link()

  mySpider.close()

  print "\ndone\n"

if __name__ == "__main__":
  main()
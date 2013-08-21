from lxml.html import fromstring,tostring
from requests import get,post,session
from mechanize import Browser
from urllib import urlencode

URLS={
  "menu":"http://apps.suffolkcountyny.gov/health/Restaurant/Rest_Search.aspx"
, "search":"http://apps.suffolkcountyny.gov/health/Restaurant/Restaurant_Info.aspx"
, "result":"http://apps.suffolkcountyny.gov/health/Restaurant/Restaurant_Violation.aspx"
}

def main():
    b=Browser()
    b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    


def main1():
    b=ASPBrowser()
    b.get(URLS['menu'])
    print b.viewstate()
    print b.eventvalidation()
    b.search(URLS['search'])
    print b.r.content
    #b.restaurant()


class ASPBrowser():
    def __init__(self):
        self.s=session()
        self.s.headers['User-Agent']='Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7'

    def get(self,url):
        self.r=self.s.get(url)
        self.x=fromstring(self.r.content)

    def viewstate(self):
        return self.x.xpath('id("__VIEWSTATE")/@value')[0]

    def eventvalidation(self):
        return self.x.xpath('id("__EVENTVALIDATION")/@value')[0]

    def search(self,url):
        params=urlencode({
          "ddl_Town":""
        , "txt_Rest_Name":""
        , "btnViewDBA_Name":"View Establishment"
        , "ddl_Town2":""
        , "txt_Rest_Name_2":""
        })
        params+='&__VIEWSTATE='+self.viewstate()+"&__EVENTVALIDATION="+self.eventvalidation()
        self.r=self.s.post(url,params,allow_redirects=True)
        self.x=fromstring(self.r.content)

    def restaurant(self,eventtarget="dgResults$ctl4697$ctl00"):
        r=self.s.post(URLS['result'],{
          "__EVENTTARGET":eventtarget
        , "__EVENTARGUMENT":""
        , "__VIEWSTATE":self.viewstate()
        })

main()
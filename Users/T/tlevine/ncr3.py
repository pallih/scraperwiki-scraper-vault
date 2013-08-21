from requests import session
from lxml.html import fromstring,tostring

def load():
  "Download the webpage"
  s=session()
  s.get("http://www.ncr.org.za/register_of_registrants/index.php")
  r=s.post("http://www.ncr.org.za/register_of_registrants/index.php"
  , data={
      "_submit_check_":"1"
    , "ns_BType":"CP1"
    , "ns_SearchText":"*"
    , "ns_Town":"All"
    , "submit.x":"20"
    , "submit.y":"37"
    , "submit":"Search"
    , "ns_cancel":"registered"
  }
  , headers={
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    , "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
    , "Accept-Encoding":"gzip,deflate,sdch"
    , "Accept-Language":"en-US,en;q=0.8"
    , "Cache-Control":"max-age=0"
    , "Connection":"keep-alive"
    , "Content-Length":"116"
    , "Content-Type":"application/x-www-form-urlencoded"
    , "Host":"www.ncr.org.za"
    , "Origin":"http://www.ncr.org.za"
    , "Referer":"http://www.ncr.org.za/register_of_registrants/index.php"
    , "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11"
  })
  return fromstring(r.content)

x=load()
print tostring(x)
print x.xpath('//*[text()="Trading Name : "]')

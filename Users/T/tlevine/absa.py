"""
How this site works
==========
Mortals access the data through [this page](http://www.absa.co.za/Absacoza/Contact-Us).

1. Inside that page is an [iframe](https://e91.absa.co.za/esl/locatorEnquiry.do?state=promptSelectService).
2. Submitting that iframe returns some junk, including some javascript that redirects you to
3. [this page](https://e91.absa.co.za/esl/locatorResult.do), which uses cookies to identify the search request.

"""
from time import time,sleep
from requests import session

IFRAME="https://e91.absa.co.za/esl/locatorEnquiry.do?state=promptSelectService"
RESULTS="https://e91.absa.co.za/esl/locatorResult.do"

def main():
  s=session()
  s.headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
  , "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
  , "Accept-Encoding":"gzip,deflate,sdch"
  , "Accept-Language":"en-US,en;q=0.8"
  , "Cache-Control":"max-age=0"
  , "Connection":"keep-alive"
  , "Content-Type":"application/x-www-form-urlencoded"
  , "Host":"e91.absa.co.za"
  , "Origin":"https://e91.absa.co.za"
  , "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7"
  }

  #Set cookies
  s.get(IFRAME)

  #Request
  s.post(IFRAME,{
     "City":"BEAUFORT WEST"
   , "Service":"branch"
   , "Province":"EC"
  })

  #Retrieve
  sleep(2)
  s.headers["Referer"]="https://e91.absa.co.za/esl/locatorEnquiry.do?state=promptSelectService"
  r=s.get(RESULTS)
  print r.content


main()
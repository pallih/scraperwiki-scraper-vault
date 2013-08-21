import scraperwiki
import lxml.html
import os
import requests

doc = lxml.html.fromstring(requests.get('http://www.cftc.gov/LawRegulation/DoddFrankAct/ExternalMeetings/index.htm').content)
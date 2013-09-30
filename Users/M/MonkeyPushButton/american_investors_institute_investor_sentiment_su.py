import scraperwiki
import lxml.html
import datetime
from datetime import datetime  

html = scraperwiki.scrape("http://www.aaii.com/SentimentSurvey")
root = lxml.html.fromstring(html) 

# Data represents what direction members feel the stock market will be in the next 6 months
i = 0;
for el in root.cssselect("span.surveyNumber"): 
    if el.text[len(el.text) - 1] == "%":
        if i == 0:
            bullish = el.text.strip().replace("%", "")
        if i == 1:
            neutral = el.text.strip().replace("%", "")
        if i == 2:
            bearish = el.text.strip().replace("%", "")
        i = i + 1

print bullish
print neutral 
print bearish 

index = html.index("Week ending")
print index 
date = html[index + 11:index + 21].strip()
print date 

date_object = datetime.strptime(date, '%m/%d/%Y')

scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"bullish", "survey_percentage":bullish})
scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"neutral", "survey_percentage":neutral})
scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"bearish", "survey_percentage":bearish})

import scraperwiki
import lxml.html
import datetime
from datetime import datetime  

html = scraperwiki.scrape("http://www.aaii.com/SentimentSurvey")
root = lxml.html.fromstring(html) 

# Data represents what direction members feel the stock market will be in the next 6 months
i = 0;
for el in root.cssselect("span.surveyNumber"): 
    if el.text[len(el.text) - 1] == "%":
        if i == 0:
            bullish = el.text.strip().replace("%", "")
        if i == 1:
            neutral = el.text.strip().replace("%", "")
        if i == 2:
            bearish = el.text.strip().replace("%", "")
        i = i + 1

print bullish
print neutral 
print bearish 

index = html.index("Week ending")
print index 
date = html[index + 11:index + 21].strip()
print date 

date_object = datetime.strptime(date, '%m/%d/%Y')

scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"bullish", "survey_percentage":bullish})
scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"neutral", "survey_percentage":neutral})
scraperwiki.sqlite.save(unique_keys=["survey_date", "mood"], data={"survey_date":date_object, "mood":"bearish", "survey_percentage":bearish})


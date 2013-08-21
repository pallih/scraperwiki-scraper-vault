import scraperwiki

scraperwiki.sqlite.attach("bookingcom_review_checking")
data = scraperwiki.sqlite.select("* FROM bookingcom_review_checking.swdata ORDER BY Date DESC LIMIT 2")
lastreviews = data[0]["Nr.of Reviews"]
previousreviews = data[1]["Nr.of Reviews"]
#print lastreviews, previousreviews
if lastreviews != previousreviews:
    newreviews = lastreviews-previousreviews
    print 'Od zadnjega preverjanja dne %s do danasnjega preverjanja dne %s se je pojavilo %i novih ocen.' %(data[1]["Date"], data[0]["Date"], newreviews)

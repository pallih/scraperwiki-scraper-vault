import scraperwiki.utils
import datetime

swiftlg = scraperwiki.utils.swimport("swift-lg-planning-application-library")

parser = swiftlg.SwiftLGParser("Fingal County Council", "Fingal", "http://planning.fingalcoco.ie/swiftlg/apas/run/wphappcriteria.display")

#results = parser.getResultsRaw(12,6,2009)
#results.save()

today = datetime.date.today()
for i in range(14):
    day = today - datetime.timedelta(days=i)
    parser.saveResults(day.day, day.month, day.year)



import scraperwiki.utils
import datetime

swiftlg = scraperwiki.utils.swimport("swift-lg-planning-application-library")

parser = swiftlg.SwiftLGParser("Dun Laoghaire-Rathdown CC", "DLR", "http://planning.dlrcoco.ie/swiftlg/apas/run/wphappcriteria.display")

# results = parser.getResultsRaw(11,10,2010)
# results.save()

today = datetime.date.today()
for i in range(365):
   day = today - datetime.timedelta(days=i)
   parser.saveResults(day.day, day.month, day.year)

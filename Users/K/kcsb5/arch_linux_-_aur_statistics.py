import scraperwiki 
import lxml.html
import datetime

# keep a reference to the scraping date
curDate  = datetime.datetime.now()
arch_linux_aur_statistics_html = scraperwiki.scrape("https://aur.archlinux.org/?setlang=en")
# parse root node from the HTML source
root = lxml.html.fromstring(arch_linux_aur_statistics_html) 
nr_records = 1

# select the AUR statistics table in the DOM tree by using a CSS selector
for tableRow in root.cssselect("div#pkg-stats tr"): 

    aurStatisticsItem = { 
        # the current name of the statistic is given by the content of the <td class="stat-desc"> tag
        'statisticItemId'   : tableRow.cssselect("td.stat-desc")[0].text_content() , 
        # the actual statistic may be found in the sibling <td> tag
        'statisticItemVal'  : tableRow.cssselect("td.stat-desc + td")[0].text_content(),
        # keep the actual scraping date for future reference
        'statisticItemDate' : curDate.strftime("%s"),
        'statisticKeyId' : nr_records} 
    scraperwiki.sqlite.save(unique_keys=["statisticKeyId","statisticItemDate"], data=aurStatisticsItem, table_name="aur_statistics", verbose=2)
    nr_records += 1

import scraperwiki 
import lxml.html
import datetime

# keep a reference to the scraping date
curDate  = datetime.datetime.now()
arch_linux_aur_statistics_html = scraperwiki.scrape("https://aur.archlinux.org/?setlang=en")
# parse root node from the HTML source
root = lxml.html.fromstring(arch_linux_aur_statistics_html) 
nr_records = 1

# select the AUR statistics table in the DOM tree by using a CSS selector
for tableRow in root.cssselect("div#pkg-stats tr"): 

    aurStatisticsItem = { 
        # the current name of the statistic is given by the content of the <td class="stat-desc"> tag
        'statisticItemId'   : tableRow.cssselect("td.stat-desc")[0].text_content() , 
        # the actual statistic may be found in the sibling <td> tag
        'statisticItemVal'  : tableRow.cssselect("td.stat-desc + td")[0].text_content(),
        # keep the actual scraping date for future reference
        'statisticItemDate' : curDate.strftime("%s"),
        'statisticKeyId' : nr_records} 
    scraperwiki.sqlite.save(unique_keys=["statisticKeyId","statisticItemDate"], data=aurStatisticsItem, table_name="aur_statistics", verbose=2)
    nr_records += 1


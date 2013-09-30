import lxml.html
import scraperwiki
import time

watch_log_html = scraperwiki.scrape('http://www.iowa-city.org/icgov/apps/police/neighborhood.asp')
watch_log_doc = lxml.html.fromstring(watch_log_html)

watch_log_rows = watch_log_doc.xpath("//table/tbody/tr")

watch_log_list = []

for row in watch_log_rows:
    try: 
        log_dict = {}
        log_dict["incidentnum"] = int(row.xpath('td')[0].xpath("a")[0].text_content())
        log_dict["activitycode"] = row.xpath('td')[1].text_content()
        if log_dict["activitycode"] != "":
               log_dict["activitycode"] = int(log_dict["activitycode"])
        else:
               log_dict["activitycode"] = 0
        log_dict["activitytype"] = row.xpath('td')[2][0].text_content()
        log_dict["location"] = row.xpath("td")[3].text_content()
        log_dict["timereported"] = time.mktime(time.strptime(row.xpath("td")[4].text_content(),"%m/%d/%Y %I:%M:%S %p"))
                
        watch_log_list.append(log_dict)
    except IndexError:
        pass

for watch_log in watch_log_list:
    scraperwiki.sqlite.save(['incidentnum'], watch_log, table_name='iowa_city_neighborhood_watch')
import lxml.html
import scraperwiki
import time

watch_log_html = scraperwiki.scrape('http://www.iowa-city.org/icgov/apps/police/neighborhood.asp')
watch_log_doc = lxml.html.fromstring(watch_log_html)

watch_log_rows = watch_log_doc.xpath("//table/tbody/tr")

watch_log_list = []

for row in watch_log_rows:
    try: 
        log_dict = {}
        log_dict["incidentnum"] = int(row.xpath('td')[0].xpath("a")[0].text_content())
        log_dict["activitycode"] = row.xpath('td')[1].text_content()
        if log_dict["activitycode"] != "":
               log_dict["activitycode"] = int(log_dict["activitycode"])
        else:
               log_dict["activitycode"] = 0
        log_dict["activitytype"] = row.xpath('td')[2][0].text_content()
        log_dict["location"] = row.xpath("td")[3].text_content()
        log_dict["timereported"] = time.mktime(time.strptime(row.xpath("td")[4].text_content(),"%m/%d/%Y %I:%M:%S %p"))
                
        watch_log_list.append(log_dict)
    except IndexError:
        pass

for watch_log in watch_log_list:
    scraperwiki.sqlite.save(['incidentnum'], watch_log, table_name='iowa_city_neighborhood_watch')

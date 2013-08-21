import scraperwiki
import re
import urllib
import lxml.etree

url=("http://www.sem-o.com/marketdata/Pages/PricingAndScheduling.aspx")
response = scraperwiki.scrape(url)

XMLfiles=re.findall(r"INITIAL SMPS\w+[.]XML",response)
XMLfiles+=re.findall(r"EX-POST INITIAL SHADOW PRICES\w+[.]XML",response)
XMLfiles+=re.findall(r"COMMERCIAL OFFER DATA - STANDARD GENERATOR UNIT\w+[.]XML",response)
XMLfiles+=re.findall(r"COMMERCIAL OFFER DATA - STANDARD DEMAND SITE UNIT\w+[.]XML",response)
XMLfiles+=re.findall(r"COMMERCIAL OFFER DATA - INTERCONNECTOR UNITS\w+[.]XML",response)
XMLfiles+=re.findall(r"TRADING DAY EXCHANGE RATE\w+[.]XML",response)
XMLfiles+=re.findall(r"SO INTERCONNECTOR TRADES\w+[.]XML",response)
XMLfiles+=re.findall(r"EX-POST INITIAL MARKET SCHEDULE QUANTITY\w+[.]XML",response)
XMLfiles+=re.findall(r"DISPATCH INSTRUCTIONS\w+[.]XML",response)
XMLfiles+=re.findall(r"INTERCONNECTOR ATC\w+[.]XML",response)


#Remove duplicates
XMLset = set(XMLfiles)

print XMLset
fullurl=("http://www.sem-o.com/MarketReports/StaticReports/")

for link in XMLset:
    xmlLink = fullurl+urllib.quote(link)
    
    xml_data = scraperwiki.scrape(fullurl+urllib.quote(link))
    root = lxml.etree.fromstring(xml_data)
    
    report_name = root.find("./REPORT_HEADER/HEADROW/REPORT_NAME").text
    report_date = root.find("./REPORT_HEADER/HEADROW/RPT_DATE").text
    report_data = "PARSE SOME DATA FROM THE XML FIILE"

    scraperwiki.sqlite.save(unique_keys=["rpt_date", "report_name"], data={"rpt_date":report_date, "report_name":report_name, "data":report_data})



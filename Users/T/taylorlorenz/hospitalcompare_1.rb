# Blank Ruby
require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

# get the hid's for all NYC hospitals
# Assuming that all the NY hospitals are listed with a search parameter of 25 mile radius from lat=40.7602619,
# lng=-73.9932872 - These params can be changed by changing the variables below
dist = "25"
lat = "40.7143528"
long = "-74.0059731"
nyhospurl = "http://www.hospitalcompare.hhs.gov/hospital-results.aspx?loc=New%20York,%20NY&lat=" + lat + "&lng=" + long + "&dist=" + dist + "&stateSearched=NY&htype=0&stype=MEDICAL&mcid=GRP_1"
# Lat longs for a hospital can be found at this URL -  http://www.hospitalcompare.hhs.gov/maps/maps-and-directions.aspx?map_id=330064  (Assuming 330064 is an id for a hospital
hospitals = open(nyhospurl)
hospdoc = Nokogiri::HTML(hospitals)
# Get an array of hospital IDs for the list of hospitals
# The table with the list of hospitals is the 1st table in the HTML page
tables = hospdoc.search('table')
# we want to iterate through the rows starting with the second row.
numofhospitals = tables[0].search('tr').count - 1
hospitaldata = tables[0].search('tr')[1..numofhospitals]
hospids = Array.new
hospitaldata.each_with_index do |hosp, i|
  hrefattrib = hosp.search('td')[1].search('a')[0].get_attribute('href')
  pidstrind = hrefattrib.index('pid=') + 4
  hid = hrefattrib[pidstrind..(pidstrind+5)]
  hospital = hosp.search("span")[0].text

  # returns an array with the text before the hospital name in the td string, the hospital name, and the stuff after the hospital name
  hosptext = hosp.text.rpartition(hospital)
  hospital = hosptext[1]
  addressnstuff = hosptext[2].strip
  puts addressnstuff
  addylen = addressnstuff.length
  phonelen = addylen-14
  phone = addressnstuff[phonelen..addylen ]


  # We want the POC data for this hospital
  url = "http://www.hospitalcompare.hhs.gov/tables/hospital-pocQualityTable.aspx?hid=" + hid + "&stype=GENERAL&measureCD=HA&stateSearched=NY&tab=SOC"
  download = open(url)

  doc = Nokogiri::HTML(download)
  trs = doc.search('tr')
  # The hospital name will always be in the first tr row, and the text of the fourth th element
  #hospital = trs[0].search('th')[3].text
  # the percent given aspirin on arrival will always be in the 7th tr row, and the text of the fourth td element 
  percent = trs[6].search('td')[3].text
  # we want tr 6 - thats the data row with the Heart Attack Patients Given Aspirin at Arrival
  measure1 = trs[6].search('td')[0].text

  ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure1, 'Value' => percent})

  # Now to save the data for PCI within 90 min of arrival
  measure2 = trs[12].search('td')[0].text
  pci = trs[12].search('td')[3].text

    ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure2, 'Value' => pci})

  # Now to save the data for Heart Attack Patients Given a Prescription for a Statin at Discharge
  measure2 = trs[13].search('td')[0].text
  pci = trs[13].search('td')[3].text

  ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure2, 'Value' => pci})

# done iterating thru list of hospitals
end
# Blank Ruby
require 'open-uri'
require 'nokogiri'
require 'scraperwiki'

# get the hid's for all NYC hospitals
# Assuming that all the NY hospitals are listed with a search parameter of 25 mile radius from lat=40.7602619,
# lng=-73.9932872 - These params can be changed by changing the variables below
dist = "25"
lat = "40.7143528"
long = "-74.0059731"
nyhospurl = "http://www.hospitalcompare.hhs.gov/hospital-results.aspx?loc=New%20York,%20NY&lat=" + lat + "&lng=" + long + "&dist=" + dist + "&stateSearched=NY&htype=0&stype=MEDICAL&mcid=GRP_1"
# Lat longs for a hospital can be found at this URL -  http://www.hospitalcompare.hhs.gov/maps/maps-and-directions.aspx?map_id=330064  (Assuming 330064 is an id for a hospital
hospitals = open(nyhospurl)
hospdoc = Nokogiri::HTML(hospitals)
# Get an array of hospital IDs for the list of hospitals
# The table with the list of hospitals is the 1st table in the HTML page
tables = hospdoc.search('table')
# we want to iterate through the rows starting with the second row.
numofhospitals = tables[0].search('tr').count - 1
hospitaldata = tables[0].search('tr')[1..numofhospitals]
hospids = Array.new
hospitaldata.each_with_index do |hosp, i|
  hrefattrib = hosp.search('td')[1].search('a')[0].get_attribute('href')
  pidstrind = hrefattrib.index('pid=') + 4
  hid = hrefattrib[pidstrind..(pidstrind+5)]
  hospital = hosp.search("span")[0].text

  # returns an array with the text before the hospital name in the td string, the hospital name, and the stuff after the hospital name
  hosptext = hosp.text.rpartition(hospital)
  hospital = hosptext[1]
  addressnstuff = hosptext[2].strip
  puts addressnstuff
  addylen = addressnstuff.length
  phonelen = addylen-14
  phone = addressnstuff[phonelen..addylen ]


  # We want the POC data for this hospital
  url = "http://www.hospitalcompare.hhs.gov/tables/hospital-pocQualityTable.aspx?hid=" + hid + "&stype=GENERAL&measureCD=HA&stateSearched=NY&tab=SOC"
  download = open(url)

  doc = Nokogiri::HTML(download)
  trs = doc.search('tr')
  # The hospital name will always be in the first tr row, and the text of the fourth th element
  #hospital = trs[0].search('th')[3].text
  # the percent given aspirin on arrival will always be in the 7th tr row, and the text of the fourth td element 
  percent = trs[6].search('td')[3].text
  # we want tr 6 - thats the data row with the Heart Attack Patients Given Aspirin at Arrival
  measure1 = trs[6].search('td')[0].text

  ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure1, 'Value' => percent})

  # Now to save the data for PCI within 90 min of arrival
  measure2 = trs[12].search('td')[0].text
  pci = trs[12].search('td')[3].text

    ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure2, 'Value' => pci})

  # Now to save the data for Heart Attack Patients Given a Prescription for a Statin at Discharge
  measure2 = trs[13].search('td')[0].text
  pci = trs[13].search('td')[3].text

  ScraperWiki.save(unique_keys=['Hospital', 'Quality Measure', 'Value'], data = {'Hospital' => hospital,'Quality Measure' => measure2, 'Value' => pci})

# done iterating thru list of hospitals
end

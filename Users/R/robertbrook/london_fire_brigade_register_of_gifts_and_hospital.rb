require 'nokogiri'

starting_url = 'http://www.london-fire.gov.uk/gifts_all.asp'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
doc.search('table.meetingReports tr').each do |tr|
    ps = tr.search('td p')
    name = ps[0]
    date = ps[1]
    details = ps[2]
    donor = ps[3]
    
    if name
      record = {'name' => name.text(), 'date' => date.text(), 'details' => details.text(), 'donor' => donor.text()}
      ScraperWiki.save(['name'], record)
    end
end

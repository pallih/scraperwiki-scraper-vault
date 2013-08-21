require 'nokogiri'
require 'time'
 
URL = "https://www.sutton.gov.uk/index.aspx?articleid=4332"

html = ScraperWiki::scrape(URL)
doc = Nokogiri::HTML(html)

meeting = ''
items_this_meeting = 0
 
doc.at("#bodytext").children.each do |node|
  if node.inner_text.match(/\d{1,2}\w{2}?\s+\w+\s+\d{4}/) # eg 10 December 2012 or 7th February 2013
    meeting = node.inner_text.strip
    items_this_meeting = 0
  end
 
  node.children.each do |subnode|
    if subnode.name == 'a' && subnode['href'].match(/\.mp3$/i)
      items_this_meeting += 1
      item = {
        :d => Time.parse(meeting) + ((items_this_meeting - 1) * 30 * 60),
        :href => subnode['href'].strip,
        :title => subnode.inner_text.strip
      }
      ScraperWiki::save_sqlite([:href], item)
    end
  end
end

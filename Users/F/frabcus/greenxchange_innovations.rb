# Scraper GreenXChange, from Nike and Creative Commons

require 'nokogiri'
require 'parsedate'

# download one page worth of innovations
def get_page(page) 
  url = "http://www.greenxchange.cc/search?page=" + page.to_s

  puts "Scraping " + url
  html = ScraperWiki.scrape(url)
  puts html

  doc = Nokogiri::HTML(html)
  c = 0
  for v in doc.search("table.result tr")
    c += 1
    raw_date = v.search('th')[0].children.detect { |n| /^[A-Z0-9 ]+$/.match(n.text.strip) }.text.strip
    data = {
      'id' => v['id'].sub('innovation_', '').to_i,
      'title' => v.search('p.title a')[0].inner_html,
      'url' => "http://www.greenxchange.cc" + v.search('p.title a')[0]['href'],
      'short_desc' => v.search('p.description')[0].inner_html.strip,
      'company' => v.search('th a')[0].inner_html,
      'when' => ParseDate.parsedate(raw_date),
      'when_raw' => raw_date,
    }
    tags = v.search('div.tag span').map { |t| { 'tag'=>t.text.strip, 'innovation_id'=>data['id'] } }
 
    ScraperWiki.save_sqlite(unique_keys=['id'], data=data, table_name='innovations')
    for t in tags
      ScraperWiki.save_sqlite(unique_keys=['innovation_id', 'tag'], data=t, table_name='tags')
    end
  end

  return c
end

# loop through every page of list of all innovations
page = 1
while get_page(page)
  page += 1
end


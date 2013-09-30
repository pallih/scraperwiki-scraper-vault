require 'nokogiri'

base_url = 'http://www.cityofboston.gov/purchasing/'
index = Nokogiri::HTML(ScraperWiki.scrape(base_url + 'bid.asp'))
index.xpath("//td/b/a").each_with_index do |a, index|
  rfp = Nokogiri::HTML(ScraperWiki.scrape(base_url + a['href']))
  record = {}
  record['url'] = base_url + a['href']
  record['title'] = rfp.xpath("//table/tr/td/div/center/b").text
  record['contact_name'] = rfp.xpath("//div['mainColAttentionBoxRed']/b[1]").text.strip.gsub(/,$/, '')
  record['contact_phone'] = rfp.xpath("//div['mainColAttentionBoxRed']/b[2]").text.gsub(/, $/, '')
  record['open_date'], record['close_date'] = rfp.xpath("//tr[1]/td[2]/div/p/b").text.gsub('Bids', '').strip.split(' - ')
  ScraperWiki.save(['url', 'title', 'contact_name', 'contact_phone', 'open_date', 'close_date'], record)
end

require 'nokogiri'

base_url = 'http://www.cityofboston.gov/purchasing/'
index = Nokogiri::HTML(ScraperWiki.scrape(base_url + 'bid.asp'))
index.xpath("//td/b/a").each_with_index do |a, index|
  rfp = Nokogiri::HTML(ScraperWiki.scrape(base_url + a['href']))
  record = {}
  record['url'] = base_url + a['href']
  record['title'] = rfp.xpath("//table/tr/td/div/center/b").text
  record['contact_name'] = rfp.xpath("//div['mainColAttentionBoxRed']/b[1]").text.strip.gsub(/,$/, '')
  record['contact_phone'] = rfp.xpath("//div['mainColAttentionBoxRed']/b[2]").text.gsub(/, $/, '')
  record['open_date'], record['close_date'] = rfp.xpath("//tr[1]/td[2]/div/p/b").text.gsub('Bids', '').strip.split(' - ')
  ScraperWiki.save(['url', 'title', 'contact_name', 'contact_phone', 'open_date', 'close_date'], record)
end


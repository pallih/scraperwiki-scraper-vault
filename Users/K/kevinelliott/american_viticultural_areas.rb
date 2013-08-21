require 'scraperwiki'
require 'nokogiri'

html = ScraperWiki.scrape('http://www.iwineinstitute.com/avabyname.asp')
doc = Nokogiri::HTML(html)
count = -1
for row in doc.search('table tr')[1].search('td table tr')
  count += 1
  next if count == 0

  cells = row.search('td')
  download_text_url = cells[1].search('a')[0]['href']
  download_pdf_url = cells[2].search('a')[0]['href']
  data = {
    'name' => cells[0].inner_text,
    'download_text_url' => download_text_url,
    'download_pdf_url' => download_pdf_url,
    'acreage' => cells[3].inner_text,
    'effective_date' => cells[4].inner_text
  }
  puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
end

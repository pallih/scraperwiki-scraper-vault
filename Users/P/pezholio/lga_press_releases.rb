require 'nokogiri'

html = ScraperWiki.scrape("http://www.local.gov.uk/media-releases")

doc = Nokogiri::HTML(html,nil,"UTF-8")

for v in doc.search("div.newsItem")
  title = v.search("h3")[0].text
  url = "http://www.local.gov.uk" + v.search("h3").search("a")[0]['href']
  summary = v.search("p.listSummary")[0].text
  date = Date.parse(v.search("p.date")[0].text).strftime('%Y-%m-%d')

  data = {
    'title' => title,
    'url' => url,
    'summary' => summary,
    'date' => date
  }
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data) 
end


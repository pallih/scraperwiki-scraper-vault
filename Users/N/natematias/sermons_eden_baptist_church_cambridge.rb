require 'nokogiri'

html = ScraperWiki.scrape("http://audio.eden-cambridge.org/")

doc = Nokogiri::HTML(html)

eden_sermons = []

for sermon in doc.css("tbody[@id='mp3table'] tr")
  cells = sermon.search('td')

  title_links = cells[1].search('a')
  title = title_links[0].inner_html
  puts title
  notes   = title_links[2].attribute("href") if title_links.size > 2
  mp3_href = title_links[0].attribute("href")
  passage = cells[3].content

  data = { 'title' => title,
           'date' => cells[0].inner_html,
           'series' => cells[2].inner_html,
           'preacher' => cells[4].inner_html,
           'duration' => cells[5].inner_html,
           'mp3' => mp3_href,
           'passage' => passage,
           'notes' => notes}
  ScraperWiki.save_sqlite(unique_keys=['title'],data=data)
end



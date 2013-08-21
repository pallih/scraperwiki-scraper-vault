require 'nokogiri'

browseUrl = "http://mitworld.mit.edu/browse"
browse = ScraperWiki.scrape(browseUrl)
doc = Nokogiri::HTML.parse(browse)

while doc.css('.next') != [] do
  doc.css('.video').each do |video|
    url = video.css('a')[0].attr('href')
    ScraperWiki.save(unique_keys=['text', 'url'], data={'text' => video.text, 'url' => url})
  end
    nextUrl = doc.css('.next').attr('href').text rescue next
    nextHtml = ScraperWiki.scrape("http://mitworld.mit.edu#{nextUrl}")
    doc = Nokogiri::HTML.parse(nextHtml)
end


  doc.css('.video').each do |video|
    url = video.css('a')[0].attr('href')
    ScraperWiki.save(unique_keys=['text', 'url'], data={'text' => video.text, 'url' => url})
  end
require 'nokogiri'

starting_url = 'http://www.publications.parliament.uk/pa/ld201011/ldelect/2/202.htm'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
doc.search('td p').each do |peer|
    if peer.inner_html.length < 100
      record = {'peer' => peer.inner_html}
      ScraperWiki.save(['peer'], record)
    end
end

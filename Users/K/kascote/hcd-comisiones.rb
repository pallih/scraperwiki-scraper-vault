require 'nokogiri'

starting_url = 'http://webappl.hcdn.gov.ar/comisiones/comisiones.jsp'
html = ScraperWiki.scrape(starting_url)
baseurl = 'http://webappl.hcdn.gov.ar/comisiones/'

doc = Nokogiri::HTML(html)
doc.css('table tr').each do |tr|
  td = tr.css('td')
  if (td.length == 2)
    a = td.last.css('a').first
    ScraperWiki.save(['order'], { 'order' => td.first.content,
                                  'link' => baseurl + a['href'],
                                  'name' => a.content })
  end
endrequire 'nokogiri'

starting_url = 'http://webappl.hcdn.gov.ar/comisiones/comisiones.jsp'
html = ScraperWiki.scrape(starting_url)
baseurl = 'http://webappl.hcdn.gov.ar/comisiones/'

doc = Nokogiri::HTML(html)
doc.css('table tr').each do |tr|
  td = tr.css('td')
  if (td.length == 2)
    a = td.last.css('a').first
    ScraperWiki.save(['order'], { 'order' => td.first.content,
                                  'link' => baseurl + a['href'],
                                  'name' => a.content })
  end
end
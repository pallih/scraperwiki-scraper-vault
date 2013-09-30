html = ScraperWiki.scrape("http://www.ssp.sp.gov.br/estatistica/dados.aspx?id=607")
push ("__doPostBack('ctl00$ContentPlaceHolder1$lnk100mil','')")
puts html


require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("table tr")
  cells = v.search('td')
  data = {
    'ano' => cells[0].inner_html,
    'homi' => cells[1].inner_html.to_i,
    'furto' => cells[2].inner_html.to_i,
    'roubo' => cells[3].inner_html.to_i,
    'veicu' => cells[4].inner_html.to_i
  }
  puts data.to_json
end


ScraperWiki.save_sqlite(unique_keys=['ano'], data=data)

html = ScraperWiki.scrape("http://www.ssp.sp.gov.br/estatistica/dados.aspx?id=607")
push ("__doPostBack('ctl00$ContentPlaceHolder1$lnk100mil','')")
puts html


require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("table tr")
  cells = v.search('td')
  data = {
    'ano' => cells[0].inner_html,
    'homi' => cells[1].inner_html.to_i,
    'furto' => cells[2].inner_html.to_i,
    'roubo' => cells[3].inner_html.to_i,
    'veicu' => cells[4].inner_html.to_i
  }
  puts data.to_json
end


ScraperWiki.save_sqlite(unique_keys=['ano'], data=data)


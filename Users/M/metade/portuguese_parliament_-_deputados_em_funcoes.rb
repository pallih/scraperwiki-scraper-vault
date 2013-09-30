require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://www.parlamento.pt/DeputadoGP/Paginas/DeputadosLista.aspx'

agent = Mechanize.new
page = agent.get(url)
page.search('#ctl00_MSO_ContentDiv table.ARTabResultados tr').map do |tr|
  link = tr.at_css('a')
  next if link.nil? 
  
  bid = $1 if link['href'] =~ /BID=(\d+)/
  if bid
    data = tr.css('td span').map { |s| s.text }
    
    hash = { 
      'name'  => link.text,
      'bid'   => bid,
      'area'  => data[0],
      'party' => data[1],
    }
    ScraperWiki.save_sqlite(unique_keys=['bid'], data=hash)
  end
end.compact
require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://www.parlamento.pt/DeputadoGP/Paginas/DeputadosLista.aspx'

agent = Mechanize.new
page = agent.get(url)
page.search('#ctl00_MSO_ContentDiv table.ARTabResultados tr').map do |tr|
  link = tr.at_css('a')
  next if link.nil? 
  
  bid = $1 if link['href'] =~ /BID=(\d+)/
  if bid
    data = tr.css('td span').map { |s| s.text }
    
    hash = { 
      'name'  => link.text,
      'bid'   => bid,
      'area'  => data[0],
      'party' => data[1],
    }
    ScraperWiki.save_sqlite(unique_keys=['bid'], data=hash)
  end
end.compact

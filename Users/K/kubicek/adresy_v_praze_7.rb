require 'nokogiri'           

uri = URI.parse('http://vdp.cuzk.cz/vdp/ruian/adresnimista/vyhledej')

query = {
        'ob.kod'=>554782,
        'mc.kod'=>500186,
        'sog.sort'=>'CASTOBCE',
        'search'=>'Vyhledat'
}
uri.query = query.collect{|name, value| "#{name}=#{value}"}.join('&')

puts "Fetching #{uri.to_s}"

html = ScraperWiki::scrape(uri.to_s)
doc = Nokogiri::HTML(html,nil,"UTF-8")

total_pages = doc.css('div.dataPager a')[-2][:href].scan(/adg.page=(\d*)/).flatten.first.to_i
last_page = ScraperWiki::get_var('last_page') || 1
last_page = 1 if last_page>=total_pages
    
(last_page..total_pages).to_a.collect{ |page|
  puts "Fetching page #{page}"
  html = ScraperWiki::scrape(uri.to_s+"&adg.page=#{page}")
  doc = Nokogiri::HTML(html,nil,"UTF-8")
  doc.css('table#item.dataTable tbody tr').each {|row|
    items = row.css('td').children
    ScraperWiki::save_sqlite(unique_keys=[:addr_id], data={
      :addr_id => items[0].inner_text,
      :addr_uri => items[5][:href],
      :numbers => items[1].inner_text,
      :district => items[2].inner_text,
      :district_uri => items[2][:href],
      :street => items[3].inner_text,
      :street_uri => items[3][:href]
    })           
  }
  ScraperWiki::save_var('last_page', page)
}
            require 'nokogiri'           

uri = URI.parse('http://vdp.cuzk.cz/vdp/ruian/adresnimista/vyhledej')

query = {
        'ob.kod'=>554782,
        'mc.kod'=>500186,
        'sog.sort'=>'CASTOBCE',
        'search'=>'Vyhledat'
}
uri.query = query.collect{|name, value| "#{name}=#{value}"}.join('&')

puts "Fetching #{uri.to_s}"

html = ScraperWiki::scrape(uri.to_s)
doc = Nokogiri::HTML(html,nil,"UTF-8")

total_pages = doc.css('div.dataPager a')[-2][:href].scan(/adg.page=(\d*)/).flatten.first.to_i
last_page = ScraperWiki::get_var('last_page') || 1
last_page = 1 if last_page>=total_pages
    
(last_page..total_pages).to_a.collect{ |page|
  puts "Fetching page #{page}"
  html = ScraperWiki::scrape(uri.to_s+"&adg.page=#{page}")
  doc = Nokogiri::HTML(html,nil,"UTF-8")
  doc.css('table#item.dataTable tbody tr').each {|row|
    items = row.css('td').children
    ScraperWiki::save_sqlite(unique_keys=[:addr_id], data={
      :addr_id => items[0].inner_text,
      :addr_uri => items[5][:href],
      :numbers => items[1].inner_text,
      :district => items[2].inner_text,
      :district_uri => items[2][:href],
      :street => items[3].inner_text,
      :street_uri => items[3][:href]
    })           
  }
  ScraperWiki::save_var('last_page', page)
}
            
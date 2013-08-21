require 'rubygems'
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser=Nokogiri::HTML

BASE_URL = "http://www.google.fr/"

brw = Mechanize.new { |b|
b.user_agent_alias ='Linux Firefox'
b.read_timeout = 1200
}

pg = brw.get(BASE_URL)
puts pg.inspect

params = {'q'=>'nodejs'}
pg = pg.form_with(:name => "f") do |f|
  #f['gs_hitf0'] = 'test' 
  params.each { |k,v| f[k] = v}
  #pg = f.submit
end.submit

def scrape(page,doc)
  puts doc.inspect
  #parse and find xpath of result
  lnco = doc.links.count
  puts "page: #{page} links count: #{lnco}"
  

  doc.links_with(:text => /Nodejs/ ).each do |ln|
    puts "Desc: #{ln.text} - Link: #{ln.href}"
  end
  
  puts "Nokogiri1:"
  puts doc.body.inspect
  resultlist = Nokogiri::HTML(doc.body).xpath('//h3[@class="r"]/a')
  #puts resultlist.inspect
  resultlist.each do |res|
    puts "Desc: #{res.text} - Link: #{res.xpath('@href')} "
  end

  puts "Nokogiri2:"
  resultlist = Nokogiri::HTML(doc.body).css('h3.r > a')
  #puts resultlist.inspect
  resultlist.each do |res|
    r2 = res.xpath('@href')
    puts "Desc: #{res.text} - Link: #{r2} "
  end
  
  puts "Nokogiri3:"
  resultlist = Nokogiri::HTML(doc.body).xpath('//div[@id="ires"]//h3/a')
  #puts resultlist.inspect
  result = 1
  resultlist.each do |res|
    r2 = res.xpath('@href')
    puts "Desc: #{res.text} - Link: #{r2} "
    
    ScraperWiki.save_sqlite(unique_keys=["page","result"], data={"page"=>page,"result"=>result,"text"=>res.text,"link"=>r2}, table_name="swdata", verbose=2)
    result+=1
  end
end

scrape(1,pg)


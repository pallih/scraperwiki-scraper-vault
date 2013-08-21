# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.drc.gov.lk"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.strip.to_i}
  end
end

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//textarea/text()").to_s.split("\n").strip
  doc.each{|d|
    r = {'doc'=>Time.now} 
    r['company_name'],r['company_number'] = d.scan(/(.*) \((.*)\)$/).flatten
    records << r unless r['company_name'].nil? or r['company_name'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['company_name'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  s_url = BASE_URL + "/App/comreg.nsf/7ef7b8683de4682765257a78003959eb?OpenForm"
  pg = br.get(s_url)
  clck = attributes(Nokogiri::HTML(pg.body).xpath(".//a[@onclick and img][1]"),"onclick").split("'")[1]
  params = {
  "__Click"=>clck,"%%Surrogate_seaSearchOption"=>"1","seaSearchOption"=>"Name,begins,with","seaSearchText"=>srch,
  "seaSearchNumber"=>"","seaSearchType"=>"Name","seaRegNo"=>"","seaSearchCondition"=>"AND","seaResult"=>"","SaveOptions"=>"0","VisibleCheck"=>""}
  pg.form_with(:name=>"_ComReg_Frm_PublicSearch") do |f|
    params.each{|k,v| f[k]=v}
    pg = f.submit
  end
  ttl = scrape(pg.body)
end

#save_metadata("OFFSET",0)
range = ('AA'..'ZZZ').to_a + ('00'..'100').to_a + ['!','@','#','$','%','^','&','*','(',')','-'].to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

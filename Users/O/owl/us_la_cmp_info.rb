# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://coraweb.sos.la.gov"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  end
end

def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,num,url)
  #tbls = Nokogiri::HTML(data).xpath(".//table[@width='100%'  and @cellspacing='0' and @cellpadding='3' and @border='0']")
  doc = Nokogiri::HTML(data)  
  r = {"DOC"=>Time.now,"SCRAPED_NUMBER"=>num.to_i}
  r["COMPANY_NAME"],r["TYPE"],r["CITY"],r["STATUS"]= text(doc.xpath(".//span[@id='lblName']")),text(doc.xpath(".//span[@id='lblType']")),text(doc.xpath(".//span[@id='lblCity']")),text(doc.xpath(".//span[@id='lblStatus']"))
  r["CHARTER_NUMBER"],r["REG_DT"],r["STATE"] = text(doc.xpath(".//span[@id='lblCharterNumber']")),text(doc.xpath(".//span[@id='lblRegistrationDate']")),text(doc.xpath(".//span[@id='lblStateOfOrigin']"))
  #puts r.inspect
  r['URL']=url
  ScraperWiki.save_sqlite(unique_keys=['CHARTER_NUMBER'],r,table_name='swdata',verbose=2) unless r['CHARTER_NUMBER'].nil?  or r['CHARTER_NUMBER'].empty? 
  return (r['CHARTER_NUMBER'].nil? or r['CHARTER_NUMBER'].empty? )?  nil : 0
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"/commercialsearch/CommercialSearchDetails_Print.aspx?CharterID=#{num}")
    resp = scrape(pg.body,num,pg.uri.to_s) unless pg.body =~ /NullReferenceException/i
    save_metadata("OFFSET",num.next) if resp == 0
  end
end

offset = get_metadata("OFFSET",968428)
(offset..offset+750).each{|num|
  resp = action(num)
}





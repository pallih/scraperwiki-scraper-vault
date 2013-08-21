# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.scsos.com/"

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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
      return tmp.join("\n")
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
  doc = Nokogiri::HTML(data)
  records = {"COMPANY_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now}
  records["COMPANY_NAME"] = text(doc.xpath(".//div[@id='content']/h2[following-sibling::div[@class='copy']/em]"))
  records["STATUS"] = text(doc.xpath(".//div[@id='content']/div[@class='copy' and em]/table/tr[td/b[text()='STATUS:']]/td[2]"))
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty? 
  return (records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty?) ? nil : 0 
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "index.asp?n=18&p=4&s=18&corporateid=#{num}"
    pg = br.get(s_url)
    resp =  scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) if resp == 0
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end



strt = get_metadata("OFFSET",636441)
endd = strt+200
(strt..endd).each{|num|
  action(num)
}

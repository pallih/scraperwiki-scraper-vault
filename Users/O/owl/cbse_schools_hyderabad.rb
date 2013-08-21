# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.crazyhyderabad.com"

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
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  data = Nokogiri::HTML(data).to_html
  doc = Nokogiri::HTML(data).xpath(".//table[@class='table_bordercolor']/tbody/tr/td")
  records = []
  doc.each{|ele| 
    r = {
      "SCHOOL"=>text(ele.xpath(".")).join("|"),
      "DOC"=>Time.now
    }
    records << r
  } if doc.length >1 
  ScraperWiki.save_sqlite(unique_keys=['SCHOOL'],records)
end

def action(num)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/cbse-schools.html?start=#{num}")
  min_body =  pg.body.scan(/div class="newsitem_text">(.*)<\/table>/m).flatten.first + "</table>"
  scrape(min_body)
end
(0..9).each{|num|
  action(num)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.crazyhyderabad.com"

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
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.delete_if{|a| a.nil? or a.empty? }
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  data = Nokogiri::HTML(data).to_html
  doc = Nokogiri::HTML(data).xpath(".//table[@class='table_bordercolor']/tbody/tr/td")
  records = []
  doc.each{|ele| 
    r = {
      "SCHOOL"=>text(ele.xpath(".")).join("|"),
      "DOC"=>Time.now
    }
    records << r
  } if doc.length >1 
  ScraperWiki.save_sqlite(unique_keys=['SCHOOL'],records)
end

def action(num)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    b.retry_change_requests = true
  }
  pg =  br.get(BASE_URL+"/cbse-schools.html?start=#{num}")
  min_body =  pg.body.scan(/div class="newsitem_text">(.*)<\/table>/m).flatten.first + "</table>"
  scrape(min_body)
end
(0..9).each{|num|
  action(num)
}
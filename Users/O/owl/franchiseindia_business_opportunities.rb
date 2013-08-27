# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.franchiseindia.com/"

class String
  def last
    return ""
  end
end

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
      str.children().collect{|st| tmp << st.text.strip}
      return tmp
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
  doc = Nokogiri::HTML(data).xpath(".//div[@class='midmain']")
  records = []
  doc.each{|ele|
    r = {
      "COMPANY_NAME"=>text(ele.xpath("span[@class='top4 dispB']/span/a")),
      "URL"=>attributes(ele.xpath("span[@class='top4 dispB']/span/a"),"href")
    }
    ele.xpath("div[@class='mid']/p").each{|para|
      r[text(para.xpath("strong")).gsub(/:| |/,"").upcase] = text(para).last#.text.to_s.strip
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      b.retry_change_requests = true

    }
    s_url = BASE_URL+"business-opportunities/All/"
    pg = br.get(s_url)
    scrape(pg.body)
    begin
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[@title='next page']"),"href")
      break if nex.nil?  or nex.empty? 
      pg = br.get(nex)
      scrape(pg.body)
    end while(true)
  rescue Exception => e
    puts [e].inspect
    retry
  end
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.franchiseindia.com/"

class String
  def last
    return ""
  end
end

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
      str.children().collect{|st| tmp << st.text.strip}
      return tmp
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
  doc = Nokogiri::HTML(data).xpath(".//div[@class='midmain']")
  records = []
  doc.each{|ele|
    r = {
      "COMPANY_NAME"=>text(ele.xpath("span[@class='top4 dispB']/span/a")),
      "URL"=>attributes(ele.xpath("span[@class='top4 dispB']/span/a"),"href")
    }
    ele.xpath("div[@class='mid']/p").each{|para|
      r[text(para.xpath("strong")).gsub(/:| |/,"").upcase] = text(para).last#.text.to_s.strip
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      b.retry_change_requests = true

    }
    s_url = BASE_URL+"business-opportunities/All/"
    pg = br.get(s_url)
    scrape(pg.body)
    begin
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[@title='next page']"),"href")
      break if nex.nil?  or nex.empty? 
      pg = br.get(nex)
      scrape(pg.body)
    end while(true)
  rescue Exception => e
    puts [e].inspect
    retry
  end
end
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.franchiseindia.com/"

class String
  def last
    return ""
  end
end

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
      str.children().collect{|st| tmp << st.text.strip}
      return tmp
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
  doc = Nokogiri::HTML(data).xpath(".//div[@class='midmain']")
  records = []
  doc.each{|ele|
    r = {
      "COMPANY_NAME"=>text(ele.xpath("span[@class='top4 dispB']/span/a")),
      "URL"=>attributes(ele.xpath("span[@class='top4 dispB']/span/a"),"href")
    }
    ele.xpath("div[@class='mid']/p").each{|para|
      r[text(para.xpath("strong")).gsub(/:| |/,"").upcase] = text(para).last#.text.to_s.strip
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      b.retry_change_requests = true

    }
    s_url = BASE_URL+"business-opportunities/All/"
    pg = br.get(s_url)
    scrape(pg.body)
    begin
      nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[@title='next page']"),"href")
      break if nex.nil?  or nex.empty? 
      pg = br.get(nex)
      scrape(pg.body)
    end while(true)
  rescue Exception => e
    puts [e].inspect
    retry
  end
end
action()
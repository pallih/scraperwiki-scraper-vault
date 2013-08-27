require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.tata.com"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//a[@class='bodylink']").each{|anchor|
      lst << attributes(anchor.xpath("."),"href")
    }
    return lst
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records ={
      "DOC" => Time.now.to_s,
      "URL" => url,
      "COMPANY_NAME" => text(doc.xpath(".//h3[@class='ArticleTitle']/text()")),
      "DESCRIPTION" => text(doc.xpath(".//td[@class='BodyTxt']/p[2]/text()")),
      "AREA_OF_BUSINESS" => text(doc.xpath(".//p[a[@name='ab' or @name='#ab']]/text()")),
      "LOCATION" => text(doc.xpath(".//p[a[@name='lc' or @name='#lc']]/text()"))
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='SWDATA',verbose=0)
  end
end


def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/company/index.aspx?sectid=21vxqwHGkoo="
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #lst = ["/company/profile.aspx?sectid=nNn/Z0o/2UI="]
    lst.each{|comp_url|
      pg_u = br.get(BASE_URL+comp_url)
      scrape(pg_u.body,"details",BASE_URL+comp_url)  
    }
  rescue Exception => e
      puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

action()
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.tata.com"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//a[@class='bodylink']").each{|anchor|
      lst << attributes(anchor.xpath("."),"href")
    }
    return lst
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records ={
      "DOC" => Time.now.to_s,
      "URL" => url,
      "COMPANY_NAME" => text(doc.xpath(".//h3[@class='ArticleTitle']/text()")),
      "DESCRIPTION" => text(doc.xpath(".//td[@class='BodyTxt']/p[2]/text()")),
      "AREA_OF_BUSINESS" => text(doc.xpath(".//p[a[@name='ab' or @name='#ab']]/text()")),
      "LOCATION" => text(doc.xpath(".//p[a[@name='lc' or @name='#lc']]/text()"))
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='SWDATA',verbose=0)
  end
end


def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/company/index.aspx?sectid=21vxqwHGkoo="
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #lst = ["/company/profile.aspx?sectid=nNn/Z0o/2UI="]
    lst.each{|comp_url|
      pg_u = br.get(BASE_URL+comp_url)
      scrape(pg_u.body,"details",BASE_URL+comp_url)  
    }
  rescue Exception => e
      puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

action()
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.tata.com"

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//a[@class='bodylink']").each{|anchor|
      lst << attributes(anchor.xpath("."),"href")
    }
    return lst
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records ={
      "DOC" => Time.now.to_s,
      "URL" => url,
      "COMPANY_NAME" => text(doc.xpath(".//h3[@class='ArticleTitle']/text()")),
      "DESCRIPTION" => text(doc.xpath(".//td[@class='BodyTxt']/p[2]/text()")),
      "AREA_OF_BUSINESS" => text(doc.xpath(".//p[a[@name='ab' or @name='#ab']]/text()")),
      "LOCATION" => text(doc.xpath(".//p[a[@name='lc' or @name='#lc']]/text()"))
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NAME'],records,table_name='SWDATA',verbose=0)
  end
end


def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/company/index.aspx?sectid=21vxqwHGkoo="
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #lst = ["/company/profile.aspx?sectid=nNn/Z0o/2UI="]
    lst.each{|comp_url|
      pg_u = br.get(BASE_URL+comp_url)
      scrape(pg_u.body,"details",BASE_URL+comp_url)  
    }
  rescue Exception => e
      puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

action()

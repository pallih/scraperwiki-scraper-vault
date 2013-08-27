# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.caipo.gov.bb"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
}


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

def scrape(pg,act,rec)
  data = pg.body
  if act == "list"
  elsif act == "details"
    r = {"link"=>pg.uri.to_s,"doc"=>Time.now}
    doc = Nokogiri::HTML(data).xpath(".")
      
    r["company_name"] = doc.xpath(".//td[@class='sectiontablerow name']/text()").text.to_s.strip
    r["company_number"] = doc.xpath(".//td[@class='sectiontablerow number']/text()").text.to_s.strip
    r["category"] = doc.xpath(".//td[@class='sectiontablerow category']/text()").text.to_s.strip
    r["incorporated_dt"] = doc.xpath(".//td[@class='sectiontablerow dateinc']/text()").text.to_s.strip
    #puts r.inspect
    return r.merge(rec) unless r["company_number"].nil? or r["company_number"].empty? 
  end
end

def action(s_no)
  begin
    record = nil
    begin
      r = scrape(@br.get(BASE_URL + "/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=#{s_no}&Itemid=61"),"details",{"scraped_number"=>s_no})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],r) if r['category'] == 'Company' unless record.nil? 
      s_no = s_no + 1
      save_metadata("start",s_no) unless r.nil? 
    end
  end
end

#save_metadata("start",35988)
#puts ScraperWiki.sqliteexecute("select max(scraped_number) from swdata")

#exit
start = get_metadata("start",35988)
(start..start+250).each{|st|
  action(st)
}
#puts scrape(@br.get("http://www.caipo.gov.bb/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=41170&Itemid=61"),"details",{})# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.caipo.gov.bb"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
}


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

def scrape(pg,act,rec)
  data = pg.body
  if act == "list"
  elsif act == "details"
    r = {"link"=>pg.uri.to_s,"doc"=>Time.now}
    doc = Nokogiri::HTML(data).xpath(".")
      
    r["company_name"] = doc.xpath(".//td[@class='sectiontablerow name']/text()").text.to_s.strip
    r["company_number"] = doc.xpath(".//td[@class='sectiontablerow number']/text()").text.to_s.strip
    r["category"] = doc.xpath(".//td[@class='sectiontablerow category']/text()").text.to_s.strip
    r["incorporated_dt"] = doc.xpath(".//td[@class='sectiontablerow dateinc']/text()").text.to_s.strip
    #puts r.inspect
    return r.merge(rec) unless r["company_number"].nil? or r["company_number"].empty? 
  end
end

def action(s_no)
  begin
    record = nil
    begin
      r = scrape(@br.get(BASE_URL + "/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=#{s_no}&Itemid=61"),"details",{"scraped_number"=>s_no})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],r) if r['category'] == 'Company' unless record.nil? 
      s_no = s_no + 1
      save_metadata("start",s_no) unless r.nil? 
    end
  end
end

#save_metadata("start",35988)
#puts ScraperWiki.sqliteexecute("select max(scraped_number) from swdata")

#exit
start = get_metadata("start",35988)
(start..start+250).each{|st|
  action(st)
}
#puts scrape(@br.get("http://www.caipo.gov.bb/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=41170&Itemid=61"),"details",{})# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.caipo.gov.bb"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
}


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

def scrape(pg,act,rec)
  data = pg.body
  if act == "list"
  elsif act == "details"
    r = {"link"=>pg.uri.to_s,"doc"=>Time.now}
    doc = Nokogiri::HTML(data).xpath(".")
      
    r["company_name"] = doc.xpath(".//td[@class='sectiontablerow name']/text()").text.to_s.strip
    r["company_number"] = doc.xpath(".//td[@class='sectiontablerow number']/text()").text.to_s.strip
    r["category"] = doc.xpath(".//td[@class='sectiontablerow category']/text()").text.to_s.strip
    r["incorporated_dt"] = doc.xpath(".//td[@class='sectiontablerow dateinc']/text()").text.to_s.strip
    #puts r.inspect
    return r.merge(rec) unless r["company_number"].nil? or r["company_number"].empty? 
  end
end

def action(s_no)
  begin
    record = nil
    begin
      r = scrape(@br.get(BASE_URL + "/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=#{s_no}&Itemid=61"),"details",{"scraped_number"=>s_no})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],r) if r['category'] == 'Company' unless record.nil? 
      s_no = s_no + 1
      save_metadata("start",s_no) unless r.nil? 
    end
  end
end

#save_metadata("start",35988)
#puts ScraperWiki.sqliteexecute("select max(scraped_number) from swdata")

#exit
start = get_metadata("start",35988)
(start..start+250).each{|st|
  action(st)
}
#puts scrape(@br.get("http://www.caipo.gov.bb/site/index.php?option=com_easytable&view=easytablerecord&id=3:new-test&rid=41170&Itemid=61"),"details",{})
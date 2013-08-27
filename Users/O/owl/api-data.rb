# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://api-data.com"

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
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@class='stuff']/tbody/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    r = {
      "PRODUCT_NAME"=>text(td[0].xpath("a")),
      "COUNTRY"=>text(td[1]),
      "MANUFACTURER"=>text(td[2]),
      "CHEMICAL_FORMULA"=>text(td[3]),
      "CAS"=>text(td[4]),
      "CEP"=>text(td[5]),
      "DMF"=>text(td[6]),
      "URL"=>attributes(td[0].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r['CAS'].nil? or r['CAS'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['CAS','PRODUCT_NAME','MANUFACTURER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
      b.max_history = 0
    }
    s_url = BASE_URL+"/base/index.php"
    params = {"q"=>srch,"search"=>"Search","search_type"=>"1"}
    pg = br.get(s_url,params)
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

action("%")# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://api-data.com"

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
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@class='stuff']/tbody/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    r = {
      "PRODUCT_NAME"=>text(td[0].xpath("a")),
      "COUNTRY"=>text(td[1]),
      "MANUFACTURER"=>text(td[2]),
      "CHEMICAL_FORMULA"=>text(td[3]),
      "CAS"=>text(td[4]),
      "CEP"=>text(td[5]),
      "DMF"=>text(td[6]),
      "URL"=>attributes(td[0].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r['CAS'].nil? or r['CAS'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['CAS','PRODUCT_NAME','MANUFACTURER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
      b.max_history = 0
    }
    s_url = BASE_URL+"/base/index.php"
    params = {"q"=>srch,"search"=>"Search","search_type"=>"1"}
    pg = br.get(s_url,params)
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

action("%")# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://api-data.com"

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
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@class='stuff']/tbody/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    r = {
      "PRODUCT_NAME"=>text(td[0].xpath("a")),
      "COUNTRY"=>text(td[1]),
      "MANUFACTURER"=>text(td[2]),
      "CHEMICAL_FORMULA"=>text(td[3]),
      "CAS"=>text(td[4]),
      "CEP"=>text(td[5]),
      "DMF"=>text(td[6]),
      "URL"=>attributes(td[0].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    records << r unless r['CAS'].nil? or r['CAS'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['CAS','PRODUCT_NAME','MANUFACTURER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 12000
      b.max_history = 0
    }
    s_url = BASE_URL+"/base/index.php"
    params = {"q"=>srch,"search"=>"Search","search_type"=>"1"}
    pg = br.get(s_url,params)
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

action("%")
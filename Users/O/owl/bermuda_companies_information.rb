# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.roc.gov.bm"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    Nokogiri::HTML(data).xpath(".//table[@border=1]/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("font/a/text()")),
        "COMPANY_NAME" => text(td[1].xpath("font/a/text()")),
        "CREATION_DT" => text(td[2].xpath("font/a/text()")),
        "URL" => BASE_URL + attributes(td[0].xpath("font/a"),"href").gsub("..","/roc/rocweb.nsf"),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/roc/rocweb.nsf/public+register/#{srch}+public+companies"
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/
  end
end
range = ['-misc-']+('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch)
  save_metadata("OFFSET",index.next)
}


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.roc.gov.bm"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    Nokogiri::HTML(data).xpath(".//table[@border=1]/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("font/a/text()")),
        "COMPANY_NAME" => text(td[1].xpath("font/a/text()")),
        "CREATION_DT" => text(td[2].xpath("font/a/text()")),
        "URL" => BASE_URL + attributes(td[0].xpath("font/a"),"href").gsub("..","/roc/rocweb.nsf"),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/roc/rocweb.nsf/public+register/#{srch}+public+companies"
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/
  end
end
range = ['-misc-']+('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch)
  save_metadata("OFFSET",index.next)
}


# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.roc.gov.bm"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    Nokogiri::HTML(data).xpath(".//table[@border=1]/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records = {
        "COMPANY_NUMBER" => text(td[0].xpath("font/a/text()")),
        "COMPANY_NAME" => text(td[1].xpath("font/a/text()")),
        "CREATION_DT" => text(td[2].xpath("font/a/text()")),
        "URL" => BASE_URL + attributes(td[0].xpath("font/a"),"href").gsub("..","/roc/rocweb.nsf"),
        "DOC" => Time.now.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records["COMPANY_NUMBER"].nil? 
    }
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/roc/rocweb.nsf/public+register/#{srch}+public+companies"
    pg = br.get(s_url)
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/
  end
end
range = ['-misc-']+('A'..'Z').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length
range.each_with_index{|srch,index|
  next if index<offset
  action(srch)
  save_metadata("OFFSET",index.next)
}



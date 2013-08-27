# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.kvk.aw/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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


def scrape(data,num,url)
  records= {"SCRAPED_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now}
  Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr[td[2]]").each{|tr|
    td = tr.xpath("td")
    k = text(td[0])
    key = nil
    case k
      #when /Business address/
      #  key = "ADDR"
      #when /Legal form/
      #  key = "TYPE"
      when /Name of the company/
        key = "COMPANY_NAME"
      #when /Statutory seat/
      #  key = "STATUTORY"
      #when /Date of incorporation/
      #  key = "CREATION_DT"
      #when /Date of commencement/
      #  key = "COMMENCE_DT"
      else
        key = nil
    end
    records[key] = text(td[1]) unless key.nil? 
  }
  
  #records["TRADE_NAME"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td/h2/strong/text()")) #unless defined?(records).nil? 
  #records["CANCELLED_DT"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(b/text(),'THIS COMPANY HAS')]/b/text()")).gsub(/THIS COMPANY HAS BEEN CANCELLED ON |THIS COMPANY HAS BEEN STRICKEN FROM OUR FILES /,"")
  tmp = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(p/text(),'Appearing in the')]/p/text()"))
  #records['LOCATION'],records['RECORD_DT'],records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last
  records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last.last
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty? 
  return (records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty?) ? nil : 0 
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "templates/kvk/view_extract.php?k=#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|TIME|HTTP/
      sleep(30)
      retry
    end
  end #unless is_available(num) > 0
end

strt = get_metadata("OFFSET",43500)
endd = strt+100
(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.kvk.aw/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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


def scrape(data,num,url)
  records= {"SCRAPED_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now}
  Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr[td[2]]").each{|tr|
    td = tr.xpath("td")
    k = text(td[0])
    key = nil
    case k
      #when /Business address/
      #  key = "ADDR"
      #when /Legal form/
      #  key = "TYPE"
      when /Name of the company/
        key = "COMPANY_NAME"
      #when /Statutory seat/
      #  key = "STATUTORY"
      #when /Date of incorporation/
      #  key = "CREATION_DT"
      #when /Date of commencement/
      #  key = "COMMENCE_DT"
      else
        key = nil
    end
    records[key] = text(td[1]) unless key.nil? 
  }
  
  #records["TRADE_NAME"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td/h2/strong/text()")) #unless defined?(records).nil? 
  #records["CANCELLED_DT"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(b/text(),'THIS COMPANY HAS')]/b/text()")).gsub(/THIS COMPANY HAS BEEN CANCELLED ON |THIS COMPANY HAS BEEN STRICKEN FROM OUR FILES /,"")
  tmp = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(p/text(),'Appearing in the')]/p/text()"))
  #records['LOCATION'],records['RECORD_DT'],records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last
  records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last.last
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty? 
  return (records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty?) ? nil : 0 
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "templates/kvk/view_extract.php?k=#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|TIME|HTTP/
      sleep(30)
      retry
    end
  end #unless is_available(num) > 0
end

strt = get_metadata("OFFSET",43500)
endd = strt+100
(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.kvk.aw/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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


def scrape(data,num,url)
  records= {"SCRAPED_NUMBER"=>num,"URL"=>url,"DOC"=>Time.now}
  Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr[td[2]]").each{|tr|
    td = tr.xpath("td")
    k = text(td[0])
    key = nil
    case k
      #when /Business address/
      #  key = "ADDR"
      #when /Legal form/
      #  key = "TYPE"
      when /Name of the company/
        key = "COMPANY_NAME"
      #when /Statutory seat/
      #  key = "STATUTORY"
      #when /Date of incorporation/
      #  key = "CREATION_DT"
      #when /Date of commencement/
      #  key = "COMMENCE_DT"
      else
        key = nil
    end
    records[key] = text(td[1]) unless key.nil? 
  }
  
  #records["TRADE_NAME"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td/h2/strong/text()")) #unless defined?(records).nil? 
  #records["CANCELLED_DT"] = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(b/text(),'THIS COMPANY HAS')]/b/text()")).gsub(/THIS COMPANY HAS BEEN CANCELLED ON |THIS COMPANY HAS BEEN STRICKEN FROM OUR FILES /,"")
  tmp = text(Nokogiri::HTML(data).xpath(".//table[@width='650']/tbody/tr/td[contains(p/text(),'Appearing in the')]/p/text()"))
  #records['LOCATION'],records['RECORD_DT'],records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last
  records['COMPANY_NUMBER']  = tmp.scan(/Industry in ([^>]*) since ([^>]*) under serial number ([^>]*) is/).last.last
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty? 
  return (records['COMPANY_NAME'].nil? or records['COMPANY_NAME'].empty?) ? nil : 0 
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "templates/kvk/view_extract.php?k=#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|TIME|HTTP/
      sleep(30)
      retry
    end
  end #unless is_available(num) > 0
end

strt = get_metadata("OFFSET",43500)
endd = strt+100
(strt..endd).each{|num|
  action(num)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'

#ScraperWiki.sqliteexecute("CREATE INDEX date_scraped ON CMPINFO (date_scraped)")
#ScraperWiki.commit
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www2.sos.state.oh.us/pls/bsqry/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "-" : str.text.gsub(/\n|\t||^\s+|\s+$/,"").gsub("\u00A0",'').strip
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def form_key(str)
  begin
      return (str.nil? or str.empty?) ? "" : str.text.gsub(/\n|\t|^\s+|:|\s+$/,"_").upcase
  rescue Exception => e
      return str.upcase unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,num,url,cd)
    records = {"date_scraped" => Time.now,"SCRAPED_NUMBER" => num,"URL"=>url,"CODE"=>cd}
    Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellspacing='0' and @cellpadding='2' and @border='1']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
        k = text(td[0])
        k_v = {}
        case k
          when /Entity Number/
            key = "COMPANY_NUMBER"
          when /Business Name/
            key = "COMPANY_NAME"
          when /Filing Type/
            key = "TYPE"
          when /Status/
            key = "STATUS"
          when /Original Filing Date/
            key = "CREATION_DT"
          when /Expiry Date/
            key = "DISSOLVE_DT"
          when /^Location/
            key = "location"
          else
            key = form_key(k)
        end
        if key == "location"
          tmp = text(td[1]).scan(/Location:(.*)County:(.*)State:(.*)/).flatten
        else
          records[key] = text(td[1])
        end
        
        #puts [key,text(td[1])].inspect
    }
    Nokogiri::HTML(data).xpath("//table[@width='100%' and @cellpadding='0' and @border='0' and not(@class) and not(@summary) and preceding::td[@class='t12ApplicationLogo']]/tr/td").each{|td|
        k = text(td).split(" ")
        case k[0]
            when /Location/
                key = "LOCATION"
            when /County/
                key = "COUNTRY"
            when /State/
                key = "STATE"
            else
                key = form_key(k[0])
        end
        records[key] = k[1]
    }
    table_name = company_type?(records["TYPE"]) ?  "CMPINFO" : "noncompanies"
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name,verbose=2) unless records['COMPANY_NUMBER'].nil? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def company_type?(type)
  type&&type.match(/company|corporation|limited|foreign|business/i)
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//td[@class='t12bottom' and @colspan='99']/a[span[text()='Download Business Search Results']]"),"href")
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "f?p=100:7:520694587981495::NO:7:P7_CHARTER_NUM:#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url,"")
    save_metadata("STRT",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
      retry if e.inspect =~ /Timeout/ or e.inspect =~ /TIME/
  end
end

#save_metadata("STRT",2035929)
#save_metadata("STRT",690511)
strt = get_metadata("STRT",2035916)
endd = strt+2000

(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'

#ScraperWiki.sqliteexecute("CREATE INDEX date_scraped ON CMPINFO (date_scraped)")
#ScraperWiki.commit
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www2.sos.state.oh.us/pls/bsqry/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "-" : str.text.gsub(/\n|\t||^\s+|\s+$/,"").gsub("\u00A0",'').strip
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def form_key(str)
  begin
      return (str.nil? or str.empty?) ? "" : str.text.gsub(/\n|\t|^\s+|:|\s+$/,"_").upcase
  rescue Exception => e
      return str.upcase unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,num,url,cd)
    records = {"date_scraped" => Time.now,"SCRAPED_NUMBER" => num,"URL"=>url,"CODE"=>cd}
    Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellspacing='0' and @cellpadding='2' and @border='1']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
        k = text(td[0])
        k_v = {}
        case k
          when /Entity Number/
            key = "COMPANY_NUMBER"
          when /Business Name/
            key = "COMPANY_NAME"
          when /Filing Type/
            key = "TYPE"
          when /Status/
            key = "STATUS"
          when /Original Filing Date/
            key = "CREATION_DT"
          when /Expiry Date/
            key = "DISSOLVE_DT"
          when /^Location/
            key = "location"
          else
            key = form_key(k)
        end
        if key == "location"
          tmp = text(td[1]).scan(/Location:(.*)County:(.*)State:(.*)/).flatten
        else
          records[key] = text(td[1])
        end
        
        #puts [key,text(td[1])].inspect
    }
    Nokogiri::HTML(data).xpath("//table[@width='100%' and @cellpadding='0' and @border='0' and not(@class) and not(@summary) and preceding::td[@class='t12ApplicationLogo']]/tr/td").each{|td|
        k = text(td).split(" ")
        case k[0]
            when /Location/
                key = "LOCATION"
            when /County/
                key = "COUNTRY"
            when /State/
                key = "STATE"
            else
                key = form_key(k[0])
        end
        records[key] = k[1]
    }
    table_name = company_type?(records["TYPE"]) ?  "CMPINFO" : "noncompanies"
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name,verbose=2) unless records['COMPANY_NUMBER'].nil? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def company_type?(type)
  type&&type.match(/company|corporation|limited|foreign|business/i)
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//td[@class='t12bottom' and @colspan='99']/a[span[text()='Download Business Search Results']]"),"href")
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "f?p=100:7:520694587981495::NO:7:P7_CHARTER_NUM:#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url,"")
    save_metadata("STRT",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
      retry if e.inspect =~ /Timeout/ or e.inspect =~ /TIME/
  end
end

#save_metadata("STRT",2035929)
#save_metadata("STRT",690511)
strt = get_metadata("STRT",2035916)
endd = strt+2000

(strt..endd).each{|num|
  action(num)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'

#ScraperWiki.sqliteexecute("CREATE INDEX date_scraped ON CMPINFO (date_scraped)")
#ScraperWiki.commit
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www2.sos.state.oh.us/pls/bsqry/"

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

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "-" : str.text.gsub(/\n|\t||^\s+|\s+$/,"").gsub("\u00A0",'').strip
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def form_key(str)
  begin
      return (str.nil? or str.empty?) ? "" : str.text.gsub(/\n|\t|^\s+|:|\s+$/,"_").upcase
  rescue Exception => e
      return str.upcase unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,num,url,cd)
    records = {"date_scraped" => Time.now,"SCRAPED_NUMBER" => num,"URL"=>url,"CODE"=>cd}
    Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellspacing='0' and @cellpadding='2' and @border='1']/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
        k = text(td[0])
        k_v = {}
        case k
          when /Entity Number/
            key = "COMPANY_NUMBER"
          when /Business Name/
            key = "COMPANY_NAME"
          when /Filing Type/
            key = "TYPE"
          when /Status/
            key = "STATUS"
          when /Original Filing Date/
            key = "CREATION_DT"
          when /Expiry Date/
            key = "DISSOLVE_DT"
          when /^Location/
            key = "location"
          else
            key = form_key(k)
        end
        if key == "location"
          tmp = text(td[1]).scan(/Location:(.*)County:(.*)State:(.*)/).flatten
        else
          records[key] = text(td[1])
        end
        
        #puts [key,text(td[1])].inspect
    }
    Nokogiri::HTML(data).xpath("//table[@width='100%' and @cellpadding='0' and @border='0' and not(@class) and not(@summary) and preceding::td[@class='t12ApplicationLogo']]/tr/td").each{|td|
        k = text(td).split(" ")
        case k[0]
            when /Location/
                key = "LOCATION"
            when /County/
                key = "COUNTRY"
            when /State/
                key = "STATE"
            else
                key = form_key(k[0])
        end
        records[key] = k[1]
    }
    table_name = company_type?(records["TYPE"]) ?  "CMPINFO" : "noncompanies"
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name,verbose=2) unless records['COMPANY_NUMBER'].nil? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def company_type?(type)
  type&&type.match(/company|corporation|limited|foreign|business/i)
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//td[@class='t12bottom' and @colspan='99']/a[span[text()='Download Business Search Results']]"),"href")
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "f?p=100:7:520694587981495::NO:7:P7_CHARTER_NUM:#{num}"
    pg = br.get(s_url)
    re = scrape(pg.body,num,s_url,"")
    save_metadata("STRT",num.next) unless re.nil? 
  rescue Exception => e
      puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
      retry if e.inspect =~ /Timeout/ or e.inspect =~ /TIME/
  end
end

#save_metadata("STRT",2035929)
#save_metadata("STRT",690511)
strt = get_metadata("STRT",2035916)
endd = strt+2000

(strt..endd).each{|num|
  action(num)
}

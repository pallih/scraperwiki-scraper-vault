require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://chroniclingamerica.loc.gov"
def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      if ret.nil? or ret.empty? 
        return default
      else
        return ret
      end
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
      #return str.text
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath("//ul[@class='results_list']/li").each{|lst|
      #puts records.inspect
      records << attributes(lst.xpath("a"),"href")
    }  
      #ScraperWiki.save_sqlite(unique_keys=["REGNO","CHALLANNO"],records,table_name="CHALLAN")
      #ScraperWiki.save_sqlite(unique_keys=["REGNO"],{"REGNO"=>records['REGNO'],"FULL_NAME"=>records['FULL_NAME']},table_name="VEHICLES")
    return records
  elsif action == "details"
    records = {}
    Nokogiri::HTML(data).xpath("//dl[@class='alt']/dt").each{|dt|
      attr = text(dt)
      key = nil
      case attr
        when /Title:/
          key = "TITLE"
        when /Alternative Titles:/
          key = "ALT_TITLE"
        when /Place of publication:/
          key = "PLACE_PUB"
        when /Geographic coverage:/
          key = "COVERAGE"
        when /Publisher:/
          key = "PUBLISHER"
        when /Dates of publication:/
          key = "PUB_DT"
        when /Description:/
          key = "DESC"
        when /Frequency:/
          key = "FREQUENCY"
        when /Language:/
          key = "LANGUAGE"
        when /Subjects:/
          key = "SUBJECTS"
        when /Notes:/
          key = "NOTES"
        when /LCCN:/
          key = "LCCN"
        when /OCLC:/
          key = "OCLC"
        when /Preceding Titles:/
          key = "PRECEDING_TITLES"
        when /Holdings:/
          key = "HOLDINGS"
        else 
          key = nil
      end
      val = ""
      dd = dt.xpath("following-sibling::dd[1]")
      if dd.at("ul")
        dd.xpath("ul/li").each{|v|
          val << text(v) <<"|"
        }
      else
        val = text(dd)
      end
      val = val.chop unless val[val.length] == "|"
      records[key]=val unless key.nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["LCCN","OCLC"],records,table_name="DIRECTORY",verbose=0)
  end
end

def scraped(params)
  return get_metadata(params,nil)
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[@class='next']"),"href")
end

def action
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    s_url = get_metadata("SRCH_URL","/search/titles/results/?state=&county=&city=&year1=1690&year2=2011&terms=&frequency=&language=&ethnicity=&labor=&material_type=&lccn=&rows=200&sort=date")
    ref = get_metadata("REF_URL",BASE_URL)
    puts 
    begin 
      pg = br.get(BASE_URL + s_url,[],BASE_URL+ref)
      lst = scrape(pg.body,"list")
      begin
        lst.each{|l_url|
          p_url = BASE_URL + l_url
          p_pg = br.get(p_url,nil,s_url)
          scrape(p_pg.body,"details")
        }
      rescue Exception => e
        puts "ERROR: While getting details :: #{e.inspect} :: #{e.backtrace}"
      end unless lst.empty? 
      ref = s_url
      s_url = "/search/titles/results/" + ne(pg.body)
      
      break if s_url == "/search/titles/results/"
      save_metadata("SRCH_URL",s_url)
      save_metadata("REF_URL",ref)
    rescue Exception => e
      puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  end
end

actionrequire 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://chroniclingamerica.loc.gov"
def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      if ret.nil? or ret.empty? 
        return default
      else
        return ret
      end
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
      #return str.text
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath("//ul[@class='results_list']/li").each{|lst|
      #puts records.inspect
      records << attributes(lst.xpath("a"),"href")
    }  
      #ScraperWiki.save_sqlite(unique_keys=["REGNO","CHALLANNO"],records,table_name="CHALLAN")
      #ScraperWiki.save_sqlite(unique_keys=["REGNO"],{"REGNO"=>records['REGNO'],"FULL_NAME"=>records['FULL_NAME']},table_name="VEHICLES")
    return records
  elsif action == "details"
    records = {}
    Nokogiri::HTML(data).xpath("//dl[@class='alt']/dt").each{|dt|
      attr = text(dt)
      key = nil
      case attr
        when /Title:/
          key = "TITLE"
        when /Alternative Titles:/
          key = "ALT_TITLE"
        when /Place of publication:/
          key = "PLACE_PUB"
        when /Geographic coverage:/
          key = "COVERAGE"
        when /Publisher:/
          key = "PUBLISHER"
        when /Dates of publication:/
          key = "PUB_DT"
        when /Description:/
          key = "DESC"
        when /Frequency:/
          key = "FREQUENCY"
        when /Language:/
          key = "LANGUAGE"
        when /Subjects:/
          key = "SUBJECTS"
        when /Notes:/
          key = "NOTES"
        when /LCCN:/
          key = "LCCN"
        when /OCLC:/
          key = "OCLC"
        when /Preceding Titles:/
          key = "PRECEDING_TITLES"
        when /Holdings:/
          key = "HOLDINGS"
        else 
          key = nil
      end
      val = ""
      dd = dt.xpath("following-sibling::dd[1]")
      if dd.at("ul")
        dd.xpath("ul/li").each{|v|
          val << text(v) <<"|"
        }
      else
        val = text(dd)
      end
      val = val.chop unless val[val.length] == "|"
      records[key]=val unless key.nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["LCCN","OCLC"],records,table_name="DIRECTORY",verbose=0)
  end
end

def scraped(params)
  return get_metadata(params,nil)
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[@class='next']"),"href")
end

def action
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    s_url = get_metadata("SRCH_URL","/search/titles/results/?state=&county=&city=&year1=1690&year2=2011&terms=&frequency=&language=&ethnicity=&labor=&material_type=&lccn=&rows=200&sort=date")
    ref = get_metadata("REF_URL",BASE_URL)
    puts 
    begin 
      pg = br.get(BASE_URL + s_url,[],BASE_URL+ref)
      lst = scrape(pg.body,"list")
      begin
        lst.each{|l_url|
          p_url = BASE_URL + l_url
          p_pg = br.get(p_url,nil,s_url)
          scrape(p_pg.body,"details")
        }
      rescue Exception => e
        puts "ERROR: While getting details :: #{e.inspect} :: #{e.backtrace}"
      end unless lst.empty? 
      ref = s_url
      s_url = "/search/titles/results/" + ne(pg.body)
      
      break if s_url == "/search/titles/results/"
      save_metadata("SRCH_URL",s_url)
      save_metadata("REF_URL",ref)
    rescue Exception => e
      puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
    end while(true)
  end
end

action
# encoding: UTF-16
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.icris.cr.gov.hk/csci/"

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
      return (str.nil? or str.text.nil?) ? "" : Iconv.conv("UTF-8","UTF-8",str.text.gsub(/\n|\t|^\s+|:|\s+$/,""))
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    records = {}
    begin
      Nokogiri::HTML(data).xpath("//form/table[1]/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /CR No/
            key = "COMPANY_NUMBER"
          when /Company Name/
            key = "COMPANY_NAME"
          when /Company Type/
            key = "TYPE"
          when /Date of Incorporation/
            key = "CREATION_DT"
          when /Company Status/
            key = "COMPANY_STATUS"
          when /Active Status/
            key = "STATUS"
          when /Remarks/
            key = "REMARKS"
          when /Winding Up Mode/
            key = "MODE"
          when /Date of Dissolution/
            key = "DISSOLVE_DT"
          when /Register of Charges/
            key = "REGISTER"
          when /Important Note/
            key = "NOTE"
          else
            key = nil
        end
        value = text(td[1])
        records[key] = value unless key.nil? 
      }
      records["SCRAPED_NUMBER"] = num
      records["URL"] = url
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="CMPINFO")
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
    end
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action
  num = get_metadata("INDEX",1)
  begin

    s_url = BASE_URL+"cns_basic_comp.do?sCRNo=#{num}&DPDSInd=&unpaid=true"
    @pg = @br.get(s_url)
    #if @pg.body =~ /NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
    #  break
    #end
    scrape(@pg.body,"details",num,s_url)
    num = num.next
    save_metadata("INDEX",num)
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    sleep(10)
  end while(true) #num = 1640791
    
end
begin
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
}
@pg = @br.get(BASE_URL + "login_i.do?loginType=iguest&username=iguest")
rescue Exception=> e
  raise("Exception: Unable the initialize the program")
end
action
# encoding: UTF-16
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.icris.cr.gov.hk/csci/"

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
      return (str.nil? or str.text.nil?) ? "" : Iconv.conv("UTF-8","UTF-8",str.text.gsub(/\n|\t|^\s+|:|\s+$/,""))
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    records = {}
    begin
      Nokogiri::HTML(data).xpath("//form/table[1]/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /CR No/
            key = "COMPANY_NUMBER"
          when /Company Name/
            key = "COMPANY_NAME"
          when /Company Type/
            key = "TYPE"
          when /Date of Incorporation/
            key = "CREATION_DT"
          when /Company Status/
            key = "COMPANY_STATUS"
          when /Active Status/
            key = "STATUS"
          when /Remarks/
            key = "REMARKS"
          when /Winding Up Mode/
            key = "MODE"
          when /Date of Dissolution/
            key = "DISSOLVE_DT"
          when /Register of Charges/
            key = "REGISTER"
          when /Important Note/
            key = "NOTE"
          else
            key = nil
        end
        value = text(td[1])
        records[key] = value unless key.nil? 
      }
      records["SCRAPED_NUMBER"] = num
      records["URL"] = url
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="CMPINFO")
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
    end
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action
  num = get_metadata("INDEX",1)
  begin

    s_url = BASE_URL+"cns_basic_comp.do?sCRNo=#{num}&DPDSInd=&unpaid=true"
    @pg = @br.get(s_url)
    #if @pg.body =~ /NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
    #  break
    #end
    scrape(@pg.body,"details",num,s_url)
    num = num.next
    save_metadata("INDEX",num)
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    sleep(10)
  end while(true) #num = 1640791
    
end
begin
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
}
@pg = @br.get(BASE_URL + "login_i.do?loginType=iguest&username=iguest")
rescue Exception=> e
  raise("Exception: Unable the initialize the program")
end
action
# encoding: UTF-16
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.icris.cr.gov.hk/csci/"

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
      return (str.nil? or str.text.nil?) ? "" : Iconv.conv("UTF-8","UTF-8",str.text.gsub(/\n|\t|^\s+|:|\s+$/,""))
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    records = {}
    begin
      Nokogiri::HTML(data).xpath("//form/table[1]/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /CR No/
            key = "COMPANY_NUMBER"
          when /Company Name/
            key = "COMPANY_NAME"
          when /Company Type/
            key = "TYPE"
          when /Date of Incorporation/
            key = "CREATION_DT"
          when /Company Status/
            key = "COMPANY_STATUS"
          when /Active Status/
            key = "STATUS"
          when /Remarks/
            key = "REMARKS"
          when /Winding Up Mode/
            key = "MODE"
          when /Date of Dissolution/
            key = "DISSOLVE_DT"
          when /Register of Charges/
            key = "REGISTER"
          when /Important Note/
            key = "NOTE"
          else
            key = nil
        end
        value = text(td[1])
        records[key] = value unless key.nil? 
      }
      records["SCRAPED_NUMBER"] = num
      records["URL"] = url
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="CMPINFO")
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
    end
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action
  num = get_metadata("INDEX",1)
  begin

    s_url = BASE_URL+"cns_basic_comp.do?sCRNo=#{num}&DPDSInd=&unpaid=true"
    @pg = @br.get(s_url)
    #if @pg.body =~ /NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
    #  break
    #end
    scrape(@pg.body,"details",num,s_url)
    num = num.next
    save_metadata("INDEX",num)
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    sleep(10)
  end while(true) #num = 1640791
    
end
begin
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
}
@pg = @br.get(BASE_URL + "login_i.do?loginType=iguest&username=iguest")
rescue Exception=> e
  raise("Exception: Unable the initialize the program")
end
action
# encoding: UTF-16
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.icris.cr.gov.hk/csci/"

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
      return (str.nil? or str.text.nil?) ? "" : Iconv.conv("UTF-8","UTF-8",str.text.gsub(/\n|\t|^\s+|:|\s+$/,""))
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
    records = {}
    begin
      Nokogiri::HTML(data).xpath("//form/table[1]/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /CR No/
            key = "COMPANY_NUMBER"
          when /Company Name/
            key = "COMPANY_NAME"
          when /Company Type/
            key = "TYPE"
          when /Date of Incorporation/
            key = "CREATION_DT"
          when /Company Status/
            key = "COMPANY_STATUS"
          when /Active Status/
            key = "STATUS"
          when /Remarks/
            key = "REMARKS"
          when /Winding Up Mode/
            key = "MODE"
          when /Date of Dissolution/
            key = "DISSOLVE_DT"
          when /Register of Charges/
            key = "REGISTER"
          when /Important Note/
            key = "NOTE"
          else
            key = nil
        end
        value = text(td[1])
        records[key] = value unless key.nil? 
      }
      records["SCRAPED_NUMBER"] = num
      records["URL"] = url
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="CMPINFO")
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
    end
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action
  num = get_metadata("INDEX",1)
  begin

    s_url = BASE_URL+"cns_basic_comp.do?sCRNo=#{num}&DPDSInd=&unpaid=true"
    @pg = @br.get(s_url)
    #if @pg.body =~ /NO MATCHING RECORD FOUND FOR THE SEARCH INFORMATION INPUT/
    #  break
    #end
    scrape(@pg.body,"details",num,s_url)
    num = num.next
    save_metadata("INDEX",num)
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    sleep(10)
  end while(true) #num = 1640791
    
end
begin
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
}
@pg = @br.get(BASE_URL + "login_i.do?loginType=iguest&username=iguest")
rescue Exception=> e
  raise("Exception: Unable the initialize the program")
end
action

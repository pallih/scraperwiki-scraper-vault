# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(" ").strip
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//div[@class='content-box-marginonly']/li").each{|li|
      anchor = li.xpath("a")
      lst << attributes(anchor.xpath("."),"href").gsub(/javascript:__doPostBack\('|'\)|','/,"")
    }
    return lst
  elsif act == "details"
    records={"DOC"=>Time.now.to_s,"URL"=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@style='padding: 10px; border: 1px solid #000000;' and table[@id='Table1']]")
    records['NAME']=text(doc.xpath("h3/span"))#.join(" ")
    doc.xpath("table[@id='Table1']/tr[not(normalize-space(td[@class='style1'])='')]").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("b/text()|text()|span/text()"))
      key = nil
      value = text(td[1].xpath("span"))
      case tmp_key
        when "Office Type:"
          key = "TYPE"
        when "Address:"
          key = "ADDRESS"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Postal Address:"
          key = "POSTAL_ADDRESS"
          value = text(td[1].xpath("div/table/tr/td/span"))
        when "DX:"
          key = "DX"
        when "Website:"
          key = "WEBSITE"
          value = text(td[1].xpath("a"))
        when "Email:"
          key = "EMAIL"
          value = text(td[1].xpath("a"))
        when "Phone:"
          key = "PHONE"
        when "Fax:"
          key = "FAX"
        when "Practice Regions:"
          key = "PRACTICE_REGION"
        when "Accredited Specialists:"
          key = "A_SPECIALISTS"
          value = text(td[1].xpath("a"))
        when "Practice Area(s):"
          key = "PRACTICE_AREAS"
          value = ""
        when "LIV Legal Referral Services:"
          key = "LIV_LRS"
          value = text(td[1].xpath("span/text()|a/text()"))
        when "Languages Spoken:"
          key = "LANGUAGES_SPOKEN"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Other Office(s)"
          key = "OTHER_OFFICES"
          value = text(td[1].xpath("a"))
      end
      puts [records['NAME'],tmp_key,key,value].inspect if not (tmp_key.nil? or tmp_key.empty?) or tmp_key=="\u00A0" and key.nil? 
      records[key]=value unless key.nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['URL'],records,table_name='swdata',verbose=2)
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url="lp_firm_list&type=searchAll&par1=%&par2="
    pg = br.get(BASE_URL+s_url)
    begin
      resp = scrape(pg.body,"list",nil)
      resp.each{|param|
        begin
          pg_tmp = nil
          
          pg.form_with(:id=>'form1') do |f|
            f['__EVENTTARGET']=param
            pg_tmp = f.submit
          end
          scrape(pg_tmp.body,"details",pg_tmp.uri.to_s) unless pg_tmp.nil? 
        rescue Exception => e
          puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
          #retry
        end
      }
    rescue Exception => e
      puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
      #retry
    end #unless exist(param)
  end
end

def trial(s_url)
  pg = Mechanize.new().get(s_url)
  scrape(pg.body,"details",s_url)
end
action(0)
#trial("http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_firm&id=214666")
#trial(BASE_URL+"f?p=102:53:1229407459053091::NO:53:P53_IDE_STRCT_0001:204312")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(" ").strip
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//div[@class='content-box-marginonly']/li").each{|li|
      anchor = li.xpath("a")
      lst << attributes(anchor.xpath("."),"href").gsub(/javascript:__doPostBack\('|'\)|','/,"")
    }
    return lst
  elsif act == "details"
    records={"DOC"=>Time.now.to_s,"URL"=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@style='padding: 10px; border: 1px solid #000000;' and table[@id='Table1']]")
    records['NAME']=text(doc.xpath("h3/span"))#.join(" ")
    doc.xpath("table[@id='Table1']/tr[not(normalize-space(td[@class='style1'])='')]").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("b/text()|text()|span/text()"))
      key = nil
      value = text(td[1].xpath("span"))
      case tmp_key
        when "Office Type:"
          key = "TYPE"
        when "Address:"
          key = "ADDRESS"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Postal Address:"
          key = "POSTAL_ADDRESS"
          value = text(td[1].xpath("div/table/tr/td/span"))
        when "DX:"
          key = "DX"
        when "Website:"
          key = "WEBSITE"
          value = text(td[1].xpath("a"))
        when "Email:"
          key = "EMAIL"
          value = text(td[1].xpath("a"))
        when "Phone:"
          key = "PHONE"
        when "Fax:"
          key = "FAX"
        when "Practice Regions:"
          key = "PRACTICE_REGION"
        when "Accredited Specialists:"
          key = "A_SPECIALISTS"
          value = text(td[1].xpath("a"))
        when "Practice Area(s):"
          key = "PRACTICE_AREAS"
          value = ""
        when "LIV Legal Referral Services:"
          key = "LIV_LRS"
          value = text(td[1].xpath("span/text()|a/text()"))
        when "Languages Spoken:"
          key = "LANGUAGES_SPOKEN"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Other Office(s)"
          key = "OTHER_OFFICES"
          value = text(td[1].xpath("a"))
      end
      puts [records['NAME'],tmp_key,key,value].inspect if not (tmp_key.nil? or tmp_key.empty?) or tmp_key=="\u00A0" and key.nil? 
      records[key]=value unless key.nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['URL'],records,table_name='swdata',verbose=2)
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url="lp_firm_list&type=searchAll&par1=%&par2="
    pg = br.get(BASE_URL+s_url)
    begin
      resp = scrape(pg.body,"list",nil)
      resp.each{|param|
        begin
          pg_tmp = nil
          
          pg.form_with(:id=>'form1') do |f|
            f['__EVENTTARGET']=param
            pg_tmp = f.submit
          end
          scrape(pg_tmp.body,"details",pg_tmp.uri.to_s) unless pg_tmp.nil? 
        rescue Exception => e
          puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
          #retry
        end
      }
    rescue Exception => e
      puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
      #retry
    end #unless exist(param)
  end
end

def trial(s_url)
  pg = Mechanize.new().get(s_url)
  scrape(pg.body,"details",s_url)
end
action(0)
#trial("http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_firm&id=214666")
#trial(BASE_URL+"f?p=102:53:1229407459053091::NO:53:P53_IDE_STRCT_0001:204312")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(" ").strip
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    lst = []
    Nokogiri::HTML(data).xpath(".//div[@class='content-box-marginonly']/li").each{|li|
      anchor = li.xpath("a")
      lst << attributes(anchor.xpath("."),"href").gsub(/javascript:__doPostBack\('|'\)|','/,"")
    }
    return lst
  elsif act == "details"
    records={"DOC"=>Time.now.to_s,"URL"=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@style='padding: 10px; border: 1px solid #000000;' and table[@id='Table1']]")
    records['NAME']=text(doc.xpath("h3/span"))#.join(" ")
    doc.xpath("table[@id='Table1']/tr[not(normalize-space(td[@class='style1'])='')]").each{|tr|
      td = tr.xpath("td")
      tmp_key = text(td[0].xpath("b/text()|text()|span/text()"))
      key = nil
      value = text(td[1].xpath("span"))
      case tmp_key
        when "Office Type:"
          key = "TYPE"
        when "Address:"
          key = "ADDRESS"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Postal Address:"
          key = "POSTAL_ADDRESS"
          value = text(td[1].xpath("div/table/tr/td/span"))
        when "DX:"
          key = "DX"
        when "Website:"
          key = "WEBSITE"
          value = text(td[1].xpath("a"))
        when "Email:"
          key = "EMAIL"
          value = text(td[1].xpath("a"))
        when "Phone:"
          key = "PHONE"
        when "Fax:"
          key = "FAX"
        when "Practice Regions:"
          key = "PRACTICE_REGION"
        when "Accredited Specialists:"
          key = "A_SPECIALISTS"
          value = text(td[1].xpath("a"))
        when "Practice Area(s):"
          key = "PRACTICE_AREAS"
          value = ""
        when "LIV Legal Referral Services:"
          key = "LIV_LRS"
          value = text(td[1].xpath("span/text()|a/text()"))
        when "Languages Spoken:"
          key = "LANGUAGES_SPOKEN"
          value = text(td[1].xpath("table/tr/td/span"))
        when "Other Office(s)"
          key = "OTHER_OFFICES"
          value = text(td[1].xpath("a"))
      end
      puts [records['NAME'],tmp_key,key,value].inspect if not (tmp_key.nil? or tmp_key.empty?) or tmp_key=="\u00A0" and key.nil? 
      records[key]=value unless key.nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['URL'],records,table_name='swdata',verbose=2)
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url="lp_firm_list&type=searchAll&par1=%&par2="
    pg = br.get(BASE_URL+s_url)
    begin
      resp = scrape(pg.body,"list",nil)
      resp.each{|param|
        begin
          pg_tmp = nil
          
          pg.form_with(:id=>'form1') do |f|
            f['__EVENTTARGET']=param
            pg_tmp = f.submit
          end
          scrape(pg_tmp.body,"details",pg_tmp.uri.to_s) unless pg_tmp.nil? 
        rescue Exception => e
          puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
          #retry
        end
      }
    rescue Exception => e
      puts "ERROR: While processing #{offset} :: #{e.inspect} :: #{e.backtrace}"
      #retry
    end #unless exist(param)
  end
end

def trial(s_url)
  pg = Mechanize.new().get(s_url)
  scrape(pg.body,"details",s_url)
end
action(0)
#trial("http://www.liv.asn.au/LegalPractice.aspx?Page=LegalPractice/lp_firm&id=214666")
#trial(BASE_URL+"f?p=102:53:1229407459053091::NO:53:P53_IDE_STRCT_0001:204312")

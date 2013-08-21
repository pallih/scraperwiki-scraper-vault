# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://gateway.hamburg.de/hamburggateway/fvp/fv/BBS/SchulenAuskunft/"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//table[@id='GatewayMaster_ContentSection_Wuc_get_Schulen1_UG1']/tr[position()>1]").each{|tr|
      r = {
        "ID"=>text(tr.xpath("td/a")),
        "PARAM"=>attributes(tr.xpath("td/a"),"href").gsub(/javascript:__doPostBack\(\'|\',\'\'\)/,"")
      }
      holder << r 
    }
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records = {'doc'=>Time.now,"schule_id"=>text(doc.xpath(".//td[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1td0']")).split(":").last.strip}
    doc.xpath(".//div[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1_div0']/table[@id='Table2']/tr[td/span]").each{|tr|
      td = tr.xpath("td")
      key = nil
      tmp_key = text(td[0].xpath("span"))
      value = attributes(td[1].xpath("input"),"value")
      case tmp_key
        when "Schulname:"
          key = "Schulname"
        when "Fr\u00C3\u00BChere Schulnamen:"
          key = "Schulnamen"
        when "Leitzeichen:"
          key = "Leitzeichen"
        when "Stra\u00C3\u009Fe/ Hausnummer:"
          key = "Hausnummer"
        when "Postleitzahl/ Ort:"
          key = "Ort"
        when "Geographische Lage:"
          key = "Geographische"
          value = text(td[1].xpath("a"))
        when "\u00C3\u0096ffentliche Verkehrsmittel:"
          key = "Verkehrsmittel"
          value = text(td[1].xpath("a"))
        when "Telefon:"
          key = "Telefon"
        when "Fax:"
          key = "Fax"
        when "E-Mail:"
          key = "email"
          value = text(td[1].xpath("a"))
        when "Homepage:"
          key = "homepage"
          value = text(td[1].xpath("a"))
        when "Rechtsstatus:"
          key = "Rechtsstatus"
        when "Archivschulname:"
          key = "Archivschulname"
        when "Bezirk:"
          key = "Bezirk"
        when "Stadtteil:"
          key = "Stadtteil"
        when "Schulformen:"
          key = "Schulformen"
        when "Ganztagsschule:"
          key = "Ganztagsschule"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "Schulstufen Ganztagsschule:"
          key = "s_Ganztagsschule"
        when "P\u00C3\u00A4dagogischer Mittagstisch:"
          key = "Mittagstisch"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "Kinderhort:"
          key = "Kinderhort"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "F\u00C3\u00B6rderschwerpunkte:"
          key = "funding"
        when "Klassenarten:"
          key = "Klassenarten"
      end
      records[key]=value unless key.nil? 
    }
    
    ScraperWiki.save_sqlite(unique_key=['schule_id'],records,table_name='schule',verbose=2) unless records['schule_id'].nil? or records['schule_id'].empty? 
    #puts records.inspect
    #records = {'doc'=>Time.now,"id"=>text(doc.xpath(".//td[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1td0']")).split(":").last.strip}
    #Nokogiri::HTML(data).xpath(".//div[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1_div1']/table[@id='Table2']/tr").each{|tr|
    #  td=tr.xpath("td")
    #}
    #ScraperWiki.save_sqlite(unique_key='NAME',records,table_name='schule',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
  end
end

def exists(name)
  ScraperWiki.sqliteexecute("select count(*) from swdata where trim(Schulname)=?",[name])['data'][0][0] rescue return 0
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "wfSchulenauskunft.aspx?Bezirk=#{num}&Sid=32"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    lst.each{|r|
      begin
        pg_tmp = nil  
        pg.form_with(:name=>'aspnetForm') do |f|
          f.action=s_url   
          f['__EVENTTARGET'],f['schnellsuche'],f['GatewayMaster:scrollLeft'],f['GatewayMaster:scrollTop']=r['PARAM'],"Suchbegriff",0,0
          pg_tmp = f.submit
        end
        scrape(pg_tmp.body,"details",nil) #unless pg_tmp.nil? 
      rescue Exception => e
        puts "ERROR: While processing #{r['NAME']}:: #{e.inspect} :: #{e.backtrace}"
        #retry if e.inspect =~ /Timeout|TIME|HTTP/
      end #if exists(r['NAME'])==0
    }
    return lst.length
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
  end
end


puts action(7).inspect
#save_metadata("STRT",5)
#range = (1..7).to_a
#strt = get_metadata("STRT",1)
#strt = 1 if strt >=range.length
#range.each_with_index{|num,idx|
#  next if idx < strt
#  action(num)
#  save_metadata("STRT",idx.next)
#}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://gateway.hamburg.de/hamburggateway/fvp/fv/BBS/SchulenAuskunft/"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//table[@id='GatewayMaster_ContentSection_Wuc_get_Schulen1_UG1']/tr[position()>1]").each{|tr|
      r = {
        "ID"=>text(tr.xpath("td/a")),
        "PARAM"=>attributes(tr.xpath("td/a"),"href").gsub(/javascript:__doPostBack\(\'|\',\'\'\)/,"")
      }
      holder << r 
    }
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data)
    records = {'doc'=>Time.now,"schule_id"=>text(doc.xpath(".//td[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1td0']")).split(":").last.strip}
    doc.xpath(".//div[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1_div0']/table[@id='Table2']/tr[td/span]").each{|tr|
      td = tr.xpath("td")
      key = nil
      tmp_key = text(td[0].xpath("span"))
      value = attributes(td[1].xpath("input"),"value")
      case tmp_key
        when "Schulname:"
          key = "Schulname"
        when "Fr\u00C3\u00BChere Schulnamen:"
          key = "Schulnamen"
        when "Leitzeichen:"
          key = "Leitzeichen"
        when "Stra\u00C3\u009Fe/ Hausnummer:"
          key = "Hausnummer"
        when "Postleitzahl/ Ort:"
          key = "Ort"
        when "Geographische Lage:"
          key = "Geographische"
          value = text(td[1].xpath("a"))
        when "\u00C3\u0096ffentliche Verkehrsmittel:"
          key = "Verkehrsmittel"
          value = text(td[1].xpath("a"))
        when "Telefon:"
          key = "Telefon"
        when "Fax:"
          key = "Fax"
        when "E-Mail:"
          key = "email"
          value = text(td[1].xpath("a"))
        when "Homepage:"
          key = "homepage"
          value = text(td[1].xpath("a"))
        when "Rechtsstatus:"
          key = "Rechtsstatus"
        when "Archivschulname:"
          key = "Archivschulname"
        when "Bezirk:"
          key = "Bezirk"
        when "Stadtteil:"
          key = "Stadtteil"
        when "Schulformen:"
          key = "Schulformen"
        when "Ganztagsschule:"
          key = "Ganztagsschule"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "Schulstufen Ganztagsschule:"
          key = "s_Ganztagsschule"
        when "P\u00C3\u00A4dagogischer Mittagstisch:"
          key = "Mittagstisch"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "Kinderhort:"
          key = "Kinderhort"
          value = td[1].xpath("span/input[@disabled='disabled']")? "False":"True"
        when "F\u00C3\u00B6rderschwerpunkte:"
          key = "funding"
        when "Klassenarten:"
          key = "Klassenarten"
      end
      records[key]=value unless key.nil? 
    }
    
    ScraperWiki.save_sqlite(unique_key=['schule_id'],records,table_name='schule',verbose=2) unless records['schule_id'].nil? or records['schule_id'].empty? 
    #puts records.inspect
    #records = {'doc'=>Time.now,"id"=>text(doc.xpath(".//td[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1td0']")).split(":").last.strip}
    #Nokogiri::HTML(data).xpath(".//div[@id='GatewayMaster_ContentSection_Wuc_get_Einzelschule1_UWT1_div1']/table[@id='Table2']/tr").each{|tr|
    #  td=tr.xpath("td")
    #}
    #ScraperWiki.save_sqlite(unique_key='NAME',records,table_name='schule',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
  end
end

def exists(name)
  ScraperWiki.sqliteexecute("select count(*) from swdata where trim(Schulname)=?",[name])['data'][0][0] rescue return 0
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "wfSchulenauskunft.aspx?Bezirk=#{num}&Sid=32"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    lst.each{|r|
      begin
        pg_tmp = nil  
        pg.form_with(:name=>'aspnetForm') do |f|
          f.action=s_url   
          f['__EVENTTARGET'],f['schnellsuche'],f['GatewayMaster:scrollLeft'],f['GatewayMaster:scrollTop']=r['PARAM'],"Suchbegriff",0,0
          pg_tmp = f.submit
        end
        scrape(pg_tmp.body,"details",nil) #unless pg_tmp.nil? 
      rescue Exception => e
        puts "ERROR: While processing #{r['NAME']}:: #{e.inspect} :: #{e.backtrace}"
        #retry if e.inspect =~ /Timeout|TIME|HTTP/
      end #if exists(r['NAME'])==0
    }
    return lst.length
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
  end
end


puts action(7).inspect
#save_metadata("STRT",5)
#range = (1..7).to_a
#strt = get_metadata("STRT",1)
#strt = 1 if strt >=range.length
#range.each_with_index{|num,idx|
#  next if idx < strt
#  action(num)
#  save_metadata("STRT",idx.next)
#}
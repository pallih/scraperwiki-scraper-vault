# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.km.bayern.de/schule/"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "details"
    records = {'DOC'=>Time.now.to_s,'URL'=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@class='vorlesen' and p/strong]")
    return nil if doc.nil? or doc.empty? 
    records['NAME']=text(doc.xpath("p/strong")).join(",")
    addr=text(doc.xpath("p[2]"))#.join(",")
    records['ADDR1'],records['POSTALCODE'],records['ADDR2']=addr.first,addr.last.split(' ').first,addr.last.split(' ').last
    
    records['TEL'],records['FAX'],records['WEB']=text(doc.xpath("p[3]")).join("").gsub(/Telefon: |Fax: |Web: /,':').split(':')[1..3]
    records['NO_OF_SCHOOLS'],records['TYPE'],records['STATUS']=text(doc.xpath("h2[text()='Verwaltungsangaben']/following::p[1]")).join("").gsub(/Schulnummer: |Schulart: |Rechtlicher Status: /,':').split(':')[1..3]
    records['NO_OF_TEACHERS'],records['NO_OF_STUDENTS']=text(doc.xpath("h2[contains(text(),'Eckdaten im Schuljahr')]/following::p[1]")).join("").gsub(/Hauptamtliche Lehrkräfte: |Schüler: /,':').split(':')[1..2]
    records['FACILITIES']=text(doc.xpath("h2[text()='Besondere Betreuungsangebote']/following::p[1]")).join("")
    records['TRAINING']=text(doc.xpath("h2[text()='Ausbildungsrichtungen']/following::p[1]")).join(",")
    #puts records.inspect
    return ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
    
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "#{offset.to_s}.html?re=1"
    pg = br.get(s_url)
    resp = scrape(pg.body,"details",s_url)
    save_metadata("OFFSET",offset.next) unless resp.nil? or resp.empty? 
  rescue Exception => e
    puts "ERROR: While processing #{offset}:: #{e.inspect} :: #{e.backtrace}"
  end
end

#action(4520)
#save_metadata("OFFSET",9253)
strt = get_metadata("OFFSET",1)
endd = strt.to_i+200

(strt..endd).each{|num|
  action(num)
  #break
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.km.bayern.de/schule/"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "details"
    records = {'DOC'=>Time.now.to_s,'URL'=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@class='vorlesen' and p/strong]")
    return nil if doc.nil? or doc.empty? 
    records['NAME']=text(doc.xpath("p/strong")).join(",")
    addr=text(doc.xpath("p[2]"))#.join(",")
    records['ADDR1'],records['POSTALCODE'],records['ADDR2']=addr.first,addr.last.split(' ').first,addr.last.split(' ').last
    
    records['TEL'],records['FAX'],records['WEB']=text(doc.xpath("p[3]")).join("").gsub(/Telefon: |Fax: |Web: /,':').split(':')[1..3]
    records['NO_OF_SCHOOLS'],records['TYPE'],records['STATUS']=text(doc.xpath("h2[text()='Verwaltungsangaben']/following::p[1]")).join("").gsub(/Schulnummer: |Schulart: |Rechtlicher Status: /,':').split(':')[1..3]
    records['NO_OF_TEACHERS'],records['NO_OF_STUDENTS']=text(doc.xpath("h2[contains(text(),'Eckdaten im Schuljahr')]/following::p[1]")).join("").gsub(/Hauptamtliche Lehrkräfte: |Schüler: /,':').split(':')[1..2]
    records['FACILITIES']=text(doc.xpath("h2[text()='Besondere Betreuungsangebote']/following::p[1]")).join("")
    records['TRAINING']=text(doc.xpath("h2[text()='Ausbildungsrichtungen']/following::p[1]")).join(",")
    #puts records.inspect
    return ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
    
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "#{offset.to_s}.html?re=1"
    pg = br.get(s_url)
    resp = scrape(pg.body,"details",s_url)
    save_metadata("OFFSET",offset.next) unless resp.nil? or resp.empty? 
  rescue Exception => e
    puts "ERROR: While processing #{offset}:: #{e.inspect} :: #{e.backtrace}"
  end
end

#action(4520)
#save_metadata("OFFSET",9253)
strt = get_metadata("OFFSET",1)
endd = strt.to_i+200

(strt..endd).each{|num|
  action(num)
  #break
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.km.bayern.de/schule/"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text unless st.text.nil? or st.text.empty?}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "details"
    records = {'DOC'=>Time.now.to_s,'URL'=>s_url}
    doc = Nokogiri::HTML(data).xpath(".//div[@class='vorlesen' and p/strong]")
    return nil if doc.nil? or doc.empty? 
    records['NAME']=text(doc.xpath("p/strong")).join(",")
    addr=text(doc.xpath("p[2]"))#.join(",")
    records['ADDR1'],records['POSTALCODE'],records['ADDR2']=addr.first,addr.last.split(' ').first,addr.last.split(' ').last
    
    records['TEL'],records['FAX'],records['WEB']=text(doc.xpath("p[3]")).join("").gsub(/Telefon: |Fax: |Web: /,':').split(':')[1..3]
    records['NO_OF_SCHOOLS'],records['TYPE'],records['STATUS']=text(doc.xpath("h2[text()='Verwaltungsangaben']/following::p[1]")).join("").gsub(/Schulnummer: |Schulart: |Rechtlicher Status: /,':').split(':')[1..3]
    records['NO_OF_TEACHERS'],records['NO_OF_STUDENTS']=text(doc.xpath("h2[contains(text(),'Eckdaten im Schuljahr')]/following::p[1]")).join("").gsub(/Hauptamtliche Lehrkräfte: |Schüler: /,':').split(':')[1..2]
    records['FACILITIES']=text(doc.xpath("h2[text()='Besondere Betreuungsangebote']/following::p[1]")).join("")
    records['TRAINING']=text(doc.xpath("h2[text()='Ausbildungsrichtungen']/following::p[1]")).join(",")
    #puts records.inspect
    return ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records['NAME'].nil? or records['NAME'].empty? 
    
  end
end

def action(offset)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "#{offset.to_s}.html?re=1"
    pg = br.get(s_url)
    resp = scrape(pg.body,"details",s_url)
    save_metadata("OFFSET",offset.next) unless resp.nil? or resp.empty? 
  rescue Exception => e
    puts "ERROR: While processing #{offset}:: #{e.inspect} :: #{e.backtrace}"
  end
end

#action(4520)
#save_metadata("OFFSET",9253)
strt = get_metadata("OFFSET",1)
endd = strt.to_i+200

(strt..endd).each{|num|
  action(num)
  #break
}

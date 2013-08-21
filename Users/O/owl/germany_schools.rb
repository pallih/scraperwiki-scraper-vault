# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://schulportraets.schleswig-holstein.de/"

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
  if str.length < 1
    return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  else
    tmp = ""
    str.collect{|st| st.text.strip}.join(";")
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,s_url)
  records={'DOC'=>Time.now.to_s,"URL"=>s_url}
  Nokogiri::HTML(data).xpath(".//*[@id='content']/div[@class='teaserBlock']/table/tbody/tr").each{|tr|
    td = tr.xpath("td")
    tmp_key = text(td[0].xpath("."))
    key = nil
    value = text(td[1].xpath("."))
    case tmp_key
      when "Dienststellen Nr."
        key = "ID"
      when "Name"
        key = "NAME"
      when "Namenszusatz"
        key = "SUFFIX"
      when "Organisationsform"
        key = "ORG_FORM"
      when "Ganztagsbetrieb"
        key = "TIMING"
      when "Straße"
        key = "ROAD"
      when "PLZ"
        key = "PLZ"
      when "Ort"
        key = "PLACE"
      when "Schulleiter(-in)"
        key = "HEAD_MASTER"
      when "Träger"
        key = "CARRIER"
      when "Rechtsstatus"
        key = "STATUS"
      when "Telefon"
        key = "TEL"
      when "Fax"
        key = "FAX"
      when "EMail"
        key = "EMAIL"
    end
    records[key]=value unless key.nil? or key.empty? 
  }
  ScraperWiki.save_sqlite(unique_key=['ID'],records,table_name='swdata',verbose=2) unless records['ID'].nil? or records['ID'].empty? 
  return (records['ID'].nil? or records['ID'].empty?) ? nil:1
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "#{'07'+'%05d' % num.to_s}/1-1/"
    pg = br.get(s_url)
    ret = scrape(pg.body,s_url)
    save_metadata("OFFSET",num.next) if ret
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
  end
end

#save_metadata("OFFSET",6000)
(get_metadata("OFFSET",6000)..7000).each{|num|
  action(num)
}
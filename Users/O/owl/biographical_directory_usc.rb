# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bioguide.congress.gov/"


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
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@cellspacing='2']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {}
      r["LAST_NAME"],r["FIRST_NAME"]=text(td[0].xpath("a")).split(",")
      r['P_URL']=attributes(td[0].xpath("a"),"href")
      r["BIRTH"],r["DEATH"]=text(td[1].xpath(".")).split("-")
      r["POSITION"]=text(td[2].xpath("."))
      r["PARTY"]=text(td[3].xpath("."))
      r["STATE"]=text(td[4].xpath("."))
      r["CONGRESS"],r["C_YR"]=text(td[5].xpath(".")).gsub(/\(|\)/,'').split( )
      r["DOC"]=Time.now

    r['LAST_NAME'],r['FIRST_NAME']=records[records.length-1]['LAST_NAME'],records[records.length-1]['FIRST_NAME'] if (r['LAST_NAME'].nil? or r['LAST_NAME'].empty?) and (r['FIRST_NAME'].nil? or r['FIRST_NAME'].empty?)
    r['BIRTH'],r['DEATH']=records[records.length-1]['BIRTH'],records[records.length-1]['DEATH'] if r['BIRTH'].nil? and r['DEATH'].nil? 
    records << r
    #puts r.inspect
   }
   return ScraperWiki.save_sqlite(unique_keys=[],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    
    params = {'congress'=>yr}
    s_url = BASE_URL+"biosearch/biosearch1.asp"
    pg = br.post(s_url,params)
    return scrape(pg.body,"details") unless pg.body =~ /No entries match these criteria/
  end
end

action(Time.new.year.to_i)# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bioguide.congress.gov/"


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
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@cellspacing='2']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {}
      r["LAST_NAME"],r["FIRST_NAME"]=text(td[0].xpath("a")).split(",")
      r['P_URL']=attributes(td[0].xpath("a"),"href")
      r["BIRTH"],r["DEATH"]=text(td[1].xpath(".")).split("-")
      r["POSITION"]=text(td[2].xpath("."))
      r["PARTY"]=text(td[3].xpath("."))
      r["STATE"]=text(td[4].xpath("."))
      r["CONGRESS"],r["C_YR"]=text(td[5].xpath(".")).gsub(/\(|\)/,'').split( )
      r["DOC"]=Time.now

    r['LAST_NAME'],r['FIRST_NAME']=records[records.length-1]['LAST_NAME'],records[records.length-1]['FIRST_NAME'] if (r['LAST_NAME'].nil? or r['LAST_NAME'].empty?) and (r['FIRST_NAME'].nil? or r['FIRST_NAME'].empty?)
    r['BIRTH'],r['DEATH']=records[records.length-1]['BIRTH'],records[records.length-1]['DEATH'] if r['BIRTH'].nil? and r['DEATH'].nil? 
    records << r
    #puts r.inspect
   }
   return ScraperWiki.save_sqlite(unique_keys=[],records,table_name='swdata',verbose=2) unless records.length==0
  end
end



def action(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    
    params = {'congress'=>yr}
    s_url = BASE_URL+"biosearch/biosearch1.asp"
    pg = br.post(s_url,params)
    return scrape(pg.body,"details") unless pg.body =~ /No entries match these criteria/
  end
end

action(Time.new.year.to_i)
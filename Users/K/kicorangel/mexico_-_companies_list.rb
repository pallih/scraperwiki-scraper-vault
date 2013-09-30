# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.siem.gob.mx"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(pg,act)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}/"  
  if act == "old"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellspacing='1']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
      "COMPANY_NAME"=> text(td[0].xpath("a")),
        "URL"=>BASE_URL + attributes(td[0].xpath("a"),"href"),
        "DOC" => Time.now
      }
      r['COMPANY_NUMBER']=r['URL'].split(/=/).last unless r['URL'] == BASE_URL
      records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
    return doc.length
  elsif act == "new"
    doc = Nokogiri::HTML(data).xpath(".//tr[@class='nota_chica']/td/table/tr")
    r = {
      "DOC"=>Time.now,
      "URL" => pg.uri.to_s,
      "COMPANY_NUMBER" => pg.uri.to_s.split(/=/).last,
      "COMPANY_NAME" => text(doc.xpath(".//td[text()='Razon Social']/following-sibling::td//td[@class='actualizacion']"))
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],r,table_name='swdata',verbose=2) unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? 
    return (r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? )? nil : 0
  end
end

def direct(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL+"/siem/portal/consultas/cedDg.asp?siem_id=#{srch}")
  ret = scrape(pg,"new")
  save_metadata("OFFSET",srch.next) unless ret.nil? 
end

def search(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg_no = get_metadata("PG_NO",1)
  params = (pg_no == 1)? {'consulta'=>1,'bandera'=>0,'nombre'=>srch} : {'pag'=>pg_no,'ir'=>pg_no}
  begin
    s_url = BASE_URL + "respuesta.asp?nombre=#{srch}&bandera=0&consulta=1"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)
    max_pg = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='max_pag']"),"value").to_i
    break if pg_no == max_pg or ttl == 0
    pg_no = pg_no +1 
    params = {'pag'=>pg_no,'ir'=>pg_no}
    save_metadata("PG_NO",pg_no)
  end while(true)
  delete_metadata("PG_NO")
end

#range = (0..10).to_a + ('A'..'Z').to_a + ["!",'@','#','$','%','^','&','*','(',')'].to_a
#offset = get_metadata("OFFSET",0)
#offset = 0 if offset >= range.length
#range.each_with_index{|strt,idx|
#  next if idx < offset
#  action(strt)
#  save_metadata("OFFSET",idx.next)
#}

strt = get_metadata("strt",2323468)
endd = strt+2000
(strt..endd).each{|srch|
  direct(srch)
}

#puts scrape(Mechanize.new().get("http://www.siem.gob.mx/siem/portal/consultas/cedDg.asp?siem_id=16419"),"new").inspect# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.siem.gob.mx"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(pg,act)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}/"  
  if act == "old"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellspacing='1']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
      "COMPANY_NAME"=> text(td[0].xpath("a")),
        "URL"=>BASE_URL + attributes(td[0].xpath("a"),"href"),
        "DOC" => Time.now
      }
      r['COMPANY_NUMBER']=r['URL'].split(/=/).last unless r['URL'] == BASE_URL
      records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
    return doc.length
  elsif act == "new"
    doc = Nokogiri::HTML(data).xpath(".//tr[@class='nota_chica']/td/table/tr")
    r = {
      "DOC"=>Time.now,
      "URL" => pg.uri.to_s,
      "COMPANY_NUMBER" => pg.uri.to_s.split(/=/).last,
      "COMPANY_NAME" => text(doc.xpath(".//td[text()='Razon Social']/following-sibling::td//td[@class='actualizacion']"))
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],r,table_name='swdata',verbose=2) unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? 
    return (r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? )? nil : 0
  end
end

def direct(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL+"/siem/portal/consultas/cedDg.asp?siem_id=#{srch}")
  ret = scrape(pg,"new")
  save_metadata("OFFSET",srch.next) unless ret.nil? 
end

def search(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg_no = get_metadata("PG_NO",1)
  params = (pg_no == 1)? {'consulta'=>1,'bandera'=>0,'nombre'=>srch} : {'pag'=>pg_no,'ir'=>pg_no}
  begin
    s_url = BASE_URL + "respuesta.asp?nombre=#{srch}&bandera=0&consulta=1"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)
    max_pg = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='max_pag']"),"value").to_i
    break if pg_no == max_pg or ttl == 0
    pg_no = pg_no +1 
    params = {'pag'=>pg_no,'ir'=>pg_no}
    save_metadata("PG_NO",pg_no)
  end while(true)
  delete_metadata("PG_NO")
end

#range = (0..10).to_a + ('A'..'Z').to_a + ["!",'@','#','$','%','^','&','*','(',')'].to_a
#offset = get_metadata("OFFSET",0)
#offset = 0 if offset >= range.length
#range.each_with_index{|strt,idx|
#  next if idx < offset
#  action(strt)
#  save_metadata("OFFSET",idx.next)
#}

strt = get_metadata("strt",2323468)
endd = strt+2000
(strt..endd).each{|srch|
  direct(srch)
}

#puts scrape(Mechanize.new().get("http://www.siem.gob.mx/siem/portal/consultas/cedDg.asp?siem_id=16419"),"new").inspect
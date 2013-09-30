#encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = 'http://www.concord-sots.ct.gov/'

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape(data,num,url)
    records = {"SCRAPED_NUMBER" => num,"URL"=>url,"DOC"=>Time.now}
    
    tr = Nokogiri::HTML(data).xpath(".//table[@class='bluebg' and @width='100%' and @cellpadding='7' and tr[td[text()='Business Inquiry Details']]]/tr[position()>1]")
    begin
      records['COMPANY_NAME'] = text(tr.xpath("//td[text()='Business Name:']/following-sibling::td[1]/strong/label/text()"))
      records['COMPANY_NUMBER'] = text(tr.xpath("//td[text()='Business Id:']/following-sibling::td[1]/strong/text()"))
      records['TYPE'] = text(tr.xpath("//td[text()='Business Type:']/following-sibling::td[1]/strong/text()"))
      records['STATUS'] = text(tr.xpath("//td[text()='Business Status:']/following-sibling::td[1]/strong/text()"))
      records['CREATION_DT'] = text(tr.xpath("//td[text()='Date Inc/Register:']/following-sibling::td[1]/strong/text()"))
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="SWDATA",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    end unless tr.nil? 
  return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def action(num)
  begin
    br = Mechanize.new { |b|
        b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "CONCORD/PublicInquiry?eid=9744&businessID="+"%07d" % num
    pg = br.get(s_url)
    ret = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless ret.nil? 
  end
end


#save_metadata("OFFSET",1045549)
strt = get_metadata("OFFSET",1045549).to_i
endd = strt+7500
(strt..endd).each{|num|
  action(num) #if iframe.nil? 
}


#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (STATUS text, URL text, COMPANY_NUMBER text, CREATION_DT text, COMPANY_NAME text, SCRAPED_NUMBER int, TYPE text, DOC timestamp)")
#ScraperWiki.sqliteexecute("insert into tmp select status,url,company_number,creation_dt,company_name,scraped_number,type,datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch') from swdata")
#ScraperWiki.sqliteexecute("update tmp set doc = datetime('now') where doc is null or doc =''")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to SWDATA")
#ScraperWiki.commit()

#encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = 'http://www.concord-sots.ct.gov/'

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape(data,num,url)
    records = {"SCRAPED_NUMBER" => num,"URL"=>url,"DOC"=>Time.now}
    
    tr = Nokogiri::HTML(data).xpath(".//table[@class='bluebg' and @width='100%' and @cellpadding='7' and tr[td[text()='Business Inquiry Details']]]/tr[position()>1]")
    begin
      records['COMPANY_NAME'] = text(tr.xpath("//td[text()='Business Name:']/following-sibling::td[1]/strong/label/text()"))
      records['COMPANY_NUMBER'] = text(tr.xpath("//td[text()='Business Id:']/following-sibling::td[1]/strong/text()"))
      records['TYPE'] = text(tr.xpath("//td[text()='Business Type:']/following-sibling::td[1]/strong/text()"))
      records['STATUS'] = text(tr.xpath("//td[text()='Business Status:']/following-sibling::td[1]/strong/text()"))
      records['CREATION_DT'] = text(tr.xpath("//td[text()='Date Inc/Register:']/following-sibling::td[1]/strong/text()"))
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="SWDATA",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    end unless tr.nil? 
  return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def action(num)
  begin
    br = Mechanize.new { |b|
        b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "CONCORD/PublicInquiry?eid=9744&businessID="+"%07d" % num
    pg = br.get(s_url)
    ret = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless ret.nil? 
  end
end


#save_metadata("OFFSET",1045549)
strt = get_metadata("OFFSET",1045549).to_i
endd = strt+7500
(strt..endd).each{|num|
  action(num) #if iframe.nil? 
}


#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (STATUS text, URL text, COMPANY_NUMBER text, CREATION_DT text, COMPANY_NAME text, SCRAPED_NUMBER int, TYPE text, DOC timestamp)")
#ScraperWiki.sqliteexecute("insert into tmp select status,url,company_number,creation_dt,company_name,scraped_number,type,datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch') from swdata")
#ScraperWiki.sqliteexecute("update tmp set doc = datetime('now') where doc is null or doc =''")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to SWDATA")
#ScraperWiki.commit()

#encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = 'http://www.concord-sots.ct.gov/'

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape(data,num,url)
    records = {"SCRAPED_NUMBER" => num,"URL"=>url,"DOC"=>Time.now}
    
    tr = Nokogiri::HTML(data).xpath(".//table[@class='bluebg' and @width='100%' and @cellpadding='7' and tr[td[text()='Business Inquiry Details']]]/tr[position()>1]")
    begin
      records['COMPANY_NAME'] = text(tr.xpath("//td[text()='Business Name:']/following-sibling::td[1]/strong/label/text()"))
      records['COMPANY_NUMBER'] = text(tr.xpath("//td[text()='Business Id:']/following-sibling::td[1]/strong/text()"))
      records['TYPE'] = text(tr.xpath("//td[text()='Business Type:']/following-sibling::td[1]/strong/text()"))
      records['STATUS'] = text(tr.xpath("//td[text()='Business Status:']/following-sibling::td[1]/strong/text()"))
      records['CREATION_DT'] = text(tr.xpath("//td[text()='Date Inc/Register:']/following-sibling::td[1]/strong/text()"))
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="SWDATA",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    end unless tr.nil? 
  return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def action(num)
  begin
    br = Mechanize.new { |b|
        b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "CONCORD/PublicInquiry?eid=9744&businessID="+"%07d" % num
    pg = br.get(s_url)
    ret = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless ret.nil? 
  end
end


#save_metadata("OFFSET",1045549)
strt = get_metadata("OFFSET",1045549).to_i
endd = strt+7500
(strt..endd).each{|num|
  action(num) #if iframe.nil? 
}


#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (STATUS text, URL text, COMPANY_NUMBER text, CREATION_DT text, COMPANY_NAME text, SCRAPED_NUMBER int, TYPE text, DOC timestamp)")
#ScraperWiki.sqliteexecute("insert into tmp select status,url,company_number,creation_dt,company_name,scraped_number,type,datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch') from swdata")
#ScraperWiki.sqliteexecute("update tmp set doc = datetime('now') where doc is null or doc =''")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to SWDATA")
#ScraperWiki.commit()

#encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = 'http://www.concord-sots.ct.gov/'

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape(data,num,url)
    records = {"SCRAPED_NUMBER" => num,"URL"=>url,"DOC"=>Time.now}
    
    tr = Nokogiri::HTML(data).xpath(".//table[@class='bluebg' and @width='100%' and @cellpadding='7' and tr[td[text()='Business Inquiry Details']]]/tr[position()>1]")
    begin
      records['COMPANY_NAME'] = text(tr.xpath("//td[text()='Business Name:']/following-sibling::td[1]/strong/label/text()"))
      records['COMPANY_NUMBER'] = text(tr.xpath("//td[text()='Business Id:']/following-sibling::td[1]/strong/text()"))
      records['TYPE'] = text(tr.xpath("//td[text()='Business Type:']/following-sibling::td[1]/strong/text()"))
      records['STATUS'] = text(tr.xpath("//td[text()='Business Status:']/following-sibling::td[1]/strong/text()"))
      records['CREATION_DT'] = text(tr.xpath("//td[text()='Date Inc/Register:']/following-sibling::td[1]/strong/text()"))
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="SWDATA",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    end unless tr.nil? 
  return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def action(num)
  begin
    br = Mechanize.new { |b|
        b.user_agent_alias = 'Linux Firefox'
    }
    s_url = BASE_URL + "CONCORD/PublicInquiry?eid=9744&businessID="+"%07d" % num
    pg = br.get(s_url)
    ret = scrape(pg.body,num,s_url)
    save_metadata("OFFSET",num.next) unless ret.nil? 
  end
end


#save_metadata("OFFSET",1045549)
strt = get_metadata("OFFSET",1045549).to_i
endd = strt+7500
(strt..endd).each{|num|
  action(num) #if iframe.nil? 
}


#ScraperWiki.sqliteexecute("drop table tmp")
#ScraperWiki.sqliteexecute("CREATE TABLE tmp (STATUS text, URL text, COMPANY_NUMBER text, CREATION_DT text, COMPANY_NAME text, SCRAPED_NUMBER int, TYPE text, DOC timestamp)")
#ScraperWiki.sqliteexecute("insert into tmp select status,url,company_number,creation_dt,company_name,scraped_number,type,datetime(strftime('%s',replace(doc,'+0000','')),'unixepoch') from swdata")
#ScraperWiki.sqliteexecute("update tmp set doc = datetime('now') where doc is null or doc =''")
#ScraperWiki.commit()
#ScraperWiki.sqliteexecute("drop table swdata")
#ScraperWiki.sqliteexecute("alter table tmp rename to SWDATA")
#ScraperWiki.commit()


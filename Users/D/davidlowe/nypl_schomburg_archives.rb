# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://digitalgallery.nypl.org/nypldigital/"

class String
  def join(str)
    self+str
  end
end
class Array
  def pretty
    self.join(";").gsub(/\u00A0|^:|;$/,'').strip
  end
end
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
  tmp = []
  str.collect{|st| tmp << st.text.strip}
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def key(str)
  str.gsub(/\([a-zA-Z]\)/,'').gsub(/\s+|\//,'_').upcase.strip
end

def scrape(data,act,url)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@id='thumbs']/ul/div[@class='newrow']/li")
    doc.each{|li|
      records << BASE_URL + attributes(li.xpath("a[1]"),"href")
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//div[@class='metacaption']")
    record = {"DOC"=>Time.now}
    doc.xpath("h4").each{|ele|
      title = text(ele.xpath(".")).join("")
      pth = ".//following-sibling::text()[preceding-sibling::h4[1][text()='#{title}']]"
      record[key(title)] = text(ele.xpath(pth)).pretty

    }
    record["IMG_URL"] = "http://images.nypl.org/index.php?id=#{record['DIGITAL_ID']}&t=w"
    record["URL"] = url
    return (record['RECORD_ID'].nil? or record['DIGITAL_ID'].nil?)? nil : record
  end
end
def exists(id)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where digital_id=?",[id])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
    s_url = get_metadata("SUB_URL","dgkeysearchresult.cfm?word=div_id%3Asm&sScope=images&sLabel=Manuscripts%2C%20Archives%20and%20Rare%20Books%20Division")
  begin
    pg = br.get(BASE_URL + s_url)
    list = scrape(pg.body,"list",nil)
    records = []
    list.each{|item|
      records << scrape(br.get(item).body,"details",item) if exists(item.scan(/imageID=(.*)\&word/).flatten.first) == 0
    }
    records.delete_if{|r| r.nil? }
    ScraperWiki.save_sqlite(unique_keys=['RECORD_ID','DIGITAL_ID'],records,table_name='swdata',verbose=2) unless records.length == 0
    nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[img[@alt='Next']]"),"href")
    break if nex.nil? or nex.empty? 
    s_url = nex
    save_metadata("SUB_URL",s_url)
  end while(true)
  delete_metadata("SUB_URL")
end

action()
#url = "http://digitalgallery.nypl.org/nypldigital/dgkeysearchdetail.cfm?trg=1&strucID=109876&imageID=76293&word=&s=1&notword=&d=hsh&c=&f=&k=0&lWord=&lField=&sScope=images&sLevel=&sLabel=Photography%20Collection%2C%20Miriam%20and%20Ira%20D%2E%20Wallach%20Division%20of%20Art%2C%20Prints%20and%20Photographs&sort=&total=62590&num=0&imgs=20&pNum=&pos=6"
#puts scrape(Mechanize.new().get(url).body,"details",url).inspect# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://digitalgallery.nypl.org/nypldigital/"

class String
  def join(str)
    self+str
  end
end
class Array
  def pretty
    self.join(";").gsub(/\u00A0|^:|;$/,'').strip
  end
end
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
  tmp = []
  str.collect{|st| tmp << st.text.strip}
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def key(str)
  str.gsub(/\([a-zA-Z]\)/,'').gsub(/\s+|\//,'_').upcase.strip
end

def scrape(data,act,url)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//div[@id='thumbs']/ul/div[@class='newrow']/li")
    doc.each{|li|
      records << BASE_URL + attributes(li.xpath("a[1]"),"href")
    }
    return records
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//div[@class='metacaption']")
    record = {"DOC"=>Time.now}
    doc.xpath("h4").each{|ele|
      title = text(ele.xpath(".")).join("")
      pth = ".//following-sibling::text()[preceding-sibling::h4[1][text()='#{title}']]"
      record[key(title)] = text(ele.xpath(pth)).pretty

    }
    record["IMG_URL"] = "http://images.nypl.org/index.php?id=#{record['DIGITAL_ID']}&t=w"
    record["URL"] = url
    return (record['RECORD_ID'].nil? or record['DIGITAL_ID'].nil?)? nil : record
  end
end
def exists(id)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where digital_id=?",[id])['data'][0][0] rescue return 0
end

def action()
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
    s_url = get_metadata("SUB_URL","dgkeysearchresult.cfm?word=div_id%3Asm&sScope=images&sLabel=Manuscripts%2C%20Archives%20and%20Rare%20Books%20Division")
  begin
    pg = br.get(BASE_URL + s_url)
    list = scrape(pg.body,"list",nil)
    records = []
    list.each{|item|
      records << scrape(br.get(item).body,"details",item) if exists(item.scan(/imageID=(.*)\&word/).flatten.first) == 0
    }
    records.delete_if{|r| r.nil? }
    ScraperWiki.save_sqlite(unique_keys=['RECORD_ID','DIGITAL_ID'],records,table_name='swdata',verbose=2) unless records.length == 0
    nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[img[@alt='Next']]"),"href")
    break if nex.nil? or nex.empty? 
    s_url = nex
    save_metadata("SUB_URL",s_url)
  end while(true)
  delete_metadata("SUB_URL")
end

action()
#url = "http://digitalgallery.nypl.org/nypldigital/dgkeysearchdetail.cfm?trg=1&strucID=109876&imageID=76293&word=&s=1&notword=&d=hsh&c=&f=&k=0&lWord=&lField=&sScope=images&sLevel=&sLabel=Photography%20Collection%2C%20Miriam%20and%20Ira%20D%2E%20Wallach%20Division%20of%20Art%2C%20Prints%20and%20Photographs&sort=&total=62590&num=0&imgs=20&pNum=&pos=6"
#puts scrape(Mechanize.new().get(url).body,"details",url).inspect
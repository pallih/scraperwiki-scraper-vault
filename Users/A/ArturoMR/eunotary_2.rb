# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'


BASE_URL = "http://notaries-directory.eu"

class String
  def d_p
   self.gsub(/[a-z]/,'')
  end
  def date_parse
    Date.parse(self).to_s
  end
  def pretty
    self.gsub(/\n|\t|\r|\u00A0/,'').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip
  end
  def join(str)
    self + str
  end
  def blank?
    return (self.nil? or self.empty?)
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
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
def a_text(str)
  tmp = []
  str.children().collect{|st|
    tmp << st.text.strip.gsub(/\u00A0/,'').strip
  }
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,'').strip
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def exists(id)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from swdata where id=?",[id])['data'][0][0]
  rescue Exception => e
    return 0
  end
end

def scrape(data,act)
  if act == "list"
    doc = JSON.parse(data)
    return doc["items"]
  elsif act == "details"
    doc = JSON.parse(data)
    return doc.delete_if{|k,v| k =~ /geoname|lastnameSearch|externalId|utf8Table|recordsCustody|linkDetailsNational|notarialOrgNationalLink|notarialOrgLocalLink|officeHours|officePlace|language|countryCode|longitude|latitude|languageRecord|url|info|lastModified/}
  end
end

def action(country)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  pg_no = 0
  begin
    pg = br.get(BASE_URL + "/edn/service/notary/json?filter1=country:#{country}&start=#{pg_no}&limit=2500&sort=lastname&dir=asc&ul=en")
    list = scrape(pg.body,"list")
    break if list.length == 0
    list.each{|ele|
      begin
        pg_tmp = br.get(BASE_URL + "/edn/service/notary/#{ele['id']}/json")
        ScraperWiki.save_sqlite(unique_keys=["id"],scrape(pg_tmp.body,"details"),table_name='swdata',verbose=2)
      end if exists(ele["id"]) == 0
    }
    pg_no = pg_no + 1000
  end while(true)
end

codes = ["AUT","BEL","BGR","HRV","CZE","EST","FRA","DEU","GRC","HUN","ITA","LVA","LTU","LUX","MLT","NLD","POL","PRT","ROU","SVK","SVN","ESP"]
offset = get_metadata("offset",0)
offset = 0 if offset >= codes.length
codes.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("offset",idx.next)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'


BASE_URL = "http://notaries-directory.eu"

class String
  def d_p
   self.gsub(/[a-z]/,'')
  end
  def date_parse
    Date.parse(self).to_s
  end
  def pretty
    self.gsub(/\n|\t|\r|\u00A0/,'').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip
  end
  def join(str)
    self + str
  end
  def blank?
    return (self.nil? or self.empty?)
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
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
def a_text(str)
  tmp = []
  str.children().collect{|st|
    tmp << st.text.strip.gsub(/\u00A0/,'').strip
  }
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,'').strip
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def exists(id)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from swdata where id=?",[id])['data'][0][0]
  rescue Exception => e
    return 0
  end
end

def scrape(data,act)
  if act == "list"
    doc = JSON.parse(data)
    return doc["items"]
  elsif act == "details"
    doc = JSON.parse(data)
    return doc.delete_if{|k,v| k =~ /geoname|lastnameSearch|externalId|utf8Table|recordsCustody|linkDetailsNational|notarialOrgNationalLink|notarialOrgLocalLink|officeHours|officePlace|language|countryCode|longitude|latitude|languageRecord|url|info|lastModified/}
  end
end

def action(country)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  pg_no = 0
  begin
    pg = br.get(BASE_URL + "/edn/service/notary/json?filter1=country:#{country}&start=#{pg_no}&limit=2500&sort=lastname&dir=asc&ul=en")
    list = scrape(pg.body,"list")
    break if list.length == 0
    list.each{|ele|
      begin
        pg_tmp = br.get(BASE_URL + "/edn/service/notary/#{ele['id']}/json")
        ScraperWiki.save_sqlite(unique_keys=["id"],scrape(pg_tmp.body,"details"),table_name='swdata',verbose=2)
      end if exists(ele["id"]) == 0
    }
    pg_no = pg_no + 1000
  end while(true)
end

codes = ["AUT","BEL","BGR","HRV","CZE","EST","FRA","DEU","GRC","HUN","ITA","LVA","LTU","LUX","MLT","NLD","POL","PRT","ROU","SVK","SVN","ESP"]
offset = get_metadata("offset",0)
offset = 0 if offset >= codes.length
codes.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("offset",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://www.onapi.gob.do"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Hash
  def strip
    self.collect{|a|a.strip}
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.strip.to_i}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    return JSON.parse(data).first["ID"] rescue nil
  elsif act == "details"
    tmp = JSON.parse(data) rescue nil
    r = {}.merge(rec)
    tmp.collect{|k,v|
      k = "company_number" if k == "Numero"
      k = "company_name" if k == "Texto"
      r[k] = v
    } unless tmp.nil? 
    return r
  end

end
  
def action(id)
  pg = @br.get(BASE_URL+"/busquedas/api/signos/all?tipoBusqueda=1&texto=#{id}&tipo=NO/NO&clase=0&_=1360027963831")
  puts pg.body
  lid = scrape(pg,"list",{})
  record = scrape(@br.get(BASE_URL + "/busquedas/api/signos/detalle?id=#{lid}"),"details",{"doc"=>Time.now}) unless lid.nil? 
  ScraperWiki.save_sqlite(unique_keys=['company_number'],record) unless record.nil? or record.empty? 
  save_metadata("start",id.next) unless record.nil? or record.empty? 
end

start = get_metadata("start",350258)

(start..start+50).each{|id|
  action(id)
  sleep(5)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://www.onapi.gob.do"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Hash
  def strip
    self.collect{|a|a.strip}
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.strip.to_i}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    return JSON.parse(data).first["ID"] rescue nil
  elsif act == "details"
    tmp = JSON.parse(data) rescue nil
    r = {}.merge(rec)
    tmp.collect{|k,v|
      k = "company_number" if k == "Numero"
      k = "company_name" if k == "Texto"
      r[k] = v
    } unless tmp.nil? 
    return r
  end

end
  
def action(id)
  pg = @br.get(BASE_URL+"/busquedas/api/signos/all?tipoBusqueda=1&texto=#{id}&tipo=NO/NO&clase=0&_=1360027963831")
  puts pg.body
  lid = scrape(pg,"list",{})
  record = scrape(@br.get(BASE_URL + "/busquedas/api/signos/detalle?id=#{lid}"),"details",{"doc"=>Time.now}) unless lid.nil? 
  ScraperWiki.save_sqlite(unique_keys=['company_number'],record) unless record.nil? or record.empty? 
  save_metadata("start",id.next) unless record.nil? or record.empty? 
end

start = get_metadata("start",350258)

(start..start+50).each{|id|
  action(id)
  sleep(5)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


BASE_URL = "https://www.onapi.gob.do"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Hash
  def strip
    self.collect{|a|a.strip}
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.strip.to_i}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    return JSON.parse(data).first["ID"] rescue nil
  elsif act == "details"
    tmp = JSON.parse(data) rescue nil
    r = {}.merge(rec)
    tmp.collect{|k,v|
      k = "company_number" if k == "Numero"
      k = "company_name" if k == "Texto"
      r[k] = v
    } unless tmp.nil? 
    return r
  end

end
  
def action(id)
  pg = @br.get(BASE_URL+"/busquedas/api/signos/all?tipoBusqueda=1&texto=#{id}&tipo=NO/NO&clase=0&_=1360027963831")
  puts pg.body
  lid = scrape(pg,"list",{})
  record = scrape(@br.get(BASE_URL + "/busquedas/api/signos/detalle?id=#{lid}"),"details",{"doc"=>Time.now}) unless lid.nil? 
  ScraperWiki.save_sqlite(unique_keys=['company_number'],record) unless record.nil? or record.empty? 
  save_metadata("start",id.next) unless record.nil? or record.empty? 
end

start = get_metadata("start",350258)

(start..start+50).each{|id|
  action(id)
  sleep(5)
}
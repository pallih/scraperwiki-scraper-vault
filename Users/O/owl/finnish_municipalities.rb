# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://en.wikipedia.org"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//div[@id='mw-content-text']/ol/li/a").each{|a|
      records << {"municipality" => attributes(a.xpath("."),"title")}
    }
    return records
  end
end

def action()
  begin
    pg = @br.get(BASE_URL + "/wiki/List_of_Finnish_municipalities")
    ScraperWiki.save_sqlite(unique_keys=['municipality'],scrape(pg,"list",{}))
  end
end

action()
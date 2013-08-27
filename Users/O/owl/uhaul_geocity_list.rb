# encoding: UTF-8
require 'mechanize'
require 'json'
require 'csv'
require 'scrapers/mcf'

BASE_URL = "http://www.uhaul.com"

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
  b.read_timeout = 2400
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

alps = ('a'..'zzz').to_a
astart = get_metadata("alphabet",0)
alps[astart..-1].each{|a|
  pg = @br.get("http://www.uhaul.com/suggest.axd?maxResults=200&type=geo-city&term=#{a}") rescue retry
  tmp = JSON.parse(pg.body)
  records = []
  tmp.collect{|a|
    t = {}
    t['city'],t['state'] = a['value'].split(",").pretty
    records << t
  }
  ScraperWiki.save_sqlite(unique_keys=['city','state'],records)
  astart = astart + 1
  save_metadata("alphabet",astart)
}
# encoding: UTF-8
require 'mechanize'
require 'json'
require 'csv'
require 'scrapers/mcf'

BASE_URL = "http://www.uhaul.com"

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
  b.read_timeout = 2400
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

alps = ('a'..'zzz').to_a
astart = get_metadata("alphabet",0)
alps[astart..-1].each{|a|
  pg = @br.get("http://www.uhaul.com/suggest.axd?maxResults=200&type=geo-city&term=#{a}") rescue retry
  tmp = JSON.parse(pg.body)
  records = []
  tmp.collect{|a|
    t = {}
    t['city'],t['state'] = a['value'].split(",").pretty
    records << t
  }
  ScraperWiki.save_sqlite(unique_keys=['city','state'],records)
  astart = astart + 1
  save_metadata("alphabet",astart)
}
# encoding: UTF-8
require 'mechanize'
require 'json'
require 'csv'
require 'scrapers/mcf'

BASE_URL = "http://www.uhaul.com"

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
  b.read_timeout = 2400
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

alps = ('a'..'zzz').to_a
astart = get_metadata("alphabet",0)
alps[astart..-1].each{|a|
  pg = @br.get("http://www.uhaul.com/suggest.axd?maxResults=200&type=geo-city&term=#{a}") rescue retry
  tmp = JSON.parse(pg.body)
  records = []
  tmp.collect{|a|
    t = {}
    t['city'],t['state'] = a['value'].split(",").pretty
    records << t
  }
  ScraperWiki.save_sqlite(unique_keys=['city','state'],records)
  astart = astart + 1
  save_metadata("alphabet",astart)
}

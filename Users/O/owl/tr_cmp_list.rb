# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ticaretsicilgazetesi.gov.tr"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='table1']/tr[position()>1]").each{|tr|
      records << {
        "company_name" => s_text(tr.xpath("./td[1]/text()")),
        "company_number" => s_text(tr.xpath("./td[2]/text()")),
        "office" => s_text(tr.xpath("./td[3]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('a'..'zzz').to_a + (0..9).to_a 
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    list = scrape(@br.post(BASE_URL + "/english/sorgu_acik.php",{"unvan1"=>"#{srch}_____","gonder"=>"SUBMIT"}),"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    rstart = rstart + 1
    save_metadata("alphabet",rstart)
    sleep(10)
  }
  delete_metadata("alphabet")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ticaretsicilgazetesi.gov.tr"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='table1']/tr[position()>1]").each{|tr|
      records << {
        "company_name" => s_text(tr.xpath("./td[1]/text()")),
        "company_number" => s_text(tr.xpath("./td[2]/text()")),
        "office" => s_text(tr.xpath("./td[3]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('a'..'zzz').to_a + (0..9).to_a 
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    list = scrape(@br.post(BASE_URL + "/english/sorgu_acik.php",{"unvan1"=>"#{srch}_____","gonder"=>"SUBMIT"}),"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    rstart = rstart + 1
    save_metadata("alphabet",rstart)
    sleep(10)
  }
  delete_metadata("alphabet")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.ticaretsicilgazetesi.gov.tr"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='table1']/tr[position()>1]").each{|tr|
      records << {
        "company_name" => s_text(tr.xpath("./td[1]/text()")),
        "company_number" => s_text(tr.xpath("./td[2]/text()")),
        "office" => s_text(tr.xpath("./td[3]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('a'..'zzz').to_a + (0..9).to_a 
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    list = scrape(@br.post(BASE_URL + "/english/sorgu_acik.php",{"unvan1"=>"#{srch}_____","gonder"=>"SUBMIT"}),"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    rstart = rstart + 1
    save_metadata("alphabet",rstart)
    sleep(10)
  }
  delete_metadata("alphabet")
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.dbo.ca.gov"

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
  def key
    self.gsub(/\s|#|\&/,'').downcase
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def keys
    self.collect{|a| a.gsub(/Institution Name|Company Name|Trust Company/,'company').gsub(/Officer Name|Contact Name|CEO/,'officer').gsub(/\s|#|\&/,'').downcase}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data)
    doc.xpath(".//table[@class='db_table']").each{|tbl|
      directory = a_text(tbl.xpath("./preceding-sibling::*[1]")).join("").strip
      keys = a_text(tbl.xpath("./tr[1]/th")).delete_if{|a| a.nil? or a.empty?}.keys

      tbl.xpath("./tr[position()>1]").each{|tr|
        r = {"directory"=>directory}
        tr.xpath("./td").each_with_index{|td,idx|
          raise "Invalid key column for index #{idx} => #{keys} ||#{tr} || #{td}" if keys[idx].nil? 
          if idx == 2
            tmp = attributes(td.xpath("./a"),"href")
            r['website'] = tmp unless tmp.nil? or tmp.empty? 
          end
          r[keys[idx]] = a_text(td.xpath(".")).join("").strip
        }
        records << r.merge(rec)
      }
    }
    return records
  elsif act == "oc"
    da = JSON.parse(data)['results']['companies']
    da.each{|a|
      return a['company']['opencorporates_url'] if a['company']['name'].downcase == rec['company'].downcase
    }
    return nil
  end
end

def action()
  list = scrape(@br.get("http://www.dbo.ca.gov/Licensees/financial_institutions_directory.asp?DATA="),"list",{})
  lstart = get_metadata("list",0)
  list[lstart..-1].each_with_index{|r,idx|
    pg = @br.get("http://api.opencorporates.com/v0.2/companies/search?api_token=mw37UvELxxjNwLI4KMc2&q=#{r['company']}")
    puts r.inspect
    puts pg.body
    oc_url = scrape(pg,"oc",r)
    r['opencorporates_url'] = oc_url
    ScraperWiki.save_sqlite(['license'],r)

    lstart = lstart + 1
    save_metadata("list",lstart)
    sleep(2)
  }
  delete_metadata("list")
end

action()
#puts scrape(@br.get("http://api.opencorporates.com/v0.2/companies/search?q=Atchison%20Village%20Credit%20Union"),"oc",{"company"=>"ATCHISON VILLAGE CREDIT UNION"}).inspect# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.dbo.ca.gov"

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
  def key
    self.gsub(/\s|#|\&/,'').downcase
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
  def keys
    self.collect{|a| a.gsub(/Institution Name|Company Name|Trust Company/,'company').gsub(/Officer Name|Contact Name|CEO/,'officer').gsub(/\s|#|\&/,'').downcase}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data)
    doc.xpath(".//table[@class='db_table']").each{|tbl|
      directory = a_text(tbl.xpath("./preceding-sibling::*[1]")).join("").strip
      keys = a_text(tbl.xpath("./tr[1]/th")).delete_if{|a| a.nil? or a.empty?}.keys

      tbl.xpath("./tr[position()>1]").each{|tr|
        r = {"directory"=>directory}
        tr.xpath("./td").each_with_index{|td,idx|
          raise "Invalid key column for index #{idx} => #{keys} ||#{tr} || #{td}" if keys[idx].nil? 
          if idx == 2
            tmp = attributes(td.xpath("./a"),"href")
            r['website'] = tmp unless tmp.nil? or tmp.empty? 
          end
          r[keys[idx]] = a_text(td.xpath(".")).join("").strip
        }
        records << r.merge(rec)
      }
    }
    return records
  elsif act == "oc"
    da = JSON.parse(data)['results']['companies']
    da.each{|a|
      return a['company']['opencorporates_url'] if a['company']['name'].downcase == rec['company'].downcase
    }
    return nil
  end
end

def action()
  list = scrape(@br.get("http://www.dbo.ca.gov/Licensees/financial_institutions_directory.asp?DATA="),"list",{})
  lstart = get_metadata("list",0)
  list[lstart..-1].each_with_index{|r,idx|
    pg = @br.get("http://api.opencorporates.com/v0.2/companies/search?api_token=mw37UvELxxjNwLI4KMc2&q=#{r['company']}")
    puts r.inspect
    puts pg.body
    oc_url = scrape(pg,"oc",r)
    r['opencorporates_url'] = oc_url
    ScraperWiki.save_sqlite(['license'],r)

    lstart = lstart + 1
    save_metadata("list",lstart)
    sleep(2)
  }
  delete_metadata("list")
end

action()
#puts scrape(@br.get("http://api.opencorporates.com/v0.2/companies/search?q=Atchison%20Village%20Credit%20Union"),"oc",{"company"=>"ATCHISON VILLAGE CREDIT UNION"}).inspect
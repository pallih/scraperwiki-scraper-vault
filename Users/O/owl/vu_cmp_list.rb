# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://vfsc.vu"

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
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//div[contains(@class,'spEntriesListCell')]").each{|div|
      r = {
        "company_name" => s_text(div.xpath("./span[@class='spEntriesListTitle']/a/text()")),
        "company_number" => s_text(div.xpath("./div[contains(@class,'field_company_number')]/text()")),
        "suffix" => s_text(div.xpath("./div[contains(@class,'field_suffix')]/text()")),
        "inc_dt" => s_text(div.xpath("./div[contains(@class,'spField') and contains(strong/text(),'Incorporation Date')]/text()")),
        "link" => append_base(BASE_URL,attributes(div.xpath("./span[@class='spEntriesListTitle']/a"),"href")),
      }
      r["located_in"] = (r["link"] =~ /international-companies/)? "International Companies":"Local Companies"
      records << r.merge(rec)
    }
    return records
  elsif act == "details"
    r = {"link"=>pg.uri.to_s}
    doc = Nokogiri::HTML(data)
    r["company_name"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/h1[@class='SPTitle']/text()"))
    r["company_number"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'field_company_number')]/text()"))
    r["suffix"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'field_suffix') and contains(strong/text(),'Suffix:')]/text()"))
    r["inc_dt"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spField') and contains(strong/text(),'Incorporation Date:')]/text()"))
    r["struck_off_dt"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spField') and contains(strong/text(),'Struck Off Date:')]/text()"))
    r["located_in"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spEntryCats')]/a[1]/text()"))

    return r.merge(rec)
  end
end

def search()
  pg = @br.post(BASE_URL+"/index.php/listings/search")
  params = {"sp_search_for"=>"search...","search"=>"Search","spsearchphrase"=>"all"}
  pg.form_with(:id=>"spSearchForm") do |f|
    params.each{|k,v| f[k] = v}
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  pg = @br.get(BASE_URL + "/index.php/listings/search/results?site=#{pg_no}") if pg_no != 1
  begin
    records = scrape(pg,"list",{"doc"=>Time.now})
    
    ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
    break if records.nil? or records.length < 500

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.get(BASE_URL + "/index.php/listings/search/results?site=#{pg_no}")
  end while(true)
  delete_metadata("page_no")
end

def action()
  lstart = ScraperWiki.select("max(id) as maxid from ocdata").first['maxid']
  (lstart..lstart+10).each{|id|
    pg = @br.get("http://vfsc.vu/index.php/listings/#{id}") rescue nil
    next if pg.nil? 
    r = scrape(pg,"details",{"doc"=>Time.now,"id"=>id})
    ScraperWiki.save_sqlite(['company_number'],r,'ocdata') unless r['company_number'].nil? or r['company_number'].empty? 
    sleep(5)
  }
end

action()

#puts scrape(@br.get("http://vfsc.vu/index.php/listings/8141"),"details",{})# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://vfsc.vu"

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
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//div[contains(@class,'spEntriesListCell')]").each{|div|
      r = {
        "company_name" => s_text(div.xpath("./span[@class='spEntriesListTitle']/a/text()")),
        "company_number" => s_text(div.xpath("./div[contains(@class,'field_company_number')]/text()")),
        "suffix" => s_text(div.xpath("./div[contains(@class,'field_suffix')]/text()")),
        "inc_dt" => s_text(div.xpath("./div[contains(@class,'spField') and contains(strong/text(),'Incorporation Date')]/text()")),
        "link" => append_base(BASE_URL,attributes(div.xpath("./span[@class='spEntriesListTitle']/a"),"href")),
      }
      r["located_in"] = (r["link"] =~ /international-companies/)? "International Companies":"Local Companies"
      records << r.merge(rec)
    }
    return records
  elsif act == "details"
    r = {"link"=>pg.uri.to_s}
    doc = Nokogiri::HTML(data)
    r["company_name"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/h1[@class='SPTitle']/text()"))
    r["company_number"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'field_company_number')]/text()"))
    r["suffix"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'field_suffix') and contains(strong/text(),'Suffix:')]/text()"))
    r["inc_dt"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spField') and contains(strong/text(),'Incorporation Date:')]/text()"))
    r["struck_off_dt"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spField') and contains(strong/text(),'Struck Off Date:')]/text()"))
    r["located_in"] = s_text(doc.xpath(".//div[@class='SPDetailEntry']/div[contains(@class,'spEntryCats')]/a[1]/text()"))

    return r.merge(rec)
  end
end

def search()
  pg = @br.post(BASE_URL+"/index.php/listings/search")
  params = {"sp_search_for"=>"search...","search"=>"Search","spsearchphrase"=>"all"}
  pg.form_with(:id=>"spSearchForm") do |f|
    params.each{|k,v| f[k] = v}
    pg = f.submit
  end
  pg_no = get_metadata("page_no",1)
  pg = @br.get(BASE_URL + "/index.php/listings/search/results?site=#{pg_no}") if pg_no != 1
  begin
    records = scrape(pg,"list",{"doc"=>Time.now})
    
    ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
    break if records.nil? or records.length < 500

    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)

    pg = @br.get(BASE_URL + "/index.php/listings/search/results?site=#{pg_no}")
  end while(true)
  delete_metadata("page_no")
end

def action()
  lstart = ScraperWiki.select("max(id) as maxid from ocdata").first['maxid']
  (lstart..lstart+10).each{|id|
    pg = @br.get("http://vfsc.vu/index.php/listings/#{id}") rescue nil
    next if pg.nil? 
    r = scrape(pg,"details",{"doc"=>Time.now,"id"=>id})
    ScraperWiki.save_sqlite(['company_number'],r,'ocdata') unless r['company_number'].nil? or r['company_number'].empty? 
    sleep(5)
  }
end

action()

#puts scrape(@br.get("http://vfsc.vu/index.php/listings/8141"),"details",{})
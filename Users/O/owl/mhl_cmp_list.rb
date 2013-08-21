# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.register-iri.com/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


class String
  def pretty
    self.strip
  end  
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"  
  if act == "list"
    records = []
    da = JSON.parse(data)["ROWS"]
    da.each{|d|
      r = {
        "company_id" => d[0],
        "link" => "http://www.register-iri.com/miCorporate/index.cfm/Corporate/details?id=#{d[0]}",
        "company_number" => d[1],
        "company_name" => d[2],
        "status" => d[5],
        "doc" => Time.now
      }
      records << r #if r['status'] == 'Active'
    }
    return records
  end
end

def action()
  s_url = BASE_URL + "/miCorporate/index.cfm/Corporate/results"
  params = {"CORP_NUMBER"=>"","CORP_NAME"=>"__","search_type"=>"bwu","Find"=>"Submit"}
  pg = @br.post(s_url,params)
  pg_no = get_metadata("pg_no",1)
  s_url = BASE_URL + "/miCorporate/handlers/Corporate.cfc?method=getCorpNames"
  params = {"filters"=>'{"groupOp":"AND","rules":[{"field":"corp_number","op":"eq","data":""},{"field":"corp_name","op":"bwu","data":"__"},{"field":"corp_type","op":"eq","data":""},{"field":"status","op":"eq","data":""}]}',"_search"=>"true","rows"=>2500,"page"=>pg_no,"sidx"=>"corp_name","sord"=>"asc"}
  begin
    pg = @br.post(s_url,params)
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.empty? 
    break if list.length == 0

    pg_no = pg_no + 1
    params["page"] = pg_no
    save_metadata("pg_no",pg_no)
  end while(true)
  delete_metadata("pg_no")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.register-iri.com/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


class String
  def pretty
    self.strip
  end  
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"  
  if act == "list"
    records = []
    da = JSON.parse(data)["ROWS"]
    da.each{|d|
      r = {
        "company_id" => d[0],
        "link" => "http://www.register-iri.com/miCorporate/index.cfm/Corporate/details?id=#{d[0]}",
        "company_number" => d[1],
        "company_name" => d[2],
        "status" => d[5],
        "doc" => Time.now
      }
      records << r #if r['status'] == 'Active'
    }
    return records
  end
end

def action()
  s_url = BASE_URL + "/miCorporate/index.cfm/Corporate/results"
  params = {"CORP_NUMBER"=>"","CORP_NAME"=>"__","search_type"=>"bwu","Find"=>"Submit"}
  pg = @br.post(s_url,params)
  pg_no = get_metadata("pg_no",1)
  s_url = BASE_URL + "/miCorporate/handlers/Corporate.cfc?method=getCorpNames"
  params = {"filters"=>'{"groupOp":"AND","rules":[{"field":"corp_number","op":"eq","data":""},{"field":"corp_name","op":"bwu","data":"__"},{"field":"corp_type","op":"eq","data":""},{"field":"status","op":"eq","data":""}]}',"_search"=>"true","rows"=>2500,"page"=>pg_no,"sidx"=>"corp_name","sord"=>"asc"}
  begin
    pg = @br.post(s_url,params)
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.empty? 
    break if list.length == 0

    pg_no = pg_no + 1
    params["page"] = pg_no
    save_metadata("pg_no",pg_no)
  end while(true)
  delete_metadata("pg_no")
end

action()
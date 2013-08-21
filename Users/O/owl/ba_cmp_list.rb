# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://bizreg.pravosudje.ba/pls/apex/"

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

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[contains(@id,'report_')]/tr[position()>1 and position()<last()]").each{|tr|
      td = tr.xpath("td")
      records << {
        "company_number" => s_text(td[0].xpath("./text()")),
        "company_name" => s_text(td[1].xpath("./a/text()")),
        "link" => BASE_URL +  attributes(td[1].xpath("./a"),"href"),
        "addr" => s_text(td[3].xpath("./text()")),
        "status" => s_text(td[4].xpath("./text()")),
        "doc" => Time.now
      }
    }
    return records
  elsif act == "params"
    doc = Nokogiri::HTML(data).xpath(".")
    r = {"p_request"=>"APPLICATION_PROCESS=OSNOVNA_PRETRAGA_PARAMS"}
    r["p_instance"] = attributes(doc.xpath(".//input[@name='p_instance']"),"value")
    r["p_flow_id"] = "186"
    r["p_flow_step_id"] = "0"
    r["x01"] = "-1"
    r["x02"] = "2"
    r["x04"] = ""
    return r.merge(rec)
  end
end

def action(s)
  @pg = @br.get("http://bizreg.pravosudje.ba/pls/apex/f?p=186:20:2742911740406467::NO::P20_SEKCIJA_TIP:PRETRAGA")
  params = scrape(@pg.body,"params",{"x03"=>"#{s}__"})
  @pg = @br.post("http://bizreg.pravosudje.ba/pls/apex/wwv_flow.show",params)
  params = {}
  start = 1
  begin
    records = scrape(@br.post(BASE_URL + "f?p=186:30:2742911740406467::NO:RP:P30_FIRSTTIME:TRUE",params).body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records) unless records.empty? 
    start = (records.empty?)? 1 : (start + 30)
    params = {"p"=>"186:30:2742911740406467:FLOW_PPR_OUTPUT_R12375225389856517_pg_R_12375225389856517:NO","pg_max_rows"=>30,"pg_min_row"=>start,"pg_rows_fetched"=>30}
    break if records.empty? 
  end while(true)
end

range = ('A'..'ZZZ').to_a + (0..99).to_a
#save_metadata("start",1)
start = get_metadata("start",0)
start = 0 if start >= range.length
range[start..-1].to_a.each{|srch|
  action(srch)
}

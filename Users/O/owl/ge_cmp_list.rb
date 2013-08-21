# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'logger'
require 'scrapers/cf'

BASE_URL = "https://enreg.reestri.gov.ge"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").strip
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
    Nokogiri::HTML(data).xpath(".//table[@class='main_tbl shadow']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      if td.length < 6
        puts tr.inner_html
        next
      end
      records << {
        "company_number" => attributes(td[0].xpath("./a"),"onclick").split("(").last.gsub(")",""),
        "i_code" => s_text(td[1].xpath("./span/text()")),
        "p_code" => s_text(td[2].xpath("./span/text()")),
        "company_name" => s_text(td[3].xpath("./text()")),
        "type" => s_text(td[4].xpath("./text()")),
        "status" => s_text(td[5].xpath("./span/text()")),
        "link" => BASE_URL + "/main.php?c=app&m=show_legal_person&legal_code_id=#{attributes(td[0].xpath('./a'),'onclick').split('(').last.gsub(')','')}",
        "doc" => Time.now
      }
    }
    ScraperWiki.save_sqlite(unique_keys=["company_number"],records,table_name='swdata',verbose=2) unless records.empty? 
  end
end

def action()
  hdr = {"X-Requested-With"=>"XMLHttpRequest","cookie"=>"MMR_PUBLIC=7ip3pu3gh4phbaen4f8kpjoi54"}
  params = {"c"=>"search","m"=>"find_legal_persons","s_legal_person_idnumber"=>"","s_legal_person_name"=>"__","s_legal_person_form"=>"0" }
  n = get_metadata("n",1)
  begin
    pg = @br.post(BASE_URL + "/main.php",params,hdr)
    scrape(pg.body,"list",{})
    nex = attributes(Nokogiri::HTML(pg.body).xpath(".//td/a[img[contains(@src,'next.png')]]"),"onclick").scan(/legal_person_paginate\((\d+)\)/).flatten.first
    break if nex.nil? 
    n = n + 1
    save_metadata("n",n)
    params = {"c"=>"search","m"=>"find_legal_persons","p"=>n}
  end while(true)
  delete_metadata("n")
end

action()
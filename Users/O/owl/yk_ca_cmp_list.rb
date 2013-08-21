# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.directoryyukon.com"
  
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
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//div[@class='results-column']/div[@class='inf-block']").each{|div|
      r = {}
      r["company_name"] = s_text(div.xpath("./strong/text()"))
      r["description"] = a_text(div.xpath("./p")).join(" ").strip

      tmp = s_text(div.xpath("./dl[@class='result']/dt[text()='Address:']/following-sibling::*[1][self::dd]/text()")).split(",").strip.reverse
      #r["address"],r["town"],r["province"],r["zipcode"] = tmp
      r["zipcode"] = tmp[0]
      r["province"] = tmp[1]
      r["town"] = tmp[2]
      r["address"] = tmp[3..-1].reverse.join(" , ").strip

      tmp = a_text(div.xpath("./dl[@class='result']/dt[text()='Phone:']/following-sibling::*[1][self::dd]")).join("|").split("|").strip
      r["phone"] = tmp[0] rescue nil
      t = tmp.select{|a| a =~ /^fax/}.first.split(" ")[1..-1].join(" ").strip rescue nil
      r["fax"] = t unless t.nil? or t.empty? or t == "None Provided"
      r["email"] = tmp[tmp.index("email")+1].downcase rescue nil
      
      tmp = s_text(div.xpath("./dl[@class='result']/dt[text()='url:']/following-sibling::*[1][self::dd]/text()"))
      r["website"] = tmp unless tmp.nil? or tmp.empty? or tmp == "None Provided"

      tmp = s_text(div.xpath("./dl[@class='result']/dt[text()='Industry:']/following-sibling::*[1][self::dd]/text()")).split(",").strip
      r["industry"] = JSON.generate tmp unless tmp.nil? or tmp.empty? 

      r["doc"] = Time.now
      records << r.merge(rec)
    }
    return records
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    list = scrape(@br.get(BASE_URL + "/results.php?page=#{pg_no}"),"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_name'],list)
    break if list.nil? or list.empty? or list.length < 8
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
    sleep(10)
  end while(true)
  delete_metadata("page_no")
end

action()

#puts scrape(@br.get("http://www.directoryyukon.com/results.php?page=1"),"list",{})
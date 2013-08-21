# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.blue.co.za"
DATE = Time.now.to_i

class String
  def join(str)
    return self+str
  end
end
def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  end
end

def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,country_code)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//div[@class='flow branches']")
  doc.each{|ele|
    r = {
      "DATE_SCRAPED"=>DATE,
      "BRANCH"=>text(ele.xpath("h4")),
      "TOWN"=>text(ele.xpath("h4")).gsub(/\(.*\)/, ""),
      "ADDRESS"=>ele.xpath("p[label[text()='address: ']]/text()").text.strip,
      "B_MGR"=>ele.xpath("p[label[text()='branch manager: ']]/text()").text.strip,
      "TELEPHONE"=>ele.xpath("p[label[text()='tel number: ']]/text()").text.strip,
      "MOBILE"=>ele.xpath("p[label[text()='cell number: ']]/text()").text.strip,
      "FAX"=>ele.xpath("p[label[text()='fax: ']]/text()").text.strip,
      "EMAIL"=>ele.xpath("p[label[text()='email: ']]/text()").text.strip,
      "COUNTRY"=>@range["#{country_code}"],
      "DOC"=>Time.now
    }
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['BRANCH', 'DATE_SCRAPED'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
    s_url = BASE_URL+"/OurBranches/SearchResult"
    pg = br.post(s_url,{"Country"=>srch,"search"=>""})
    scrape(pg.body,srch)
  rescue Exception => e
   raise e
  end
end

@range = {"1"=>"South Africa","2"=>"Botswana","3"=>"Zambia","4"=>"Tanzania","5"=>"Uganda","6"=>"Lesotho","7"=>"Malawi",
"8"=>"Namibia","9"=>"Kenya","10"=>"Nigeria","11"=>"Swaziland","12"=>"Rwanda","13"=>"Cameroon","14"=>"Ghana"}
action(1)
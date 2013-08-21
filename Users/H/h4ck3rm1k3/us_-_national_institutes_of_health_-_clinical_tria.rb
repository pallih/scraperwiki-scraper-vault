# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.kpaonline.org"

class String
  def last
    return ""
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
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'')}
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def key(str)
  return str.strip.gsub(/\u00A0|[!@#\$%^&*()]/,"").strip.gsub(/ /,"_").upcase
end

def scrape(data,act)
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".//table[@class='data_table']//tr[th and td]")
    records = {"DOC"=>Time.now}
    doc.each{|ele|
      records[key(ele.xpath("th/text()").text)] = text(ele.xpath("td"))
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["NCT_NUMBER"],records,table_name='swdata',verbose=2) unless records['NCT_NUMBER'].nil? or records['NCT_NUMBER'].empty? 
  elsif act == "list"
    doc = Nokogiri::HTML(data).xpath(".//table[@class='layout_table footer']//tr/td/a")
    records = []
    doc.collect {|a| records << attributes(a.xpath("."),"href").split(/\//).last }
    return records
  end
end

def action(srch,act)
  begin
    if act == "list"
      pg = @br.get(BASE_URL+"/ct2/crawl/#{srch}")
      return scrape(pg.body,"list")
 
# http://www.kpaonline.org/viewOnMap/result.aspx?is=KPA00449
  elsif act == "details"
      pg = @br.get(BASE_URL+"/viewOnMap/result.aspx?is=#{srch}")
      scrape(pg.body,"details")
  
#
#municipalities  http://www.kpaonline.org/AdminM.aspx?mun=Prizren

    end
  rescue Exception => e
    puts [srch,e].inspect
    retry unless e.inspect =~ /SqliteException|interrupt/i
  end
end

def exists(nct)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where nct_number=?",[nct])['data'][0][0] rescue 0
end

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
}

strt = get_metadata("CRAWL",0)
endd = strt + 10

(strt..endd).each{|crawl|
  lst = action(crawl,"list")
  lst.each{|nct|
    action(nct,"details") unless exists(nct) > 0
  }
  save_metadata("CRAWL",strt.next) unless lst.nil? or lst.empty? 
}
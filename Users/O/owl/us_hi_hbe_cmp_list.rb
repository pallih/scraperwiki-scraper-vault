#encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'hpricot'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://hbe.ehawaii.gov"

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
    end
end

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete(#{key})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
    records = []
    doc = Nokogiri::HTML(data).xpath(".//*[@id='table1']/table[1]/tr[position()>1]")
    doc.each do|tr|
      td = tr.xpath("td")
      r = {
         "COMPANY_NAME" => text(td[0].xpath("a")),
         "URL" => BASE_URL+attributes(td[0].xpath("a"),"href"),
         "RECORD_TYPE" => text(td[1].xpath(".")),
         "COMPANY_NUMBER" => text(td[2].xpath(".")),
         "TYPE" => text(td[3].xpath(".")),
         "STATUS" => text(td[4].xpath("span")),
         "DOC" => Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? or r['RECORD_TYPE'] =~ /Trade/ or r['RECORD_TYPE']=="Temporary Name" or r['RECORD_TYPE']=="Name Reservation"
    end
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0 
    return doc.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.retry_change_requests = true
    }
    s_url = BASE_URL + "/documents/search.html?beginsWith=true&query=#{srch}&page=0&recordType=ALL&status=ALL"
    pg = br.get(s_url)
    return srch,scrape(pg.body)
  end
end


#puts ScraperWiki.sqliteexecute("delete from swdata where record_type like 'Trade%' or record_type like 'Temporary%' or record_type == 'Name Reservation'")
#puts ScraperWiki.commit()
#save_metadata("OFFSET",477)
range = (0..10).to_a + ('A0'..'Z9').to_a + ('AAA'..'ZZZ').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
  sleep(10)
}
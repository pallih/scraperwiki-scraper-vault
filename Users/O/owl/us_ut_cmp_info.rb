# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://secure.utah.gov"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//div[@class='entities']/div[@class='entityRow']").each{|row|
    r={
      "COMPANY_NAME"=>text(row.xpath("div[@class='entityName']/a")),
      "STATUS"=>text(row.xpath("div[@class='entityDetails']/div[@class='detailStatus']")),
      "TYPE"=>text(row.xpath("div[@class='entityDetails']/div[@class='detailType']")),
      "CITY"=>text(row.xpath("div[@class='entityDetails']/div[@class='detailCity']")),
      "URL"=>BASE_URL+attributes(row.xpath("div[@class='entityName']/a"),"href")
    }
    r["COMPANY_NUMBER"]=r["URL"].split('entity=').last
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = {"track"=>6, "name"=>srch, "index.searchByName"=>"Search", "type"=>"beginning" }
    pg = br.post(BASE_URL+"/bes/action/searchresults",params) rescue retry
    ttl_cnt = pg.body.scan(/Total Results:(.*)/).flatten.first.to_f
    pg_cnt = (ttl_cnt/50).ceil
    scrape(pg.body)
    (1..pg_cnt).each{|pgno|
      begin
        pg_tmp = br.get(BASE_URL+"/bes/action/searchresults?pageNo=#{pgno}")
        scrape(pg_tmp.body)
      rescue Exception=>e
        puts [srch,pgno,e].inspect
        retry unless e.inspect =~ /interrupt/i
      end
    }
  end
end

save_metadata("OFFSET",675)
range = ('AA'..'ZZ').sort.to_a + (0..10).to_a + ['@','#']
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.dbd.go.th"

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


def scrape(data)
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@border='1']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "DATE"=>text(td[1].xpath(".")),
      "COMPANY_NUMBER"=>text(td[2].xpath(".")),
      "STATUS"=>text(td[3].xpath(".")),
      "COMPANY_NAME"=>text(td[4].xpath(".")),
      "ADDR"=>text(td[5].xpath(".")),
      "DOC"=>Time.now
    } 
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  } if doc.length > 1
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
 begin
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    #b.log = Logger.new(STDERR)
  }
  s_url = BASE_URL + "/corpsearch_test/corpsearch4.phtml?kw=#{srch}&kwtype=partial&sm2=Search#{get_metadata('SEQUENCE','')}"
  pg = br.get(s_url)
  ttl = scrape(pg.body)
  return nil if pg.body =~ /No record found/
  begin
    lnk = pg.link_with(:text=>"Next>>")
    break if lnk.nil? 
    pg = br.click(lnk)
    ttl = ttl + scrape(pg.body)
    #break if ttl >= 25000 
    save_metadata("SEQUENCE","&#{lnk.href.to_s.split("&").last}")
  end while(true)
  delete_metadata("SEQUENCE")
 rescue Exception => e
  puts [srch,e.inspect,e.backtrace].inspect
 end
  return srch,ttl
end

#save_metadata("OFFSET",11767)

#delete_metadata("SEQUENCE")
range = ("A00".."Z99").to_a + ("AAA".."ZZZ").to_a + ('000'..'999').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}
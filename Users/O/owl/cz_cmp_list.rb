# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://wwwinfo.mfcr.cz/cgi-bin/ares/"

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
  doc = Nokogiri::HTML(data).xpath(".//table[@class='TList']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=> text(td[0].xpath(".")),
      "COMPANY_NAME"=> text(td[1].xpath("span")),
      "DOC" => Time.now
    }
    td[2].xpath("a").each{|a|
      r[text(a.xpath(".")).gsub(/ /,"_").upcase] = BASE_URL+attributes(a.xpath("."),"href")
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  begin
    s_url = BASE_URL + "ares_es.cgi?jazyk=en&obch_jm=#{srch}&ico=&cestina=&obec=&k_fu=&maxpoc=1000&ulice=&cis_or=&cis_po=&setrid=ZADNE&pr_for=&nace=&nace_h=&xml=2&filtr=1"
    pg = br.get(s_url)
    scrape(pg.body)
  end
end

range = ('AA'..'ZZ').to_a + ('00'..'99').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range[offset..-1].each_with_index{|strt,idx|
  action(strt)
  save_metadata("OFFSET",offset + idx)
  sleep(5)
}
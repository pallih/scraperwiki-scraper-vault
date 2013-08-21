# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.fundempresa.org.bo/directorio/"

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
  doc = Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//div[@class='left']/div[@class='empresas']")
  doc.each{|div|
    r = {
      "URL"=> BASE_URL + attributes(div.xpath("div[@class='right']/a"),"href"),
      "DOC" => Time.now
    }
    r["COMPANY_NAME"],r["LOCATION"] = text(div.xpath("span")).first#.split("en ")
    r["COMPANY_NUMBER"] = r['URL'].split("=")[1].split("&").first
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
  pg_no = get_metadata("PG_NO",1)
  begin
    s_url = BASE_URL + "listado-de-empresas.php?page=#{pg_no}&rubro=#{srch}&depto=00&seccion=&division=&clase=&searchSW=1&radio=1"
    pg = br.get(s_url)
    ttl = scrape(pg.body)
    pg_no = pg_no + 1
    if ttl == 0 or Nokogiri::HTML(pg.body).xpath(".//a[@title='Siguiente']").empty? 
      delete_metadata("PG_NO")
      break
    end
    save_metadata("PG_NO",pg_no)
  end while(true)
end

#save_metadata("PG_NO",9)

range = (0..10).to_a + ('A'..'Z').to_a + ["!",'@','#','$','%','^','&','*','(',')'].to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index{|strt,idx|
  next if idx < offset
  action(strt)
  save_metadata("OFFSET",idx.next)
}

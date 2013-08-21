require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.londonstockexchange.com"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
  ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end


def scrape(data,act)
  if act=="list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='table_dati']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      r = {
        "DOC"=>Time.now.to_s,
        "CODE" => text(td[0].xpath("text()")),
        "COMPANY_NAME" => text(td[1].xpath("a/text()")),
        "URL" => BASE_URL+attributes(td[1].xpath("a"),"href"),
        "CURRENCY" => text(td[2].xpath("text()")),
      }
      r["ISIN"] = r["URL"].split("=")[1][0..11] unless r["URL"].nil? or r==BASE_URL
      #puts records.inspect
      records << r
    }
    ScraperWiki.save_sqlite(unique_keys=['ISIN'],records,table_name='SWDATA',verbose=2) unless records.length==0
  elsif act=="check"
    return attributes(Nokogiri::HTML(data).xpath(".//a[@title='Next']"),"href")
  end
end


def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg_no = get_metadata("PGNO",1)
    params = "/exchange/prices-and-markets/stocks/prices-search/stock-prices-search.html?initial=#{srch}&page=#{pg_no}"
    begin
      s_url = BASE_URL + params
      pg = br.get(s_url)
      scrape(pg.body,"list")
      params = scrape(pg.body,"check")
      save_metadata("PGNO",pg_no.next)
    rescue Exception => e
      puts "ERROR: While processing #{s_url}:: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry if e.inspect =~ /Timeout|TIME|HTTP/
    end while not params.nil? 

  end
end

range = ("A".."Z").to_a + [0]
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  begin
    action(srch)
  save_metadata("OFFSET",index.next)
  delete_metadata("PGNO")
  end unless index < offset
end
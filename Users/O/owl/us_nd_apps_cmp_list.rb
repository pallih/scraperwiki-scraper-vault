require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://secure.apps.state.nd.us"

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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
      return tmp
    end
  rescue Exception => e
    puts [str,e.inspect].inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//*[@id='BusnSrchFM']//table/tr[position()>1]").each{|tr|
    td = tr.xpath("td")
    type,status = text(td[2].xpath(".")).first.strip.split("-")
    r = {
      "COMPANY_NUMBER" =>text(td[0].xpath(".")),
      "COMPANY_NAME" =>text(td[1].xpath(".")),
      "TYPE" => type.strip,
      "STATUS" => status.strip,
      "DOC" => Time.now
    }
    records << r unless r['TYPE'] == 'Trade Name' or r['TYPE'] == 'Fictitious Name' or r['TYPE'] == 'Trademark' or r['TYPE'] == "Reserved Name" or r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? or r['COMPANY_NUMBER'] = '\u00A0'
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = "srchName=#{srch}&srchSystemId=&srchType=Start&resultsPerPage=400&srchOwnerName=&srchLicenseNo=&srchCity=&srchCounty=&command=Search"
    s_url = BASE_URL + "/sc/busnsrch/busnSearch.htm?"
    pg = nil
    begin
      pg = br.get(s_url+params)
      params="command=navPN"
      scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While traversing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while pg.at("a[text()='Next']")
  rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end 
end

#save_metadata("OFFSET",0)
range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)

offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end

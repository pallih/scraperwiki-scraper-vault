require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.sos.nh.gov/corporate/soskb/"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
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
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
      Nokogiri::HTML(data).xpath(".//td[not(@width)]/table[@width='100%' and not(@align or @cellpadding or @cellspacing) and @border='0']/tr[position()>3]").each{|tr|
        td = tr.xpath("td")
        r = {
          "COMPANY_NAME" => text(td[0].xpath("font/a")),
          "COMPANY_NUMBER" => text(td[1].xpath("font/a")),
          "URL" => BASE_URL+attributes(td[0].xpath("font/a"),"href"),
          "TYPE" => text(td[2].xpath("center")),
          "STATUS" => text(td[3].xpath("center")),
          "CREATION_DT" => text(td[4].xpath("font")),
          "DOC" => Time.now
        }
        records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r["TYPE"]=="Trade Name" or r["STATUS"]=="Merged" or r["STATUS"]=="Reserved Name" or r["TYPE"]=="Foreign Corp Registered Name"
      }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()=' >> ']"),"href")
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Mac Safari'
      b.read_timeout = 1200
      b.max_history=0
      b.retry_change_requests = true
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    index = get_metadata("INDEX",-50)
    s_url = BASE_URL + "SearchResults.asp?"
    params = "FormName=CorpNameSearch&Words=Starting&SearchStr=#{srch}&SearchType=Search&"
    position = (index>=0)? "Pos=Next+50+%3E%3E&TopRec=#{index}" : ""
    reference = (index>=0)? s_url + params + "Pos=Next+50+%3E%3E&TopRec=#{index-50}" : s_url 

    pg = br.post(s_url+params+position,"",{"Referer"=>reference})
    begin
      scrape(pg.body,"list")
      pg.form_with(:name => "CorpNameSearch") do |f|
        f["Pos"] = "Next 50 >>"
        pg =  f.submit
      end 
      index = index+50
      if not pg.at("input[@value='Next 50 >>']")
        save_metadata("INDEX",-50)
        break
      end
    save_metadata("INDEX",index)
    rescue Exception => e
      puts "ERROR: While processing #{s_url} :: #{e.inspect} :: #{e.backtrace}"
      sleep(2)
      retry
    end while(true)
    save_metadata("OFFSET",srch.next)
  rescue Exception => e
    puts "Error: Sequence initialization failed for character #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end


save_metadata("OFFSET",0)

range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  action(srch) unless index < offset
  save_metadata("OFFSET",index.next)
end


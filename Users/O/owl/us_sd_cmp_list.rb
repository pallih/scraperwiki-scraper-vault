require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sdsos.gov/business/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
        retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
        puts "ERROR: #{e.inspect} during save_metadata(#{key}) :: #{e.backtrace}"
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
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records =[]
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_MainContent_rdgResults_ctl00']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER" => text(td[0].xpath("a")),
        "COMPANY_NAME" => text(td[1].xpath("span")),
        "STATE" => text(td[2].xpath(".")),
        "TYPE" => text(td[3].xpath(".")),
        "STATUS" => text(td[4].xpath(".")),
        "URL" => BASE_URL + attributes(td[0].xpath("a"),"href"),
        "DOC"=>Time.now
      }
      records << r unless r['TYPE']=='LLC Reserved Name' or r['TYPE'] == "Foreign Registered Name"
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name='swdata',verbose=2) unless records.length == 0
  end
end

def action(from,to)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      #b.read_timeout = 120
      b.max_history=0
     }
    params = {
    "ctl00$RadScriptManager1"=>"ctl00$MainContent$ctl00$MainContent$RadAjaxPanel1Panel|ctl00$MainContent$btnSearch","__EVENTTARGET"=>"ctl00$MainContent$btnSearch",
      "ctl00$MainContent$txtZip"=>"     -    ","ctl00$MainContent$txtDateFrom"=>from.to_s,
        "ctl00$MainContent$txtDateFrom$dateInput"=>"#{from.to_s}-00-00-00","ctl00$MainContent$txtDateTo"=>to.to_s,"ctl00$MainContent$txtDateTo$dateInput"=>"#{to.to_s}-00-00-00","__ASYNCPOST"=>"false"
    }
    pg = br.get(BASE_URL+"search.aspx")
  
    pg.form_with(:name=>"aspnetForm") do|f|
      params.each{|k,v| f[k]=v}
      pg = f.submit 
    end
    size = text(pg.at("div[@class='rgWrap rgInfoPart']/strong[3]"))
    params["ctl00_MainContent_rdgResults_ctl00_ctl03_ctl02_ChangePageSizeTextBox_text"],params["ctl00$MainContent$rdgResults$ctl00$ctl03$ctl02$ChangePageSizeTextBox"]=size,size
    params["ctl00$MainContent$rdgResults$ctl00$ctl03$ctl02$ChangePageSizeLinkButton"]="Change"
    pg.form_with(:name=>"aspnetForm") do|f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    scrape(pg.body,"list")
  end
end

t = Time.new()
action(Date.new(t.year,t.month,1),Date.civil(t.year,t.month,-1))

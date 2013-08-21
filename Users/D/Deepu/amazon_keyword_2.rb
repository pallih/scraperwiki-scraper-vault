# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "https://www.corporations.state.pa.us/"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
}

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,num,url)
  if action == "details"
      records = {"SCRAPED_NUMBER" => num,"URL"=>nil,"DOC"=>Time.now.to_s}
      Nokogiri::HTML(data).xpath("//table[@width='98%']/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /Entity Number/
            key = "COMPANY_NUMBER"
          when /Status/
            key = "STATUS"
          when /Entity Creation Date/
            key = "CREATION_DT"
          when /State of Business/
            key = "STATE"
          when /Registered Office Address/
            key = "ADDR1"
          when /Principal Place of Business/
            key = "ADDR3"
          when /Dissolve Date/
            key = "DISSOLVE_DT"
          when /Mailing Address/
            key = "ADDR2"
          else
            key = nil
        end
        value = text(td[1])
        if value == "Current Name"
          key = "COMPANY_NAME"
          value = text(td[0])
        end
        records[key] = value unless key.nil? 
      }
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["SCRAPED_NUMBER"],records,table_name="CMPINFO",verbose=0) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
      return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0
  end
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action(num)
  begin
    params =
    s_url = BASE_URL+"corp/soskb/searchbycharternumber.asp?"
    @pg = @br.post(s_url,{'CharterNumber'=>num,'SearchBtn'=>'Search'},{'Referer'=>BASE_URL+"corp/soskb/searchbycharternumber.asp?dtm=592210648148148",'Cookie'=>'ASPSESSIONIDSCDBADBS=NMFMGIMBMJBCMBPCOLOOKFEC'})
    re = scrape(@pg.body,"details",num,s_url)
    save_metadata("INDEX",num.next) unless re.nil? 
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
    sleep(30)
    retry if e.inspect =~ /Timeout|TIME|HTTP/
    
  end
end

#s_url = BASE_URL+"corp/soskb/SearchResults.asp"
#captcha_field="03AHJ_VusFYwP0KBtLp3OaHYc_LenSxAL5ltYpiB4crMj6uf1_bvStZ8CgWHnRALftaktoqrBZKmgg2kmLwJ7V0BRaUY0Um9mvC0H1Lw4Nr43i-quYUmjmQnBlHAt_nwJ6yOjl-Gwp0ghz"
#params = {"VerifyPage"=>"","Words"=>"Starting","OnlyActive"=>"","SearchStr"=>"Google","recaptcha_challenge_field"=>captcha_field,"recaptcha_response_field"=>"MCOcts+evayyeaucw"}
#headers = {"referer"=>"https://www.corporations.state.pa.us/corp/soskb/SearchResults.asp"}
#@pg=@br.post(s_url,params,headers)

#iframe = @pg.at("iframe")
#puts iframe unless iframe.nil?
save_metadata("INDEX",5610)
strt = get_metadata("INDEX",1000000).to_i
endd = strt+5000
(strt..endd).each{|num|
  action(num) #if iframe.nil?
}

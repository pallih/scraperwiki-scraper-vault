# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.njportal.com"

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
  doc = Nokogiri::HTML(data).xpath(".//table[@id='mainContent_wzMain_searchResult_gvCopiesSearchResult']/tr[position()>2 and position()<last()]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[1].xpath(".")),
      "COMPANY_NUMBER" => text(td[2].xpath(".")),
      "TYPE" => text(td[4].xpath(".")),
      "FILING_DT" => text(td[5].xpath(".")),
      "DOC" => Time.now
    }
    records << r unless r['COMPANY_NUMBER'].nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def init()
  @br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  s_url = BASE_URL+"/DOR/businessrecords/EntityDocs/BusinessCopies.aspx"
  @pg = @br.get(s_url)

  params = {"__EVENTTARGET"=>"ctl00$mainContent$wzMain$searchInput$rblSearchType$0","ctl00$mainContent$wzMain$searchInput$rblSearchType"=>"BusinessName"}
  @pg.form_with(:id=>"form1") do|f|
    params.each{|k,v| f[k]=v}
    @pg = f.submit
  end
end

def action(srch)
  begin
    init() if @pg.nil? 
    pg_tmp = nil
    params = {"ctl00$mainContent$wzMain$searchInput$rblSearchType"=>"BusinessName","ctl00$mainContent$wzMain$searchInput$txtBusinessName"=>srch,
      "ctl00$mainContent$wzMain$StartNavigationTemplateContainerID$btnContinue"=>"Continue →"}
    @pg.form_with(:id=>"form1") do|f|
      params.each{|k,v| f[k]=v }
      pg_tmp = f.submit
    end
    exit if pg_tmp.body =~ /Application Offine/

    ttl = scrape(pg_tmp.body)
    pg_no = 2
    begin
      nex = text(Nokogiri::HTML(pg_tmp.body).xpath(".//table[not(@id)]/tr/td[font/span]/following-sibling::td[1]/font/a"))
      break if nex.nil? or nex.empty? 
      params = {"__EVENTTARGET"=>"ctl00$mainContent$wzMain$searchResult$gvCopiesSearchResult","__EVENTARGUMENT"=>"Page$#{pg_no}"}
      pg_no = pg_no+1 
      pg_tmp.form_with(:id=>"form1") do |f|
        params.each{|k,v| f[k] = v }
        pg_tmp = f.submit
      end
      ttl = ttl + scrape(pg_tmp.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while true
    return srch,ttl
  end
end

#ScraperWiki.sqliteexecute("CREATE TABLE `swdata` (`DOC` timestamp, `FILING_DT` text, `TYPE` text, `COMPANY_NAME` text, `COMPANY_NUMBER` text);")
#ScraperWiki.commit()

#save_metadata("TRIAL","R>>RO>>ROC>>ROCK>>ROCKL")
#save_metadata("TRIAL","U>>UN>>UNI>>UNIT>>UNITE>>UNITED>>UNITEDW>>UNITEDWO>>UNITEDWOO")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A0'..'Z9').to_a
  offset = get_metadata("OFFSET",0)
  range.each_with_index{|srch,idx|
    next if idx < offset
    action(srch)
    save_metadata("OFFSET",idx.next)
  }
  save_metadata("TRIAL","A")
  delete_metadata("OFFSET")
  trial = "A"
  srch = "A"
end
begin
  prev,ret = action(srch.split(//).join('%'))
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 500
    srch = srch+'A'
    trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)
  else
    t_a = trial.split(">>")
    t_s = t_a.pop
    t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
    srch = (t_s == 'Z')? nil : t_s.next
    trial = (t_a << srch).join(">>")
  end
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)


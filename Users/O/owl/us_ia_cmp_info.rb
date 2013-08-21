require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sos.iowa.gov/"


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

def is_available(num)
    return ScraperWiki.sqliteexecute("select count(*) from swdata where scraped_number=?",[num])['data'][0][0]
end

def scrape(data)
  r={"DOC"=>Time.now}
  r["COMPANY_NUMBER"],r["COMPANY_NAME"],r["STATUS"]=text(Nokogiri::HTML(data).xpath(".//table[@class='results display'][1]/tr[not(@class)][2]/td"))
  r["TYPE"],r["INC_ST"],r["MODIFIED"]=text(Nokogiri::HTML(data).xpath(".//table[@class='results display'][1]/tr[not(@class)][4]/td"))
  r["EXP_DT"],r["EFFECTIVE_DT"],r["FILING_DT"]=text(Nokogiri::HTML(data).xpath(".//table[@class='results display'][1]/tr[not(@class)][6]/td"))
  ScraperWiki.save_sqlite(unique_key=['COMPANY_NUMBER'],r,table_name='swdata',verbose=2) unless r["COMPANY_NAME"].nil? or r["COMPANY_NAME"].empty? if r["TYPE"] =~ /legal/i
  return (r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty?)? nil : 0
end

def action(index)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.max_history=0
      b.read_timeout = 1200
    }
    s_url = BASE_URL+"search/business/search.aspx"
    params = {'busNo'=>index,'btnBusNo'=>'Search'}
    pg = br.get(s_url)
    pg.form_with(:name=>"frm2") do|f| 
      params.each{|k,v| f[k]=v}
      pg = f.submit 
    end
    re = scrape(pg.body)
    save_metadata("INDEX",index.next) unless re.nil? 
  end
end

#ScraperWiki.sqliteexecute("delete from swdata where type='' or type='Foreign fictitious' or type='Registered' or type='Reserved'")
#ScraperWiki.commit()
#save_metadata("INDEX",459278)
strt = get_metadata("INDEX",430469)
range = (strt..(strt + 500)).to_a
range.each{|index|
  action(index)
  sleep(5)
}

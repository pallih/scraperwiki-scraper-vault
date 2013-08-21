require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://egov.sos.state.or.us"

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
      str.text.collect{|st| tmp << st.text.strip }
      return tmp
    end
  rescue Exception => e
    puts [str.inner_html,e,e.inspect,e.backtrace].inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,url,num)
  if action == "details"
    records = {"DOC"=>Time.now,"SCRAPED_NUMBER"=>num,"URL" => url}
    tr = Nokogiri::HTML(data).xpath("html/body/form/table[2]/tr[position()>1]")
    td = tr.xpath("td")
    return nil if td.length < 3
    records["COMPANY_NUMBER"] = attributes(td[0].xpath("input[@name='p_regist_nbr']"),"value")
    records["TYPE"] = text(td[1])
    records["STATUS"] = text(td[2])
    records["COMPANY_NAME"] = text(Nokogiri::HTML(data).xpath("html/body/form/table[3]/tr/td[2]"))
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    return (records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty?) ? nil : 0 
  end
end

def scraped(params)
  return get_metadata(params,nil)
end

def action(num)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL + "/br/pkg_web_name_srch_inq.show_detl?p_be_rsn=#{num}&p_srce=BR_INQ&p_print=FALSE"
    pg = br.get(s_url)
    re = scrape(pg.body,"details",s_url,num)
    save_metadata("INDEX",num.next) unless re.nil? 
  rescue Exception => e
    puts "ERROR: While processing #{num} :: #{e.inspect} :: #{e.backtrace}"
  end
end

#save_metadata("INDEX",1532360)
strt = get_metadata("INDEX",1532360).to_i
endd = strt+1000

(strt..endd).each{|num|
  action(num)
}

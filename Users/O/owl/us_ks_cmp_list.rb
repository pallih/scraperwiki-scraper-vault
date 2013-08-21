# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.accesskansas.org/"

class String
  def join(str)
    return self+str
  end
end
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
  doc = Nokogiri::HTML(data).xpath(".//table[@width='90%']/tr[td]")

  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME"=>text(td[0].xpath(".")).join(""),
      "COMPANY_NUMBER"=>text(td[1].xpath(".")),
      "DOC"=>Time.now
    } 
    #puts r.inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def init
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
    s_url = BASE_URL+"bess/flow/main"
    @pg = br.get(s_url)
    params = [{"j_id9_SUBMIT"=>1,"processIds"=>"startSearchLink","startSearchLink"=>"startSearchLink"},{"J_id9_SUBMIT"=>1,"processIds"=>"byEntityNumberLink","byEntityNumberLink"=>"byEntityNumberLink"}]
    @pg.form_with(:name=>"j_id9") do|f|
      params[0].collect{|k,v| f[k]=v}
      @pg = f.submit
    end 
      @pg.form_with(:name=>"j_id9") do|f|
        params[1].collect{|k,v| f[k]=v}
        @pg = f.submit
      end 
  rescue Exception => e
   raise e
  end
end

def action(srch)
 begin
  init() if @pg.nil? 
  pg_tmp = nil
  params = {"searchFormForm:j_id13"=>"Search","searchFormForm:entityNumber"=>"%07d" % srch, "searchFormForm_SUBMIT"=>"1"}
  @pg.form_with(:name=>"searchFormForm") do |f|
    return nil if f.nil? 
    params.collect{|k,v| f[k]=v}
    pg_tmp = f.submit
  end
  return nil if pg_tmp.body =~ /Search by Name|An error has occurred while processing your request|failed search/i
  resp = scrape(pg_tmp.body)
  save_metadata("STRT",srch+1) if resp > 0 
 rescue Exception => e
    puts [srch,e.inspect,e.backtrace].inspect
 end
end

strt = get_metadata("START",7449440)

(strt..strt+12000).each{|srch|
  action(srch)
}
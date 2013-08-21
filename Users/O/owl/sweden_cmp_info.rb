# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://foretagsfakta.bolagsverket.se"
@br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
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
      return tmp.join("\n")
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
  doc = Nokogiri::HTML(data).xpath(".//div[@id='resultat-foretag']//ul/li/dl")
  doc.each{|dl|
    dd=dl.xpath("dd")
    r={
      "COMPANY_NAME"=>text(dd[0].xpath("a")),
      "COMPANY_NUMBER"=>text(dd[1].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length<=0
  return doc.length
end


def init()
s_url=BASE_URL+"/fpl-dft-ext-web/home.seam?actionMethod=home.xhtml:search.onNewSearch()&cid=34794"
@pg = @br.get(s_url)
end

def action(srch)
  begin
    init()
    ttl,params = 0,{'fp-sok'=>'fp-sok', 'fp-sok:sokterm'=>srch+'%%*', 'fp-sok:find'=>'Search'}
    @pg.form_with(:name=>'fp-sok') do|f|
      params.each{|k,v| f[k] = v }
      @pg = f.submit
    end
    begin
      return srch,ttl if @pg.nil? 
      len = scrape(@pg.body)
      ttl = ttl + len
      break if not @pg.at("a[@id='j_id238']")
      lnk = @pg.link_with(:id=>'j_id238')
      @pg = lnk.click unless lnk.nil? 
    end while(true) unless @pg.body =~ /The search gave no results|You need to update the page/
    return srch,ttl if @pg.body =~ /The search gave no results|You need to update the page/ 
    #ret= text(@pg.at("div[@id='resultat-foretag']/h2/span")).scan(/Results:(.*)of (.*)/)
    #puts ret.inspect
    return srch,ttl#(ret.nil? or ret.empty?)?  1 : ret[0][1].to_i
  end
end

save_metadata("wa",true)
begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 500
  begin
    prev,ret = action(srch)
    puts [prev,ret].inspect
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(2)
  end while(true)
end
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://foretagsfakta.bolagsverket.se"
@br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
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
      return tmp.join("\n")
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
  doc = Nokogiri::HTML(data).xpath(".//div[@id='resultat-foretag']//ul/li/dl")
  doc.each{|dl|
    dd=dl.xpath("dd")
    r={
      "COMPANY_NAME"=>text(dd[0].xpath("a")),
      "COMPANY_NUMBER"=>text(dd[1].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length<=0
  return doc.length
end


def init()
s_url=BASE_URL+"/fpl-dft-ext-web/home.seam?actionMethod=home.xhtml:search.onNewSearch()&cid=34794"
@pg = @br.get(s_url)
end

def action(srch)
  begin
    init()
    ttl,params = 0,{'fp-sok'=>'fp-sok', 'fp-sok:sokterm'=>srch+'%%*', 'fp-sok:find'=>'Search'}
    @pg.form_with(:name=>'fp-sok') do|f|
      params.each{|k,v| f[k] = v }
      @pg = f.submit
    end
    begin
      return srch,ttl if @pg.nil? 
      len = scrape(@pg.body)
      ttl = ttl + len
      break if not @pg.at("a[@id='j_id238']")
      lnk = @pg.link_with(:id=>'j_id238')
      @pg = lnk.click unless lnk.nil? 
    end while(true) unless @pg.body =~ /The search gave no results|You need to update the page/
    return srch,ttl if @pg.body =~ /The search gave no results|You need to update the page/ 
    #ret= text(@pg.at("div[@id='resultat-foretag']/h2/span")).scan(/Results:(.*)of (.*)/)
    #puts ret.inspect
    return srch,ttl#(ret.nil? or ret.empty?)?  1 : ret[0][1].to_i
  end
end

save_metadata("wa",true)
begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 500
  begin
    prev,ret = action(srch)
    puts [prev,ret].inspect
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(2)
  end while(true)
end

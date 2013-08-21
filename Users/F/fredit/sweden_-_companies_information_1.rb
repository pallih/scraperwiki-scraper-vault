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
  Nokogiri::HTML(data).xpath(".//div[@id='resultat-foretag']//ul/li/dl").each{|dl|
    dd=dl.xpath("dd")
    r={
      "COMPANY_NAME"=>text(dd[0].xpath("a")),
      "COMPANY_NUMBER"=>text(dd[1].xpath(".")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length<=0
  return records.length
end

def action(srch)
  begin
    params = {'fp-sok'=>'fp-sok', 'fp-sok:sokterm'=>srch+'%%*', 'fp-sok:find'=>'Search'}
    @pg.form_with(:name=>'fp-sok') do|f|
      params.each{|k,v| f[k] = v }
      @pg = f.submit
    end
    begin
      return if @pg.nil? 
      scrape(@pg.body)
      break if not @pg.at("a[@id='j_id196']")
      lnk = @pg.link_with(:id=>'j_id196')
      @pg = lnk.click unless lnk.nil? 
    rescue Exception =>e 
      puts "ERROR: While processing #{srch}-looping :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|TIME|HTTP/
        retry
      end
    end while(true) unless @pg.body =~ /The search gave no results|You need to update the page/
    return nil if @pg.body =~ /The search gave no results|You need to update the page/ 
    ret= text(@pg.at("div[@id='resultat-foretag']/h2/span")).scan(/Results:(.*)of (.*)/)
    return (ret.nil? or ret.empty?)?  1 : ret[0][1].to_i
  rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /Timeout|TIME|HTTP/
      retry
    end
  end
end

trial = get_metadata("TRIAL","A")
trial = "A" if trial.nil? or trial.empty? 
srch = trial.nil? or trial.empty? ? "A" : trial.split(">>").last #get_metadata("SRCH",'A')

s_url=BASE_URL+"/fpl-dft-ext-web/home.seam?actionMethod=home.xhtml:search.onNewSearch()&cid=34794"
@pg = @br.get(s_url)

begin
  ret = action(srch)
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
  save_metadata("TRIAL",trial)
end while(true)


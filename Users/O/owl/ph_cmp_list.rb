# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.business.gov.ph"

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
  doc = Nokogiri::HTML(data).xpath(".//*[@*='_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:data']//tbody/tr")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[0].xpath("span")),
      "ADDR"=>text(td[1].xpath("span")),
      "STATUS"=>text(td[2].xpath("span")),
      "SCOPE"=>text(td[3].xpath("span")),
      "DOC" => Time.now
    }
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    init() if @pg.nil? 
    params = {
      "ice.submit.partial"=>"false",
      "ice.event.target"=>"_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:j_id16",
      "ice.event.captured"=>"_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:j_id16",
      "ice.event.type"=>"onclick",
      "ice.event.alt"=>"false",
      "ice.event.ctrl"=>"false",
      "ice.event.shift"=>"false",
      "ice.event.meta"=>"false",
      "ice.event.x"=>"841",
      "ice.event.y"=>"381",
      "ice.event.left"=>"true",
      "ice.event.right"=>"false",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:j_id16"=>"Search",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm"=>"",
      "icefacesCssUpdates"=>"",
      "javax.faces.ViewState"=>"1",
      "javax.faces.RenderKitId"=>"",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:businessName"=>"#{srch}___",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:searchmode"=>"begins",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:j_id39"=>"50",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:dataScroll_1"=>"",
      "_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:_idcl"=>"",
      "ice.session"=>@sessionID,
      "ice.view"=>"1",
      "ice.focus"=>"",
      "rand"=>"0.005384820651808009"
    }
    s_url = BASE_URL+"/pbr-search/block/send-receive-updates"
    pg_tmp = @br.post(s_url,params)
    raise "retry" if pg_tmp.body =~ /expired/i
    ttl = scrape(pg_tmp.body)  
    begin
      nex = Nokogiri::HTML(pg_tmp.body).xpath(".//a[@id='_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:dataScroll_1next']")
      break if nex.nil? or nex.empty? 
      params["ice.event.target"]="_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:nextpage_1"
      params["ice.event.captured"]="_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:dataScroll_1next"
      params["_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:dataScroll_1"]="next"
      params["_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:_idcl"]="_pbr_search_portlet_WAR_pbrsearch_:PBRSearchForm:dataScroll_1next"
      pg_tmp = @br.post(s_url,params)
      ttl = ttl + scrape(pg_tmp.body)
    rescue Exception => e
      puts "ERROR: While looping #{srch} :: #{e.inspect} :: #{e.backtrace}"
      exit if e.inspect =~ /exit|refused|interrupt/i
    end while true
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect =~ /retry/
      @pg=nil
      retry
    end
  end
end

def init()
  @br = Mechanize.new {|b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
    #b.log = Logger.new(STDERR)
  } 
  s_url = BASE_URL + "/web/guest/search"
  @pg = @br.get(s_url)
  @sessionID = @pg.body.scan(/false,session: '(.*)',view/).flatten.first
end

trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A1'..'Z9').to_a
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
  prev,ret = action(srch)
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
  elsif ret == 1000
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


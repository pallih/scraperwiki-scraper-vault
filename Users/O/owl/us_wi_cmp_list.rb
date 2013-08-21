require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.wdfi.org/apps/CorpSearch/"


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
    end
end

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name =?",[name])
    ScraperWiki.commit()
  rescue Exception=>e
    puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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
  doc = Nokogiri::HTML(data).xpath(".//*[@id='results']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath(".")),
      "COMPANY_NAME"=>text(td[1].xpath("span[@class='name']")),
      "TYPE" => text(td[1].xpath("span[@class='typeDescription']")),
      "URL"=> BASE_URL+attributes(td[1].xpath("span[@class='name']/a"),"href"),
      "STATUS"=>text(td[3].xpath("span[@class='statusDescription']")),
      "DOC" => Time.now
     }
    records << r unless r['COMPANY_NUMBER'].nil?  or r['COMPANY_NUMBER'].empty? or r['TYPE'] =~ /name/i
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  begin
    init() if @pg.nil? 
    params = {"ctl00$cpContent$txtSearchString"=>srch,"ctl00$cpContent$btnSearch"=>"SearchRecords","ctl00$cpContent$rblNameSet"=>"Entities","ctl00$cpContent$rblIncludeActiveEntities"=>"Include","ctl00$cpContent$rblIncludeOldNames"=>"Exclude"}
    pg_tmp = nil
    @pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k]=v }
      pg_tmp = f.submit
    end
    len = Nokogiri::HTML(pg_tmp.body).xpath(".//table[@id='results']/tr[position()>1]").length
    if pg_tmp.body =~ /captcha/
      raise "captcha"
    end
    scrape(pg_tmp.body)
  rescue Exception => e
    puts [srch,e].inspect
    exit if e.inspect =~ /HTTPForbidden|captcha|exit|interrupt|refused/i
    #if e.inspect =~ /captcha/
    #  @pg = nil
    #  init()
    #  retry
    #end
  end
end

def init()
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
  b.set_proxy(ARGV[3],ARGV[4]) unless ARGV[3].nil? or ARGV[4].nil? 
}
 @pg = @br.get(BASE_URL+"Advanced.aspx")
end

#puts ScraperWiki.sqliteexecute("create index idx_doc on swdata(doc);")

range = ('A'..'ZZZ').to_a + (0..1000).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
  sleep(10)

end
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.wdfi.org/apps/CorpSearch/"


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
    end
end

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name =?",[name])
    ScraperWiki.commit()
  rescue Exception=>e
    puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip.gsub(/\u00A0/,'')
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip.gsub(/\u00A0/,'') }
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
  doc = Nokogiri::HTML(data).xpath(".//*[@id='results']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath(".")),
      "COMPANY_NAME"=>text(td[1].xpath("span[@class='name']")),
      "TYPE" => text(td[1].xpath("span[@class='typeDescription']")),
      "URL"=> BASE_URL+attributes(td[1].xpath("span[@class='name']/a"),"href"),
      "STATUS"=>text(td[3].xpath("span[@class='statusDescription']")),
      "DOC" => Time.now
     }
    records << r unless r['COMPANY_NUMBER'].nil?  or r['COMPANY_NUMBER'].empty? or r['TYPE'] =~ /name/i
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  begin
    init() if @pg.nil? 
    params = {"ctl00$cpContent$txtSearchString"=>srch,"ctl00$cpContent$btnSearch"=>"SearchRecords","ctl00$cpContent$rblNameSet"=>"Entities","ctl00$cpContent$rblIncludeActiveEntities"=>"Include","ctl00$cpContent$rblIncludeOldNames"=>"Exclude"}
    pg_tmp = nil
    @pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k]=v }
      pg_tmp = f.submit
    end
    len = Nokogiri::HTML(pg_tmp.body).xpath(".//table[@id='results']/tr[position()>1]").length
    if pg_tmp.body =~ /captcha/
      raise "captcha"
    end
    scrape(pg_tmp.body)
  rescue Exception => e
    puts [srch,e].inspect
    exit if e.inspect =~ /HTTPForbidden|captcha|exit|interrupt|refused/i
    #if e.inspect =~ /captcha/
    #  @pg = nil
    #  init()
    #  retry
    #end
  end
end

def init()
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true
  b.set_proxy(ARGV[3],ARGV[4]) unless ARGV[3].nil? or ARGV[4].nil? 
}
 @pg = @br.get(BASE_URL+"Advanced.aspx")
end

#puts ScraperWiki.sqliteexecute("create index idx_doc on swdata(doc);")

range = ('A'..'ZZZ').to_a + (0..1000).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
  sleep(10)

end

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.registroimprese.it"

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
  doc = Nokogiri::HTML(data).xpath(".//div[@id='content_content']/div[@class='occorrenza']")
  doc.each{|div|
    azione = attributes(div.xpath("form/input[@name='azione']"),"value")
    criptoCF=attributes(div.xpath("form/input[@name='criptoCF']"),"value")
    criptoC = attributes(div.xpath("form/input[@name='criptoC']"),"value")
    criptoR = attributes(div.xpath("form/input[@name='criptoR']"),"value")
    base = attributes(div.xpath("form/input[@name='base']"),"value")
    idApp = attributes(div.xpath("form/input[@name='idApp']"),"value")
    r = {
      "COMPANY_NAME"=>text(div.xpath("div[@class='occorrenza_titolo']/span/a/font/b")),
      "URL"=>"#{BASE_URL}/dama/comc/comc/EN/ricerca/openPopUpVetrina.jsp?#{BASE_URL}/dama/comc/navcom&azione=#{azione}&criptoCF=#{criptoCF}&criptoC=#{criptoC}&criptoR=#{criptoR}&base=#{base}&idApp=#{idApp}",
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r['COMPANY_NAME'].nil? or r['COMPANY_NAME'].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def init()
  begin
    @br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      #b.log = Logger.new(STDERR)
    }

    @pg = @br.get(BASE_URL + "/dama/comc/comc/EN/index.jsp?ricerca=perNome")
    @br.get("http://www.registroimprese.it/dama/comc/capImage.gpj")
  end
end

def action(srch)
  begin
    init() if @pg.nil? 
    params = { "ricerca"=>srch,"max"=>20 }
    @pg.form_with(:name=>"form1") do |f|
      params.each{|k,v| f[k]=v }
      @pg = f.submit
    end
    scrape(@pg.body)
  end
end

#save_metadata("OFFSET",3)
range = ('A00'..'Z99').to_a + ('A'..'ZZZZ').sort.to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset>=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

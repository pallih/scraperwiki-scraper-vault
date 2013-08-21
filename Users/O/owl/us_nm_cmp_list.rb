# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://efile.prc.newmexico.gov/Efile/corplookup/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  b.retry_change_requests = true  
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+|&nbsp;/,' ').strip
  end
end

class Array
  def strip
    self.collect{|a|a.strip}
  end
  def downcase
    self.collect{|a|a.downcase}
  end
end

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data)
  doc.xpath(".//table[@id='MainContent_gvCorps']/tr[contains(@class,'RowStyle')]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=>s_text(td[1].xpath("./text()")),
      "COMPANY_NAME"=>s_text(td[2].xpath("./text()")),
      "TYPE"=>s_text(td[3].xpath("./text()")),
      "STATUS"=>s_text(td[4].xpath("./text()")),
      #"LINK" => append_base(BASE_URL,attributes(td[5].xpath("./a"),"href")),
      "DOC"=>Time.now
    }
    records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
  }
  #puts records
  nex = attributes(doc.xpath(".//tr[@class='PagerStyle']/td/table/tr/td[span]/following-sibling::*[1][self::td]/a"),"href").split("'")[3]
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length,nex
end

def action(srch)
  begin
    pg = @br.get(BASE_URL+"Lookdn.aspx")
    tmp = JSON.generate({"ctl00$MainContent$txtName"=>srch,"ctl00$MainContent$btnSearch"=>"Search","ctl00$MainContent$drpSearchOptions"=>"S"})
    params = JSON.parse(get_metadata("form",tmp))

    begin
      pg.form_with(:id=>"formID") do |f|
        params.each{|k,v| f[k] = v}
        pg = f.submit
      end
      len,nex = scrape(pg.body)
      break if nex.nil? or nex.empty? or len < 10
      params = {'__EVENTTARGET'=>'ctl00$MainContent$gvCorps','__EVENTARGUMENT'=>nex}
      tmp = {}
      pg.form_with(:id=>"formID").fields.each{|f|
        tmp[f.name] = f.value
      }
      save_metadata("form",JSON.generate(tmp))
    end while(true)
    delete_metadata("form")  
  end
end

list = ('a'..'z').to_a + (0..9).to_a + ['_','%','#','@','*',' '].to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|l|
  action(l)
  lstart = lstart + 1 
  save_metadata("list",lstart)
}
delete_metadata("list")

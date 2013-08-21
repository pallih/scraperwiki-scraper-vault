# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://www.mca.gov.in/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//*[@id='list1']/tbody/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {
        "doc"=>Time.now.to_s,
        "company_name" => s_text(td[1].xpath("./text()")),
        "company_number" => s_text(td[2].xpath("./text()")),
        "gln" => s_text(td[3].xpath("./text()")),
        "status" => s_text(td[4].xpath("./text()"))
      }
      records << r.merge(rec)
    }
    return records
  end
end

def action(srch)
  pg = @br.get(BASE_URL+"DCAPortalWeb/dca/MyMCALogin.do?method=setDefaultProperty&mode=14")
  params = {'sessioncheck'=>'yes', 'crumbLabelKey'=>'screen.label.CINGLN', 'screenID'=>'screen.label.CINGLN', 'taskID'=>'9403','searchCriteria'=>'STRT', 'companyName'=>srch, 'method'=>'find', 'menuForm'=>'welcome'}
  begin
    pg.form_with(:name => "CompanyCINSRForm") do |f|
      params.each{|k,v| f[k] = v }
      f.radiobutton_with(:value => "1",:name => "search").check rescue nil
      pg =  f.submit
    end unless pg.nil? or pg.form_with(:name=>"CompanyCINSRForm").nil? 
    
    records = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records) unless records.empty? 
    if pg.nil? or pg.at("a[@id='nextlist1']").nil? 
      pg=nil
      break
    end
    params = {'sessioncheck'=>'yes', 'screenID'=>'Results', 'hidSaveMode_list1'=>'', 'stNextEnabled'=>'true', 'stPreviousEnabled'=>'false', 'taskID'=>'9403', 'queryValues'=>'', 'rowModified_list1'=>'', 'method'=>'next'}
  end while(true)
end

range =  ('00'..'99').to_a + ('AA'..'ZZZ').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end
#action("SAA")
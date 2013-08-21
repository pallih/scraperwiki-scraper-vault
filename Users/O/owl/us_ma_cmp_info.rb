# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://corp.sec.state.ma.us/corp/corpsearch/"

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end
class Array
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(data)
  records = []
  Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @border='1' and not(@bordercolor) and @cellpadding='4']/tr[position()>1]").each{|tr|
    td=tr.xpath("td")
    r={
      'COMPANY_NAME'=> s_text(td[0].xpath("font/a/text()")),
      'COMPANY_NUMBER'=> s_text(td[1].xpath("font/text()")),
      'ADDR'=> s_text(td[3].xpath("font/text()")),
      'URL'=>BASE_URL+attributes(td[0].xpath("font/a"),"href"),
      'DOC'=>Time.now
    }
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"CorpSearchInput.asp")
    params = {'SearchType'=>'E', 'EntityName'=>srch, 'EntitySearchMethod'=>'B', 'IndividualSearchMethod'=>'B', 'lstDisplay'=>'5000', 'FormCode'=>'0000160', 'FilingMethod'=>'I', 'ReadFromDB'=>'False', 'Refreshed'=>'True'}
    pginfo = eval(get_metadata("PGINFO",""))
    params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = pginfo unless pginfo.nil? or pginfo.empty? 
    begin
      f = pg.forms[0]
      begin
        params.each{|k,v| f[k] = v }
        f.action="CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed=" unless f.action=~ /entitylist/i
        pg = f.submit
      end unless f.nil? 
      scrape(pg.body)
      break if pg.body =~ /No Records Matched/
      nex = pg.at("input[@name='cmdNext']")
      if nex.nil? 
        break
      else
        val = nex.attr('onclick').to_s
        if val.nil? or val.empty? 
          break
        else
          params['iPageNum'],params['TotalPageCount'],params['TotalRecords'] = val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0]
          save_metadata("PGINFO",val.scan(/fGoto_Page\((.*),(.*),(.*)\)/)[0].to_s)
        end
      end
      sleep(2)
    end while(true)
    delete_metadata("PGINFO")
  end
end

#action("GOOG")
#exit
range =  (0..9).to_a + ('A'..'Z').sort.to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
      sleep(2)
end


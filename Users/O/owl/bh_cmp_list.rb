# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'
require 'date'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.moic.gov.bh/CReServices/inquiry/"

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
      return tmp.join(" ")
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
  doc = Nokogiri::HTML(data).xpath(".//table[@id='grdCR']/tr[position()>1 and position()<last()]")
  doc.each{|tr|
    td = tr.xpath("td")
    break unless td.length == 7
    r = {
      "COMPANY_NUMBER"=>text(td[0].xpath("a")),
      "COMPANY_NAME"=>text(td[1].xpath(".")),
      "COMPANY_NAME_L"=>text(td[2].xpath(".")),
      "TYPE"=>text(td[3].xpath(".")),
      "REG_DT"=>text(td[4].xpath(".")),
      "DUE_DT"=>text(td[5].xpath(".")),
      "STATUS"=>text(td[6].xpath(".")),
      "URL"=>BASE_URL+attributes(td[0].xpath("a"),"href"),
      "DOC"=>Time.now
    }
    #puts r.inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(dt)
  from = dt
  to = dt.next
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
    }
    s_url = BASE_URL+"CREnqiury.aspx"
    pg = br.get(s_url)
    params = {'__EVENTTARGET'=>'FindCRAdvanceSearch'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    params = {'__EVENTTARGET'=>'lnkShowMoreCRSearchOptions'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    params = {'__EVENTTARGET'=>'ddlToMonth','ddlToMonth'=>to.month}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    params = {'__EVENTTARGET'=>'ddlFromMonth','ddlFromMonth'=>from.month}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    ttl = 0
    frm = (Date.new(dt.year,dt.month,(get_metadata("DAY",dt.day))))
    frm.upto(Date.new(frm.year,frm.month,-1)).to_a.each{|dt_c|
    begin 
    pg_tmp = nil
    params = {
      'ddlFromDay'=>dt_c.day,'ddlFromMonth'=>dt_c.month,'ddlFromYear'=>dt_c.year,'ddlToDay'=>dt_c.next.day,'ddlToMonth'=>dt_c.next.month,'ddlTOYear'=>dt_c.next.year,
      'btnFindCr'=>'Submit'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg_tmp = f.submit
    end
    ttl = scrape(pg_tmp.body)
    begin
      nex = text(Nokogiri::HTML(pg.body).xpath(".//td/table[@border and not(@cellpadding)]/tr/td[span]/following-sibling::td[1]/a"))
      break if nex.nil? or nex.empty? 
      params = {"__EVENTTARGET"=>"grdCR","__EVENTARGUMENT"=>"Page$#{nex}"}
      pg_tmp.form_with(:name=>"Form1") do |f|
        params.each{|k,v| f[k]=v }
        pg_tmp = f.submit    
      end
      ttl = ttl + scrape(pg_tmp.body)
    rescue Exception=>e
      puts "ERROR: While looping #{dt} :: #{e.inspect} :: #{e.backtrace}"  
      retry
    end while(true)
    rescue Exception => e
      puts "ERROR: While processing #{dt_c} :: #{e.inspect} :: #{e.backtrace}"
      retry unless e.inspect =~ /internal/i
    end
    save_metadata("DAY",dt_c.next.day)
    }
  rescue Exception => e
    puts "ERROR: While processing #{dt} :: #{e.inspect} :: #{e.backtrace}"
    retry unless e.inspect =~ /internal/i
  end
  return ttl
end



#save_metadata("DAY",Date.new(1920,1,1).to_s)
#strt = Date.strptime(get_metadata("STRT",'01.01.2012'),'%d.%m.%Y')
#endd = Date.today
#(strt..endd).each{|dt|
#  dt_s = dt.strftime('%d.%m.%Y')
#  ret = action(dt)
#  #break if ret == "BLOCKED"
#  #save_metadata("STRT",dt.next.strftime('%d.%m.%Y'))
#}
#save_metadata("YEAR",1977)
#save_metadata("MONTH",1)
#save_metadata("DAY",1)
((get_metadata("YEAR",1976))..Date.today.year).each{|yr|
  (get_metadata("MONTH",1)..12).each{|mnth|
    action(Date.new(yr,mnth,1))
    save_metadata("MONTH",mnth.next)
    #puts Date.new(yr,mnth,1).inspect
  }
  delete_metadata("MONTH")
  save_metadata("YEAR",yr.next) unless yr.next > Time.now.year
  #action(Date.strptime(get_metadata("STRT",'1.1.2012'),"%d.%m.%Y"))
}

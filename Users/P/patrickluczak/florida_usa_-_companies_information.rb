# encoding: ASCII-8BIT
require 'open-uri'
require 'csv'
require 'date'

BASE_URL = "ftp://ftp.dos.state.fl.us/public/doc/cor/"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      return (ret.nil?)? default : ret
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
      str.children().collect{|st| tmp << st.text.strip}
      return tmp.join("\n").strip
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def action(filename)
  begin
  open(BASE_URL+filename) do |o|
    File.open(filename, "w") { |f| f << o.read }
  end unless File.exists?(filename)
  arr = IO.readlines(filename)
  records = []
  arr.each{|a|
    a_a = a.unpack("A12A192A01A15A42A42A28A02A10A02A42A42A28A02A10A02A08A14A01A08A02A04A01A08A04A01A08A04A01A08A42A01A42A28A02A05A04")
    r ={"DOC"=>Time.now,"COR_NUMBER"=>a_a[0],"COR_NAME"=>a_a[1],"COR_STATUS"=>a_a[2],"COR_FILING_TYPE"=>a_a[3],"COR_PRINC_ADD_1"=>a_a[4],"COR_PRINC_ADD_2"=>a_a[5],"COR_PRINC_CITY"=>a_a[6],"COR_PRINC_STATE"=>a_a[7],"BCOR_PRINC_ZIP"=>a_a[8],"COR_PRINC_COUNTRY"=>a_a[9],"COR_MAIL_ADD_1"=>a_a[10],"COR_MAIL_ADD_2"=>a_a[11],"COR_MAIL_CITY"=>a_a[12],"COR_MAIL_STATE"=>a_a[13],"COR_MAIL_ZIP"=>a_a[14],"COR_MAIL_COUNTRY"=>a_a[15],"COR_FILE_DATE"=>a_a[16],"COR_FEI_NUMBER"=>a_a[17],"MORE_THAN_SIX_OFF_FLAG"=>a_a[18],"LAST_TRX_DATE"=>a_a[19],"STATE_COUNTRY"=>a_a[20],"REPORT_YEAR_1"=>a_a[21],"HOUSE_FLAG_1"=>a_a[22],"REPORT_DATE_1"=>a_a[23],"REPORT_YEAR_2"=>a_a[24],"HOUSE_FLAG_2"=>a_a[25],"REPORT_DATE_2"=>a_a[26],"REPORT_YEAR_3"=>a_a[27],"HOUSE_FLAG_3"=>a_a[28],"REPORT_DATE_3"=>a_a[29],"RA_NAME"=>a_a[30],"RA_NAME_TYPE"=>a_a[31],"RA_ADD_1"=>a_a[32],"RA_CITY"=>a_a[33],"RA_STATE"=>a_a[34],"RA_ZIP5"=>a_a[35],"RA_ZIP4"=>a_a[36]}
   records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['COR_NUMBER'],records,table_name="CORP",verbose=2) unless records.length == 0
  rescue Exception => e
    puts [filename,e.inspect,e.backtrace].inspect
    return nil if e.inspect =~ /Failed to open file/i
    raise e
  end
  return records.length
end

save_metadata("STRT","2012-01-17")
strt = Date.parse(get_metadata("STRT",Date.today-20))

(strt..strt+10).each{|dt|
  resp = action(dt.strftime('%Y%m%d').to_s+"c.txt")
  save_metadata("STRT",dt.next.to_s) if not resp.nil? 
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.registreentreprises.gouv.qc.ca"


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

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    elsif str.children().length == 0
      return ""
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
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


def scrape(data,act)
  if act == "details"
    doc = Nokogiri::HTML(data)
    records={
      "COMPANY_NAME"=>text(doc.xpath(".//textarea[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl04_fsCons_txtNomEntrpr__cs']")),
      "COMPANY_NUMBER"=>attributes(doc.xpath(".//input[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl04_fsCons_txtNEQ__cs']"),"value"),
      "ADDR"=>text(doc.xpath(".//textarea[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl06_ctl00_AdresseCompleteConsultationAdresse__cs']")),
      "STATUS"=>text(doc.xpath(".//textarea[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl11_ctl01__cs']")),
      "INCORPORATION_DT"=>attributes(doc.xpath(".//input[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl11_ctl00__cs']"),"value"),
      "FINAL_DT"=>text(doc.xpath(".//textarea[@id='CPH_K1ZoneContenu1_Cadr_Section01_Section01_ctl11_ctl03__cs']")).gsub(/Aucune date de cessation n'est prévue./,""),
      "DOC"=>Time.now
    } unless doc.nil? 
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.nil? or records['COMPANY_NUMBER'].nil? or records['COMPANY_NUMBER'].empty? 
    return records['COMPANY_NUMBER']
  end
end
def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
      b.retry_change_requests = true
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE

    }
    params = {
      'IdCtrlPatientez'=>'CPH_K1ZoneContenu1_Cadr_IdSectionRechSimple_IdSectionRechSimple_KRBTRechSimple_btnRechercher',
      'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$K1Fieldset1$ChampRecherche$_cs'=>srch,
      'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$K1Fieldset1$InputACauseBugIExplorer'=>'',
      'ctl00$CPH_K1ZoneContenu1_Cadr$IdSectionRechSimple$IdSectionRechSimple$KRBTRechSimple$btnRechercher'=>'Rechercher'
    }
    s_url = BASE_URL + "/RQAnonymeGR/GR/GR03/GR03A2_19A_PIU_RechEnt_PC/PageRechSimple.aspx?T1.CodeService=S00436"
    pg = br.get(s_url)
    begin
      frm = pg.form_with(:id=>'form1')
      pg.form_with(:id=>'form1') do|f|
        params.each{|k,v| f[k] = v }
        pg = f.submit
      end unless frm.nil? 
      return nil if frm.nil? 
      return scrape(pg.body,"details")
    rescue Exception =>e 
      puts "ERROR: While processing #{srch}-looping :: #{e.inspect} :: #{e.backtrace}"
      if e.inspect =~ /Timeout|TIME|HTTP/
        retry
      end
    end
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end
#action(3367881145)

range = (get_metadata('STRT',3367867218).to_i..3369999999).to_a
range.each{|srch|
  resp = action(srch)
  save_metadata('STRT',srch.next) unless resp.nil? or resp.empty? 
}
  
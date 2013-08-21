# TODO
# DONE - fix weird sqlite error
# - meslek ve ogrenim istikrarli calismiyor, duzelecek
# - resimli ornek bir view
# - dogumyili ve yeri, parti, ili vs'ye gore bir harita yapilacak

require 'nokogiri'
require 'open-uri'
require 'mechanize'

# Retrieve page
agent = Mechanize.new
page = agent.get('http://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.liste')

i=0

page.links.each do |link|
  if link.href =~ /milletvekillerimiz_sd.bilgi?/

    # Retrieve vekil links
    vekil_page = agent.click(link) 
    
    # find parti and ozgecmis tag in html
    isim = vekil_page.search("div[@id='mv_isim']").inner_text
    ozgecmis = vekil_page.search("div[@id='ozgecmis_icerik']").inner_text.gsub(/\s{3,}/,'').strip
    partiHtml = "table[1] table[1] tr[" + (i+2).to_s() +"] td[3]"

    # assign difficult to handle strings separately
    if ozgecmis.length > 0
      #meslek = ozgecmis.split(';')[0].split('.').last.strip
      dogumtarihi = ozgecmis[isim.length..-1][1..-1].split("'")[0].strip
      dogumyeri = ozgecmis.gsub(isim,'').gsub(dogumtarihi,'').split("'")[1].split(' ')[1]
      
      # assign meslek, ogrenim
      meslekOgrenim = vekil_page.search("div[@id='ozgecmis_icerik']").inner_html.split('</p>')[1].split(/\s\s/)[3]
      if meslekOgrenim =~ /;/ 
        meslek = meslekOgrenim.split(';')[0]
        ogrenim = ozgecmis.split(';')[1].split(' bitirdi.')[0].split(' mezun oldu.')[0][0..-3].split("'")[0]
      elsif meslekOgrenim =~ /,/ 
        meslek = meslekOgrenim.split(',')[0]
        ogrenim = meslekOgrenim.split(',')[1].strip[0..-1]
      else
        meslek = ''
        ogrenim = ''
      end
    end
    puts ogrenim


    # Retrieve fields + Generate record
    data = { 
      'sicil_no' => link.href[-4,4], 
      'isim' => isim, 
      'il' => vekil_page.search("div[@id='mv_ili']").inner_text.split(" ")[0], # take "Adana" from "Adana Milletvekili"
      'gorev' => vekil_page.search("div[@id='mv_gorev']").inner_text,
      'parti' => page.search(partiHtml).inner_text,
      'ozgecmis' => ozgecmis,
      #'meslek' => meslek,
      #'ogrenim' => ogrenim,
      'dogumtarihi' => dogumtarihi,
      'dogumyeri' => dogumyeri
    }
    i+=2 # cycle i + 2 because of the html structure of the doc

    # Save to datastore
    ScraperWiki.save_sqlite unique_keys = ['sicil_no'], data = data
    #puts data
  end
end

###################################################################
# Forming URLs for views 
# img_url = "http://www.tbmm.gov.tr/mv_resim/" + sicil_no + ".jpg"
# vekil_url = "http://www.tbmm.gov.tr/develop/owa/milletvekillerimiz_sd.bilgi?p_donem=24&p_sicil=" + sicil_no
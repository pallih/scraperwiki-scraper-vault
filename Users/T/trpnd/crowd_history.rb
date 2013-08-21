# openssl required to avoid mechanize login error
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

# Browser Emulation
require 'mechanize'
login_uri = "http://www.realworld.jp/crowd/history/"
agent = Mechanize.new
agent.user_agent_alias = 'Windows IE 7'
agent.follow_meta_refresh = true
html = agent.get login_uri

agent.page.form_with(:action => "https://ssl.realworld.jp/auth/login?method=post"){|form|
  form.field_with(:name => 'rwsid').value = ''
  form.field_with(:name => 'pass' ).value = ''
  form.submit
}


require 'nokogiri'           
doc = Nokogiri::HTML html
doc.search('//table[@class="history list"]').each do |v|
  cells = v.search 'td'
  if cells.count == 8
    data = {
           id: cells[0].inner_html, #作業ID
       d_date: cells[1].inner_html, #作業日時
      f_point: cells[2].inner_html, #ポイント
       a_date: cells[3].inner_html, #付与日時
         name: cells[4].inner_html, #作業名
      a_point: cells[5].inner_html, #獲得pt
       status: cells[6].inner_html, #判定状況
         memo: cells[7].inner_html  #備考
    }
    #puts data.to_json
    #Saving to the ScraperWiki datastore
    ScraperWiki::save_sqlite(['id'], data)         
 end
end

#import scraperwiki           
#html = scraperwiki.scrape("http://www.realworld.jp/crowd/history/")
#print html

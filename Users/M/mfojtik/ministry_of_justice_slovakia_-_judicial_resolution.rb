require 'rubygems'
require 'mechanize'
require 'nokogiri'

BASE_URL = 'http://www.justice.gov.sk/Stranky/Sudne-rozhodnutia/Sudne-rozhodnutia.aspx'

agent = Mechanize.new do |config|
  config.user_agent_alias = 'Mac Safari'
end

puts "[*] Connecting to #{BASE_URL}"
agent.get(BASE_URL) do |page|
  p = Nokogiri::HTML(page.body)
  page_count = p.css("td select").select do |s|
    s[:name] == "ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager"
  end.first.css("option").size/10
  1.upto(page_count) do |page_num|
    puts "[#{page_num}/#{page_count}] Requesting list of resolutions"
    list = page.form_with( :name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = "ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager"
      f['ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager'] = page_num
      f['ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVCountOnPage'] = 100
    end.submit
    list = Nokogiri::HTML(list.body)
    counter = 0
    items = {}
    list.css('.mainText .sprava div table.GridTable tr td a').each do |resolution_page_link|
      counter += 1
      puts "[#{page_num}/#{counter}] #{resolution_page_link[:href]}"
      agent.get(resolution_page_link[:href]) do |resolution_page|
        resolution = Nokogiri::HTML(resolution_page.body)
        resolution_id = resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpIdSudnehoSpisu').text
        item = { resolution_id => {
          :court => resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpSud').text.strip,
          :judge => resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpSudcaKtoryVydalRozhodnutie').text.strip,
          :references => resolution.css('div.hodnota span').text.strip
        }}
        puts "[#{page_num}/#{counter}] Requesting details"
        details = resolution_page.form_with( :name => 'aspnetForm') do |f|
          f['__CALLBACKID'] = 'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$rozhodnutieSudneViewer'
          f['__CALLBACKPARAM'] = 'c0:page='
        end.submit
        details_html = Nokogiri::HTML(details.body.split('setViewSize(602,930);').last.split("','id':").first)
        item[resolution_id].merge!({ :text => details_html.text })
        ScraperWiki.save([resolution_id],  item)
      end
    end
  end

end
require 'rubygems'
require 'mechanize'
require 'nokogiri'

BASE_URL = 'http://www.justice.gov.sk/Stranky/Sudne-rozhodnutia/Sudne-rozhodnutia.aspx'

agent = Mechanize.new do |config|
  config.user_agent_alias = 'Mac Safari'
end

puts "[*] Connecting to #{BASE_URL}"
agent.get(BASE_URL) do |page|
  p = Nokogiri::HTML(page.body)
  page_count = p.css("td select").select do |s|
    s[:name] == "ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager"
  end.first.css("option").size/10
  1.upto(page_count) do |page_num|
    puts "[#{page_num}/#{page_count}] Requesting list of resolutions"
    list = page.form_with( :name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = "ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager"
      f['ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVPager'] = page_num
      f['ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanieCiv$ctl13$ctl00$cmbAGVCountOnPage'] = 100
    end.submit
    list = Nokogiri::HTML(list.body)
    counter = 0
    items = {}
    list.css('.mainText .sprava div table.GridTable tr td a').each do |resolution_page_link|
      counter += 1
      puts "[#{page_num}/#{counter}] #{resolution_page_link[:href]}"
      agent.get(resolution_page_link[:href]) do |resolution_page|
        resolution = Nokogiri::HTML(resolution_page.body)
        resolution_id = resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpIdSudnehoSpisu').text
        item = { resolution_id => {
          :court => resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpSud').text.strip,
          :judge => resolution.css('div.hodnota a#ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_ctl01_hpSudcaKtoryVydalRozhodnutie').text.strip,
          :references => resolution.css('div.hodnota span').text.strip
        }}
        puts "[#{page_num}/#{counter}] Requesting details"
        details = resolution_page.form_with( :name => 'aspnetForm') do |f|
          f['__CALLBACKID'] = 'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$rozhodnutieSudneViewer'
          f['__CALLBACKPARAM'] = 'c0:page='
        end.submit
        details_html = Nokogiri::HTML(details.body.split('setViewSize(602,930);').last.split("','id':").first)
        item[resolution_id].merge!({ :text => details_html.text })
        ScraperWiki.save([resolution_id],  item)
      end
    end
  end

end

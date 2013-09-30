require 'nokogiri'

# retrieve a page
base_url = 'http://webinfo.parl.gc.ca/MembersOfParliament/'
starting_url = base_url + 'MainMPsCompleteList.aspx?TimePeriod=Current&Language=E'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
rows = doc.search('#MasterPage_MasterPage_BodyContent_PageContent_Content_' + 
  'ListContent_ListContent_grdCompleteList tr').to_a

rows.shift
rows.each do |tr|
    cells = tr.css('td')
    name = cells[0].inner_text
    profile_url = base_url + cells[0].css('a').first['href']
    constituency = cells[1].inner_text
    province = cells[2].inner_text
    caucas = cells[3].inner_text

    profile_html = ScraperWiki.scrape(profile_url)
    profile_doc = Nokogiri::HTML(profile_html)

    email = profile_doc.css('#MasterPage_MasterPage_BodyContent_PageContent_' + 
      'Content_DetailsContent_DetailsContent__ctl0_hlEMail').inner_text
    
    headshot_url = base_url+ profile_doc.css('#MasterPage_MasterPage_BodyContent_PageContent_Content_' +
      'TombstoneContent_TombstoneContent_ucHeaderMP_imgPhoto').first['src']

    ScraperWiki.save(['name', 'email', 'profile_url', 'headshot_url', 'constituency', 'province', 'caucas'], 
        {'name' => name, 'profile_url' => profile_url, 'headshot_url' => headshot_url, 
         'constituency' => constituency, 'province' => province, 'caucas' => caucas, 'email' => email })

end

require 'nokogiri'

# retrieve a page
base_url = 'http://webinfo.parl.gc.ca/MembersOfParliament/'
starting_url = base_url + 'MainMPsCompleteList.aspx?TimePeriod=Current&Language=E'
html = ScraperWiki.scrape(starting_url)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
rows = doc.search('#MasterPage_MasterPage_BodyContent_PageContent_Content_' + 
  'ListContent_ListContent_grdCompleteList tr').to_a

rows.shift
rows.each do |tr|
    cells = tr.css('td')
    name = cells[0].inner_text
    profile_url = base_url + cells[0].css('a').first['href']
    constituency = cells[1].inner_text
    province = cells[2].inner_text
    caucas = cells[3].inner_text

    profile_html = ScraperWiki.scrape(profile_url)
    profile_doc = Nokogiri::HTML(profile_html)

    email = profile_doc.css('#MasterPage_MasterPage_BodyContent_PageContent_' + 
      'Content_DetailsContent_DetailsContent__ctl0_hlEMail').inner_text
    
    headshot_url = base_url+ profile_doc.css('#MasterPage_MasterPage_BodyContent_PageContent_Content_' +
      'TombstoneContent_TombstoneContent_ucHeaderMP_imgPhoto').first['src']

    ScraperWiki.save(['name', 'email', 'profile_url', 'headshot_url', 'constituency', 'province', 'caucas'], 
        {'name' => name, 'profile_url' => profile_url, 'headshot_url' => headshot_url, 
         'constituency' => constituency, 'province' => province, 'caucas' => caucas, 'email' => email })

end


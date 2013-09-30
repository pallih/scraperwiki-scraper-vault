require 'mechanize'

agent = Mechanize.new

url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/AllPublicNotices.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOTAL.ENQ'
page = agent.get(url)

base_info_url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/PublicNoticeDetails.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOT.VIW&ApplicationId='
comment_url = 'http://www.marrickville.nsw.gov.au/planning/da/comment.html'

(page/'//*[@id="ctl00_Content_cusApplicationResultsGrid_pnlCustomisationGrid"]').search('table').each do |t|
  closing_date = t.search('td')[7].inner_text
  on_notice_to = (closing_date == 'N/A' ? nil : Date.strptime(closing_date, '%d/%m/%Y'))

  record = {
    'council_reference' => t.search('td')[1].inner_text,
    'description'       => t.search('td')[3].inner_text,
    'on_notice_to'      => on_notice_to,
    'address'           => t.search('td')[5].inner_text,
    'info_url'          => base_info_url + t.search('td')[1].inner_text,
    'comment_url'       => comment_url,
    'date_scraped'      => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
endrequire 'mechanize'

agent = Mechanize.new

url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/AllPublicNotices.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOTAL.ENQ'
page = agent.get(url)

base_info_url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/PublicNoticeDetails.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOT.VIW&ApplicationId='
comment_url = 'http://www.marrickville.nsw.gov.au/planning/da/comment.html'

(page/'//*[@id="ctl00_Content_cusApplicationResultsGrid_pnlCustomisationGrid"]').search('table').each do |t|
  closing_date = t.search('td')[7].inner_text
  on_notice_to = (closing_date == 'N/A' ? nil : Date.strptime(closing_date, '%d/%m/%Y'))

  record = {
    'council_reference' => t.search('td')[1].inner_text,
    'description'       => t.search('td')[3].inner_text,
    'on_notice_to'      => on_notice_to,
    'address'           => t.search('td')[5].inner_text,
    'info_url'          => base_info_url + t.search('td')[1].inner_text,
    'comment_url'       => comment_url,
    'date_scraped'      => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
endrequire 'mechanize'

agent = Mechanize.new

url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/AllPublicNotices.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOTAL.ENQ'
page = agent.get(url)

base_info_url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/PublicNoticeDetails.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOT.VIW&ApplicationId='
comment_url = 'http://www.marrickville.nsw.gov.au/planning/da/comment.html'

(page/'//*[@id="ctl00_Content_cusApplicationResultsGrid_pnlCustomisationGrid"]').search('table').each do |t|
  closing_date = t.search('td')[7].inner_text
  on_notice_to = (closing_date == 'N/A' ? nil : Date.strptime(closing_date, '%d/%m/%Y'))

  record = {
    'council_reference' => t.search('td')[1].inner_text,
    'description'       => t.search('td')[3].inner_text,
    'on_notice_to'      => on_notice_to,
    'address'           => t.search('td')[5].inner_text,
    'info_url'          => base_info_url + t.search('td')[1].inner_text,
    'comment_url'       => comment_url,
    'date_scraped'      => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
endrequire 'mechanize'

agent = Mechanize.new

url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/AllPublicNotices.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOTAL.ENQ'
page = agent.get(url)

base_info_url = 'http://www.marrickville.nsw.gov.au/ePropertyProd/P1/PublicNotices/PublicNoticeDetails.aspx?r=$P1.WEBGUEST&f=$P1.ESB.PUBNOT.VIW&ApplicationId='
comment_url = 'http://www.marrickville.nsw.gov.au/planning/da/comment.html'

(page/'//*[@id="ctl00_Content_cusApplicationResultsGrid_pnlCustomisationGrid"]').search('table').each do |t|
  closing_date = t.search('td')[7].inner_text
  on_notice_to = (closing_date == 'N/A' ? nil : Date.strptime(closing_date, '%d/%m/%Y'))

  record = {
    'council_reference' => t.search('td')[1].inner_text,
    'description'       => t.search('td')[3].inner_text,
    'on_notice_to'      => on_notice_to,
    'address'           => t.search('td')[5].inner_text,
    'info_url'          => base_info_url + t.search('td')[1].inner_text,
    'comment_url'       => comment_url,
    'date_scraped'      => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
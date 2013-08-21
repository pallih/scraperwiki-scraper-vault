require 'mechanize'

url = 'http://www.mornpen.vic.gov.au/Page/Page.asp?Page_Id=700'
agent = Mechanize.new

page = agent.get(url)

page.search('.h2').each do |a|
  record = {
    'council_reference' => a.inner_text.split('-')[0].strip,
    'description'       => a.parent.parent.search('.p')[1].inner_html.split('<br>')[0],
    'address'           => a.inner_text.split('-')[1..-1].join.strip,
    'info_url'          => url,
    'comment_url'       => url,
    'date_scraped'      => Date.today.to_s
  }
  
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
     puts "Skipping already saved record " + record['council_reference']
  end
end
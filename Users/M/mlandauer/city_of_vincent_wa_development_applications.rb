require 'mechanize'

url = "http://www.vincent.wa.gov.au/Your_Community/Whats_On/Community_Consultation/Planning_Applications"

agent = Mechanize.new
page = agent.get(url)
page.search('.listitemrow').each do |i|
  info_url = i.at('a')['href']
  record = {
    'council_reference' => info_url.split('/')[-2..-1].join('/'),
    'address' => i.at('.address br').next_sibling.inner_text.gsub("\r\n", "").squeeze(' ').strip,
    'description' => i.at('.listitemtext > strong').next_sibling.inner_text,
    'info_url' => info_url,
    'comment_url' => 'mailto:mail@vincent.wa.gov.au',
    'date_scraped' => Date.today.to_s,
    'on_notice_to' => i.at('.listitemtext > b').next_sibling.inner_text.split('/').reverse.join('-')
  }
  if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

require 'mechanize'

url = "http://www.vincent.wa.gov.au/Your_Community/Whats_On/Community_Consultation/Planning_Applications"

agent = Mechanize.new
page = agent.get(url)
page.search('.listitemrow').each do |i|
  info_url = i.at('a')['href']
  record = {
    'council_reference' => info_url.split('/')[-2..-1].join('/'),
    'address' => i.at('.address br').next_sibling.inner_text.gsub("\r\n", "").squeeze(' ').strip,
    'description' => i.at('.listitemtext > strong').next_sibling.inner_text,
    'info_url' => info_url,
    'comment_url' => 'mailto:mail@vincent.wa.gov.au',
    'date_scraped' => Date.today.to_s,
    'on_notice_to' => i.at('.listitemtext > b').next_sibling.inner_text.split('/').reverse.join('-')
  }
  if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end


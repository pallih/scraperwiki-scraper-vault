require 'mechanize'

agent = Mechanize.new { |a| 
  a.user_agent_alias = 'Mac Safari'
}

# Their pagination is broken, so we need to keep track of which ones we've seen
# to prevent a time-out.
pages = {}

(1470.0/30).to_i.times do |i|
  page = agent.get("http://statistics.allfacebook.com/pages/leaderboard/-/-/-/f/DESC/-/#{i*30}")
  doc = Nokogiri::HTML(page.body)
  doc.search('table').first.search('tbody tr')[0..-2].each_with_index do |row,i|
    # puts [row.css('td')[1].css('a').first['href'].split("/")[3],row.css('td')[1].inner_text.strip, row.css('td')[2].inner_text.strip].join(', ')
    page_name = row.css('td')[1].css('a').first['href'].split("/")[3]
    next if pages[page_name]

    pages[page_name] = true
    ScraperWiki.save_sqlite(unique_keys=["page_name"], data={
      "page_name"=>page_name,
      "pretty_name"=>row.css('td')[1].inner_text.strip,
      "fan_count"=>row.css('td')[2].inner_text.strip.gsub(",","").to_i,
      "link"=>"http://facebook.com/#{page_name}"
    })           
  end
end
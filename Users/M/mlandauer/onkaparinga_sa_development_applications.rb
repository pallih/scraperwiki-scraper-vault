require 'mechanize'

domain = "http://www.onkaparingacity.com"
url = "http://www.onkaparingacity.com/onka/living_here/planning_development/applications_for_public_comment.jsp"

def clean(t)
  t.squeeze(' ').strip
end

def find_item_from(items, search_key)
  items.each do |item|
    if item =~ search_key
      return item.match(search_key)[1].gsub(/\u00A0 /,' ').strip
    end
  end
  return 'N/A'
end

agent = Mechanize.new
page = agent.get(url)
council_reference = nil
page.search('#body > p').each do |p|
  info = p.inner_html.split("<br>")
  if info.length == 1
    # We're guessing that this paragraph just contains the council_reference. Save it for later.
    council_reference = find_item_from(info, /Application Number:.* ([^<]+)/)
  end
  if info.length > 2
    address = find_item_from(info, /Subject Land:(.*)/)
    if address.include?('(')
      address = address.split('(').first + address.split(')').last
    end

    # Sometimes there is an empty <p> after a DA
    urls = p.next_element.search('a').empty? ? p.next_element.next_element.search('a') : p.next_element.search('a')

    record = {
      'council_reference' => council_reference,
      'address' => clean(address) + ", SA",
      'description' => find_item_from(info, /Nature of Development:(.*)/),
      'info_url' => domain + urls[0]['href'],
      'comment_url' => domain + urls[1]['href'],
      'date_scraped' => Date.today.to_s,
      'on_notice_from' => info[4].split(' ').last.split('/').reverse.join('-'),
      'on_notice_to' => info[5].split(' ').last.split('/').reverse.join('-'),
    }
    if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end
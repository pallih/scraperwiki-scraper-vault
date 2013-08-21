require 'mechanize'
require 'faraday'
require 'json'

# @todo use http://app06.ottawa.ca/en/city_hall/statisticsdata/opendata/info/elected_officials/
# Both Curl and the Python scraper inexplicably download the Ottawa page as binary:
# https://scraperwiki.com/scrapers/ottawa_city_councilors/

BASE_URL = 'http://ottawa.ca'
COUNCIL_URL = BASE_URL + 'node/267267/index.html'
MAYOR_URL = BASE_URL + '/en/city-council'

ScraperWiki::sqliteexecute('DELETE FROM swdata')

def get_value(doc, key)
  node = doc.at_xpath(%(//*[contains(text(), "#{key}")]))
  if node
    p = node.ancestors('p')
    value = p.children.map{|child|
      if child.name == 'br'
        "\n"
      else
        child.text.strip
      end
    }.join.sub(key, '').strip
    value = p.first.next_element.text.strip if value.empty? 
    value
  end
end

def scrape(url, data)
  agent = Mechanize.new
  agent.user_agent_alias = 'Mac Safari'

  doc = agent.get(url).parser

  if data[:elected_office] == 'Councillor'
    doc.at_css('h2').text[/(\d+) (.+)/]
    data[:district_id] = $1
    data[:district_name] = $2
  end

  offices = {}
  tel = get_value(doc, /\([0-9][0-9][0-9]\)/)

  tel.enum_for(:scan, /([\d-]+) \(([^)]+)\)/).each do
    type = Regexp.last_match(2)
    offices[type] = {
      type: type,
      tel: Regexp.last_match(1),
    }
  end

  if offices.empty? 
    offices['office'] = {
      type: 'office',
      tel: tel,
    }
  end

  offices['office'].merge!({
    postal: get_value(doc, 'Address').sub(', Ontario', ' ON '),
    fax: get_value(doc, 'Fax'),
  })

  data.merge!({
    source_url: url,
    url: url,
    name: doc.at_css('h1').text.sub(/Mayor|Councillor/, '').strip,
    email: get_value(doc, 'E-mail'),
    offices: offices.values.to_json,
  })

  data[:extra] = {}
  twitter = doc.at_xpath(%(//*[contains(@href, "twitter.com")])) # can be a or area tag
  if twitter and not twitter[:href]['ottawacity'] # don't assign city Twitter account
    data[:extra][:twitter] = twitter[:href]
  end
  facebook = doc.at_xpath(%(//*[contains(@href, "facebook.com")])) # can be a or area tag
  if facebook
    data[:extra][:facebook] = facebook[:href]
  end
  data[:extra] = data[:extra].to_json

  data[:photo_url] = BASE_URL + doc.at_css('#rightHandLinks img,.graphicLeft img')[:src]
  data[:personal_url] = get_value(doc, 'Website')
  unless data[:personal_url].nil? or data[:personal_url][%r{^https?://}]
    data[:personal_url] = "http://#{data[:personal_url]}"
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end

scrape MAYOR_URL, {
  elected_office: 'Mayor',
  district_name: 'Ottawa',
  district_id: 0,
  boundary_url: '/boundaries/census-subdivisions/3506008/',
}

agent = Mechanize.new
agent.user_agent_alias = 'Mac Safari'

agent.get(COUNCIL_URL).parser.css('h3').each do |h3|
  scrape Faraday.head("#{BASE_URL}#{h3.at_css('a')[:href]}").env[:response_headers][:location], {
    elected_office: 'Councillor',
  }
end

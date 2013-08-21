require 'nokogiri'

starting_url = 'http://services.parliament.uk/bills/'

def get_data url, tries=0
  #ScraperWiki.scrape seems to choke periodically, this retries it a few times before
  #giving up on it
 
  max = 5

  begin
    return ScraperWiki.scrape(url)
  rescue
    if tries >= max
      raise "error retrieving data"
    else
      tries += 1
      sleep(rand(8))
      return get_data(url, tries)
    end
  end
end

def get_last_stage url
  html = get_data(url)
  doc = Nokogiri::HTML(html)
  stage = "??"
  stage_image = doc.xpath('//div[@class="last-event"]/ul/li/img')
  unless stage_image.empty? 
    image_name = stage_image.attr("src").value
    image_name = image_name[image_name.rindex("/")..image_name.length]
    case image_name
      when /1R/
        stage = "1st Reading"
      when /2R/
        stage = "2nd Reading"
      when /3R/
        stage = "3rd Reading"
      when /Comm/
        stage = "Committee"
      when /Rep/
        stage = "Report"
      when /PP/
        stage = "Ping Pong"
      else
        stage = "?"
    end
  end
  stage
end

html = get_data(starting_url)

doc = Nokogiri::HTML(html)
doc.xpath('//tr[starts-with(@class, "tr")]').each do |td|
    house = td.xpath('td[@class="middle"][1]/img/@title').inner_html
    url = td.xpath('td[@class="bill-item-description"]/a/@href').to_s
    title = td.xpath('td[@class="bill-item-description"]/a').inner_html
    date = td.xpath('td[@class="middle"][2]').inner_html
    if house == "Royal Assent"
      house = "n/a"
      stage = "Royal Assent"
    elsif house == "Ping Pong"
      house = "n/a"
      stage = "Ping Pong"
    else
      stage = get_last_stage("http://services.parliament.uk/" + url)
    end
    record = {'title' => title, 'house' => house, 'stage' => stage, 'url' => "http://services.parliament.uk" + url, 'date' => date}
    ScraperWiki.save(['title'], record)
end

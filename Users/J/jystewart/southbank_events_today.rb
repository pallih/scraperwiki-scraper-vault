# Blank Ruby

require 'open-uri'
require 'nokogiri'

time = Time.now
base_url = "http://ticketing.southbankcentre.co.uk/find/all?start[value][year]=#{time.year}&start[value][month]=#{time.month}&start[value][day]=#{time.day}&end[value][year]=#{time.year}&end[value][month]=#{time.month}&end[value][day]=#{time.day}"

html = ScraperWiki.scrape(base_url)
doc = Nokogiri::HTML(html)

page_count = doc.search('.pager-item').last.text.to_i

event_list = {}

page_count.times do |page|
  url = base_url + "&page=#{page}"
  this_html = ScraperWiki.scrape(url)
  this_doc = Nokogiri::HTML(this_html)

  events = this_doc.search('#listings>li')
  one_day_events = events.select { |e| e.search('.date-display-single').count == 1 }

  one_day_events.each do |event|
    info = {
      :date => time.strftime("%Y-%m-%d"),
      :uri => "http://ticketing.southbankcentre.co.uk/" + event.at('.event-title a')['href'],
      :title => event.at('.event-title').text,
      :venue => event.at('.event-venue').text,
      :description => event.at('.event-copy').text,
      :tags => event.search('.event-tags a').collect { |a| a.text }.uniq,
      :is_free => event.search('.event-tags a').collect { |a| a.text }.include?('Free')
    }
    begin
      ScraperWiki.save([:uri], info)
    rescue SqliteException
      puts "#{info[:uri]} not unique"
    end
  end
  

end


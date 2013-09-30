require 'nokogiri'

scraped_queries = []
bad_responses = []
next_query = 0

while next_query < 2000 do
  url  = "https://scoutapp.com/accounts/new?subscription_id=#{next_query}"
  begin
    html = ScraperWiki.scrape(url)
  rescue HTTPClient::BadResponseError => e
    bad_responses << [url, e]
    next
  ensure
    # Do not hammer the server with too many requests
    sleepy = rand(20)/ 10.0
    puts "sleeping for #{sleepy}s (at #{next_query} query)"
    sleep(sleepy)

    # Make sure to increment the id for the next request
    next_query += 1
  end

  scraped_queryies << next_query
  data = []
  Nokogiri::HTML(html).css("#public_left div.bold").each do |div|
    description = div.text.
      gsub(/\s\s+/m, ' ').
      sub(/Your Plan: /, '').
      sub(/\s?Have a coupon\?/, '').
      strip
    data << {
      'subscription_id' => next_query,
      'description'     => description,
      'name'            => (description =~ /(\w+) \(/ && $1).to_s.strip,
      'conditions'      => (description =~ /\(([^)]+)/ && $1).to_s.strip,
      'url'             => url
    }
  end
  #                       unique keys               , key value data
  ScraperWiki.save_sqlite(["subscription_id", "url"], data)
  puts "Saving page #{scraped_queries.size}"
end

puts "#{bad_responses.size} bad"
puts "#{scraped_queries.size} good"
puts "#{bad_responses.size + scraped_queries.size} total"
require 'nokogiri'

scraped_queries = []
bad_responses = []
next_query = 0

while next_query < 2000 do
  url  = "https://scoutapp.com/accounts/new?subscription_id=#{next_query}"
  begin
    html = ScraperWiki.scrape(url)
  rescue HTTPClient::BadResponseError => e
    bad_responses << [url, e]
    next
  ensure
    # Do not hammer the server with too many requests
    sleepy = rand(20)/ 10.0
    puts "sleeping for #{sleepy}s (at #{next_query} query)"
    sleep(sleepy)

    # Make sure to increment the id for the next request
    next_query += 1
  end

  scraped_queryies << next_query
  data = []
  Nokogiri::HTML(html).css("#public_left div.bold").each do |div|
    description = div.text.
      gsub(/\s\s+/m, ' ').
      sub(/Your Plan: /, '').
      sub(/\s?Have a coupon\?/, '').
      strip
    data << {
      'subscription_id' => next_query,
      'description'     => description,
      'name'            => (description =~ /(\w+) \(/ && $1).to_s.strip,
      'conditions'      => (description =~ /\(([^)]+)/ && $1).to_s.strip,
      'url'             => url
    }
  end
  #                       unique keys               , key value data
  ScraperWiki.save_sqlite(["subscription_id", "url"], data)
  puts "Saving page #{scraped_queries.size}"
end

puts "#{bad_responses.size} bad"
puts "#{scraped_queries.size} good"
puts "#{bad_responses.size + scraped_queries.size} total"

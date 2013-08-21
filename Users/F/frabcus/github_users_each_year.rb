#!/usr/bin/ruby

# Scrapes Github's search results to count the number of signed up
# users they have each month since they started in January 2008.

#<div id="code_search_results"> 
#  <div class="header"> 
#      <div class="title">

require 'nokogiri'
require 'uri'
require 'net/http'
require 'net/https'
    
def get_for_date(year, month)
  query = "created:[%4d-%02d-01T00:00:00.000Z TO %4d-%02d-01T00:00:00.000Z]"
  url = "https://github.com/search?type=Users&q=%s"

  next_year = year
  next_month = month + 1
  if next_month > 12
      next_month = 1
      next_year = year + 1
  end
  display_date = format("%4d-%02d", year, month)

  # already done?
  if ScraperWiki.get_var(display_date) == 1
    puts display_date + " already done"
    return
  end

  specific_query = format(query, year, month, next_year, next_month)
  specific_url = format(url, URI.escape(specific_query))
  # puts specific_url

  u  = URI.parse(specific_url)
  http = Net::HTTP.new(u.host, u.port)
  http.use_ssl = (u.scheme == 'https')
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE # stop annoying warning
  request = Net::HTTP::Get.new(u.request_uri)
  content = http.request(request).body
  
  doc = Nokogiri::HTML(content)
  doc.search('#code_search_results .header .title').each do |t|
    inner = t.inner_html
    m = /Users \((\d+)\)/.match(inner)
    raise Exception, "Failed to match number of users in: " + inner unless m
    c = m[1].to_i

    total = ScraperWiki.sqliteexecute("select sum(new_users) from swdata where `when` <= ?", [ display_date ])["data"][0][0]

    ScraperWiki.save_sqlite(unique_keys=['when'], data={
      'when' => display_date, 'new_users' => c, 'total_users' => total
    })

    puts display_date + "," + c.to_s + "," + total.to_s

    ScraperWiki.save_var(display_date, 1)
  end
end

def do_it
  now_month = Date.today.mon
  now_year = Date.today.year
  puts "now year " + now_year.to_s + " month " + now_month.to_s
  puts "month, new github users, total github users"
  (2008..now_year).each do |year|
    (1..12).each do |month|
      if now_month == month and now_year == year
        # don't even try to do this month, as figures not ready
        return
      end
      get_for_date(year, month)
      $stdout.flush
    end
  end
end

do_it



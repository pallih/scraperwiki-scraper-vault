# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'
require 'time'


require "net/http"
require "uri"

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end



def parse(n)
  url_text = "http://www.london2012.com/games/sport-competition-schedules/olympic-sport-competition-schedule.php?start=#{n}&Search_x=45&Search_y=17"

  url = URI.parse(url_text)
  p url
  req = Net::HTTP::Get.new(url_text)
  # Gets 403 if user agent is not specified
  req.add_field("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9")

  puts "Fetching #{url_text}"

  res = Net::HTTP.new(url.host, url.port).start do |http|
    http.request(req)
  end

  doc = Nokogiri::HTML.parse(res.body)
  body= doc.css('.data tr')[1..-1]

  ary = []
  body.each do |b|
    # # Sample Data set
    # <tr class="">
    # <td rowspan="2" class="firstCell">28 July<br>15:00 - 18:45<br><img src="images/medals/medal2.png" alt="Medal event" title="Medal event" class="medal">
    # </td>
    # <td class="topCell">Archery</td>
    # <td class="topCell">Lord's Cricket Ground</td>
    # </tr>
    # <tr><td colspan="2" class="noBorder">Men's Team: quarter-finals, semi-finals, bronze medal match, gold medal match, victory ceremony</td></tr>
    # 
    # The first row has date, time , whether the event is related to medal or not, sports category, and venue name
    # The second row has some additional info

    r = unless b.attributes == {}
      rr = []
      b.css('td').children.each  {|a| 
        rr << a.text if a.class == Nokogiri::XML::Text
      }
      # Checking if medal related event
      img = if b.child.css('img').length > 0
        b.child.css('img')[0].attributes["title"].value
      else
        nil
      end
      rr.push img
      rr
    else
      # description
      b.css('td').children.map{|c| c.text }.reject{|a| a == ""}
      # b.text
    end
    ary << r
  end

  while ary.length > 0
    row, description = ary.shift(2)
    local_date, local_time, category, venue, medal =  row
    start_time, end_time = local_time.split(" - ")
    start_time_epoch = Time.parse("#{local_date} #{start_time}:00 +0100").to_i
    end_time_epoch   = Time.parse("#{local_date} #{end_time}:00 +0100").to_i
    description.each do |d|
      data = {:local_date => local_date, :local_time => local_time, :start_time_epoch => start_time_epoch, :end_time_epoch => end_time_epoch, :category => category, :venue => venue, :medal => medal, :description => d}
      p data
      ScraperWiki::save_sqlite(unique_keys=[:local_date, :local_time, :category, :description], data=data)
    end
    n+=1
    p n
    p row
  end
end


num = 1
page_num = 20
last_num = 641
# last_num = 100

results=[]
while num <= last_num
  p num
  parse(num)
  num+=page_num
end

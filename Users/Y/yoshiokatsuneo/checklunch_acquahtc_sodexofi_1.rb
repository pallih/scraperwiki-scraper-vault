#!/usr/bin/ruby

require 'open-uri'
require 'nokogiri'
require 'pp'

body = open('http://www.sodexo.fi/pinta').read
html = Nokogiri.parse(body)

week2weekno = {
  "Maanantai" => 0,
  "Tiistai" => 1,
  "Keskiviikko" => 2,
  "Torstai" => 3,
  "Perjantai" => 4
};

@week_begin = nil

html.search("//div[@class='list-date']/b").each{|node|
  node.text.scan(/^Viikko\s*(\d+)/){
    week = $1.to_i
    @week_begin = Date.commercial(2013, week, 1);
    print "week=#{week}, week_begin=#{@week_begin}\n";
  }
  print "date=#{node.text}\n"
}
html.search("//div[@class='food-list-wrapper']/table/tbody/tr").each{|node_tr|
  print "node_tr:#{node_tr}\n\n"
  node_tr.search("th[@class='day']").each{|node_th|
    day_of_the_week=node_th.text
    weekno = week2weekno[day_of_the_week]
    @date = @week_begin + weekno
    print "day_of_the_week=#{day_of_the_week}, weekno=#{weekno}, date=#{@date}\n"
  }
  @food_title_en = nil
  @food_title_fi = nil
  @food_prices = nil
  @food_properties = ""
  node_tr.search("span[@class='food-title-en']").each{|node|
    @food_title_en = node.text
    print "Title:#{@food_title_en}\n"
  }
  node_tr.search("span[@class='food-title-fi']").each{|node|
    @food_title_fi = node.text
    print "Title:#{@food_title_fi}\n"
  }
  node_tr.search("td[@class='food-prices']").each{|node|
    node.text.scan(/(\d+),(\d+)/){
      @food_prices = "#{$1}.#{$2}"
      print "Price:#{@food_prices}\n"
    }
  }
  node_tr.search("td[@class='food-properties']").each{|node|
    @food_properties = node.text
    @food_properties.gsub!(/\s/,"")
  }
  if(! @food_title_en) then
    @food_title_en = @food_title_fi
  end
  if(@food_properties != "") then
    @food_title_en = "#{@food_title_en} (#{@food_properties})"
  end

  if (@food_title_en && @food_prices) then
    doc_item = {
      "date" => @date,
      "title" => @food_title_en,
      "price" => @food_prices,
    }
    ScraperWiki::save_sqlite(['date','title'], doc_item)
    print "date:#{@date}, title:#{@food_title_en}, price:#{@food_prices}\n"
  end
}




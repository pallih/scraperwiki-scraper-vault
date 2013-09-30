# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'


require "net/http"
require "uri"

def get_doc(url_text)
  url = URI.parse(url_text)
  p url
  req = Net::HTTP::Get.new(url_text)

  puts "Fetching #{url_text}"

  res = Net::HTTP.new(url.host, url.port).start do |http|
    http.request(req)
  end

  res.body
end

def run(year)
  base_url = "http://www.databaseolympics.com"
  year_url = "#{base_url}/games/gamesyear.htm?g=#{year[:page]}"
  
  sports =  Nokogiri::HTML.parse(get_doc(year_url)).css('.bio a')[1..-1].map{|a| [a.text, a.attributes["href"].value]}
  ary = []
  sports[0..-1].each do |s|
    name, url = s
    short = url.split('=').last
    p short
    # File.open("./data/#{short}.html", "w") do |f|
    #   p base_url + url
    #   f.write get_doc(base_url + url)
    # end
    doc = Nokogiri::HTML.parse get_doc(base_url + url)
    c = -1
    copy = ""
    tr = doc.css('.pt8 tr')[1..-1]
    tr.each do |a| 
      if a.child.text != ""
        copy = a.child.text
      else
        a.child.content = copy
      end
      a
    end
    r = tr.map do |t|
      # <tr class="cl2">
      # <td>Women's Team</td> 
      #   <td><a href="/players/playerpage.htm?ilkid=DodemSop01">Sophie Dodemont</a></td> 
      #   <td class="cen"><a href="/country/countryyear.htm?cty=FRA&amp;g=47">FRA</a></td> 
      #   <td class="rht"></td> 
      #   <td class="cen">BRONZE</td> 
      # </tr>
      event, _, person, _, country, _, time, _, medal, _ = t.children.map do |c|
        c.text
      end
      ary.push [year[:year], name, short, event, person, country, time, medal]
      person = person.each_char.map{|c|  c.unpack("C*").pack("U*")}.join unless person.valid_encoding? 
      event = event.each_char.map{|c|  c.unpack("C*").pack("U*")}.join unless event.valid_encoding?
      data = {:year => year[:year], :category => name, :short => short, :event => event, :person => person, :country => country, :time => time, :medal => medal}
      # p data
      begin
        ScraperWiki::save_sqlite(unique_keys=[:year, :category, :event, :person, :country, :time, :medal], data=data)
      rescue Exception => e
        p data
        raise "ERROR: #{e}"
      end
    end
  end  
end


years = [
  {
    :year => 2008,
    :page => 47
  },
  {
    :year => 2004,
    :page => 26
  },
  {
    :year => 2000,
    :page => 25
  }
]

years.each do |year|
  run year
end# -*- coding: utf-8 -*-
require 'rubygems'
require 'open-uri'
require 'nokogiri'


require "net/http"
require "uri"

def get_doc(url_text)
  url = URI.parse(url_text)
  p url
  req = Net::HTTP::Get.new(url_text)

  puts "Fetching #{url_text}"

  res = Net::HTTP.new(url.host, url.port).start do |http|
    http.request(req)
  end

  res.body
end

def run(year)
  base_url = "http://www.databaseolympics.com"
  year_url = "#{base_url}/games/gamesyear.htm?g=#{year[:page]}"
  
  sports =  Nokogiri::HTML.parse(get_doc(year_url)).css('.bio a')[1..-1].map{|a| [a.text, a.attributes["href"].value]}
  ary = []
  sports[0..-1].each do |s|
    name, url = s
    short = url.split('=').last
    p short
    # File.open("./data/#{short}.html", "w") do |f|
    #   p base_url + url
    #   f.write get_doc(base_url + url)
    # end
    doc = Nokogiri::HTML.parse get_doc(base_url + url)
    c = -1
    copy = ""
    tr = doc.css('.pt8 tr')[1..-1]
    tr.each do |a| 
      if a.child.text != ""
        copy = a.child.text
      else
        a.child.content = copy
      end
      a
    end
    r = tr.map do |t|
      # <tr class="cl2">
      # <td>Women's Team</td> 
      #   <td><a href="/players/playerpage.htm?ilkid=DodemSop01">Sophie Dodemont</a></td> 
      #   <td class="cen"><a href="/country/countryyear.htm?cty=FRA&amp;g=47">FRA</a></td> 
      #   <td class="rht"></td> 
      #   <td class="cen">BRONZE</td> 
      # </tr>
      event, _, person, _, country, _, time, _, medal, _ = t.children.map do |c|
        c.text
      end
      ary.push [year[:year], name, short, event, person, country, time, medal]
      person = person.each_char.map{|c|  c.unpack("C*").pack("U*")}.join unless person.valid_encoding? 
      event = event.each_char.map{|c|  c.unpack("C*").pack("U*")}.join unless event.valid_encoding?
      data = {:year => year[:year], :category => name, :short => short, :event => event, :person => person, :country => country, :time => time, :medal => medal}
      # p data
      begin
        ScraperWiki::save_sqlite(unique_keys=[:year, :category, :event, :person, :country, :time, :medal], data=data)
      rescue Exception => e
        p data
        raise "ERROR: #{e}"
      end
    end
  end  
end


years = [
  {
    :year => 2008,
    :page => 47
  },
  {
    :year => 2004,
    :page => 26
  },
  {
    :year => 2000,
    :page => 25
  }
]

years.each do |year|
  run year
end
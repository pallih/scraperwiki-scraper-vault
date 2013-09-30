# encoding: binary
require 'nokogiri'
require 'open-uri'

class MeetingScraper
  def initialize(session)
    html = open("http://stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/#{session}/?all=true").read
    @doc = Nokogiri::HTML.parse(html)
  end

  def each_meeting(&blk)
    @doc.css(".mainbody > h3 > a").each do |a| 
      yield Meeting.new("http://stortinget.no" + a['href']) 
    end
  end
end

class Meeting
  def initialize(url)
    @day = url[/\/(\d{6})\/$/, 1] or raise "unable to parse day from #{url.inspect}"
    @doc = Nokogiri::HTML.parse(open(url).read)
  end

  def each_issue(&blk)
    @doc.xpath(".//*[@class='mainbody']//a[contains(text(), 'Sak nr.')]").each do |a|
      yield Issue.new(@day, "http://stortinget.no" + a['href'])
    end
  end
end

class Issue
  def initialize(day, url)
    @day = day
    @url = url
    @doc = Nokogiri::HTML.parse(open(url).read)
  end

  def votes
    times = @doc.text.scan(/\(\s*Voteringsutskrift kl. (\d{2}.\d{2}.\d{2})\s*\)/).flatten
    times.map do |time|
      year, month, day = @day.scan(/.{2}/).map(&:to_i)
      year = "20#{year}"

      { 
        timestamp: Time.parse("#{year}-#{month}-#{day} #{time.gsub('.', ':')}"),
        url: @url
      }
    end
  end
end


MeetingScraper.new("2009-2010").each_meeting do |meeting|
  meeting.each_issue do |issue|
    votes = issue.votes || next
    ScraperWiki.save_sqlite(["timestamp"], votes)
  end
end# encoding: binary
require 'nokogiri'
require 'open-uri'

class MeetingScraper
  def initialize(session)
    html = open("http://stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Referater/Stortinget/#{session}/?all=true").read
    @doc = Nokogiri::HTML.parse(html)
  end

  def each_meeting(&blk)
    @doc.css(".mainbody > h3 > a").each do |a| 
      yield Meeting.new("http://stortinget.no" + a['href']) 
    end
  end
end

class Meeting
  def initialize(url)
    @day = url[/\/(\d{6})\/$/, 1] or raise "unable to parse day from #{url.inspect}"
    @doc = Nokogiri::HTML.parse(open(url).read)
  end

  def each_issue(&blk)
    @doc.xpath(".//*[@class='mainbody']//a[contains(text(), 'Sak nr.')]").each do |a|
      yield Issue.new(@day, "http://stortinget.no" + a['href'])
    end
  end
end

class Issue
  def initialize(day, url)
    @day = day
    @url = url
    @doc = Nokogiri::HTML.parse(open(url).read)
  end

  def votes
    times = @doc.text.scan(/\(\s*Voteringsutskrift kl. (\d{2}.\d{2}.\d{2})\s*\)/).flatten
    times.map do |time|
      year, month, day = @day.scan(/.{2}/).map(&:to_i)
      year = "20#{year}"

      { 
        timestamp: Time.parse("#{year}-#{month}-#{day} #{time.gsub('.', ':')}"),
        url: @url
      }
    end
  end
end


MeetingScraper.new("2009-2010").each_meeting do |meeting|
  meeting.each_issue do |issue|
    votes = issue.votes || next
    ScraperWiki.save_sqlite(["timestamp"], votes)
  end
end
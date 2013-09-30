require 'nokogiri'

module BCTransit
  BASE_URL = 'http://www.bctransit.com/'

  class Region
    attr_reader :abbreviation, :name, :routes

    def routes
      unless instance_variable_defined? :@routes
        @routes = BCTransit::Route.scrape self
      end

      @routes
    end

    def initialize(abbreviation, name)
      @abbreviation, @name = abbreviation, name
    end

    def to_s
      "#<#{self.class}: abbreviation: #{abbreviation}, name: #{name}"
    end

    def self.all
      html = ScraperWiki::scrape BASE_URL
      doc = Nokogiri::HTML html

      regions = doc.xpath('(//select[@name="jumplist"]/option[starts-with(@value, "/regions/")])[position()>2]').map do |o|
        Region.new o[:value][/^\/regions\/(\w+)\//, 1], o.content.strip
      end
    end
  end

  class Route
    attr_reader :name, :number

    def initialize(name, number)
      @name, @number = name, number
    end

    def to_s
      "#<#{self.class}: name: #{name}, number: #{number}>"
    end

    def self.scrape(region)
      html = ScraperWiki::scrape "#{BASE_URL}/regions/#{region.abbreviation}/"
      doc = Nokogiri::HTML html

      routes = doc.xpath('//div[@id="dvSchedule"]//p[@class="rightmenusubitem"]/a[contains(@href, "line=")]').map do |a|
        Route.new a.content.strip, a[:href][/line=(\d+)/, 1].to_i
      end
      
      routes.uniq { |route| route.number }
    end
  end

  class Schedule
    attr_reader :title

    def initialize(title)
      @title = title
    end

    def to_s
      "#<#{self.class}: title: #{title}>"
    end

    def self.scrape(region, route, day = 1, direction = 0)
      html = ScraperWiki::scrape "#{BASE_URL}/regions/#{region.abbreviation}/schedules/schedule.cfm?route=#{route.number}:#{direction}&day=#{day}"
      doc = Nokogiri::HTML html

      title = doc.xpath('//title')[0].content.strip
      times = doc.xpath('//td[@class="css-sched-times"]').map { |t| t.content[/\d+:\d+|-/] }.compact
      waypoints = doc.xpath('//td[@class="css-sched-waypoints"]').map { |w| w.content.strip }.uniq

      puts waypoints
    end
  end
end

region = BCTransit::Region.new 'vic', 'Victoria'
route = BCTransit::Route.new 'UVic', 1

BCTransit::Schedule.scrape region, route

# ScraperWiki::save_sqlite [:abbreviation, :name], regions, 'regions'
require 'nokogiri'

module BCTransit
  BASE_URL = 'http://www.bctransit.com/'

  class Region
    attr_reader :abbreviation, :name, :routes

    def routes
      unless instance_variable_defined? :@routes
        @routes = BCTransit::Route.scrape self
      end

      @routes
    end

    def initialize(abbreviation, name)
      @abbreviation, @name = abbreviation, name
    end

    def to_s
      "#<#{self.class}: abbreviation: #{abbreviation}, name: #{name}"
    end

    def self.all
      html = ScraperWiki::scrape BASE_URL
      doc = Nokogiri::HTML html

      regions = doc.xpath('(//select[@name="jumplist"]/option[starts-with(@value, "/regions/")])[position()>2]').map do |o|
        Region.new o[:value][/^\/regions\/(\w+)\//, 1], o.content.strip
      end
    end
  end

  class Route
    attr_reader :name, :number

    def initialize(name, number)
      @name, @number = name, number
    end

    def to_s
      "#<#{self.class}: name: #{name}, number: #{number}>"
    end

    def self.scrape(region)
      html = ScraperWiki::scrape "#{BASE_URL}/regions/#{region.abbreviation}/"
      doc = Nokogiri::HTML html

      routes = doc.xpath('//div[@id="dvSchedule"]//p[@class="rightmenusubitem"]/a[contains(@href, "line=")]').map do |a|
        Route.new a.content.strip, a[:href][/line=(\d+)/, 1].to_i
      end
      
      routes.uniq { |route| route.number }
    end
  end

  class Schedule
    attr_reader :title

    def initialize(title)
      @title = title
    end

    def to_s
      "#<#{self.class}: title: #{title}>"
    end

    def self.scrape(region, route, day = 1, direction = 0)
      html = ScraperWiki::scrape "#{BASE_URL}/regions/#{region.abbreviation}/schedules/schedule.cfm?route=#{route.number}:#{direction}&day=#{day}"
      doc = Nokogiri::HTML html

      title = doc.xpath('//title')[0].content.strip
      times = doc.xpath('//td[@class="css-sched-times"]').map { |t| t.content[/\d+:\d+|-/] }.compact
      waypoints = doc.xpath('//td[@class="css-sched-waypoints"]').map { |w| w.content.strip }.uniq

      puts waypoints
    end
  end
end

region = BCTransit::Region.new 'vic', 'Victoria'
route = BCTransit::Route.new 'UVic', 1

BCTransit::Schedule.scrape region, route

# ScraperWiki::save_sqlite [:abbreviation, :name], regions, 'regions'

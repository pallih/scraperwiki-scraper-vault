# Blank Ruby
require "uri"
require "nokogiri"

class AvrilScraper
  attr_reader :tour_dates
  
  def initialize
    @base_url = "http://www.avrillavigne.com/ca/events"
    @current_url = nil
    @doc = nil
    @tour_dates = []
  end

  def scrape(load_url = nil)
    load_url = load_url || @base_url
    @current_url = load_url
    puts load_url
    
    html = ScraperWiki.scrape(load_url)
    @doc = Nokogiri::HTML(html)
    for tr in @doc.search("tr.tid-14")
      cells = tr.search("td")
      tour_data = {
        "date" => cells[0].content.strip,
        "location" => cells[1].content.strip,
        "venue" => cells[2].content.strip,
        "ticket" => cells[3].content.strip
      }
      @tour_dates.push(tour_data)
      self.scrape(self.next_url) if (self.has_next? && sleep(3))
    end
    
  end
  
  def has_next?
    return !@doc.search("li.pager-next > a").count.zero?;
  end
  
  def next_url
    return self.has_next? && URI.parse(@current_url).merge(@doc.search("li.pager-next > a").attribute("href").to_s).to_s()
  end
end

avril_scraper = AvrilScraper.new
avril_scraper.scrape()

tour_dates = avril_scraper.tour_dates
ScraperWiki.save_sqlite(unique_keys=['date'], data=tour_dates) # Blank Ruby
require "uri"
require "nokogiri"

class AvrilScraper
  attr_reader :tour_dates
  
  def initialize
    @base_url = "http://www.avrillavigne.com/ca/events"
    @current_url = nil
    @doc = nil
    @tour_dates = []
  end

  def scrape(load_url = nil)
    load_url = load_url || @base_url
    @current_url = load_url
    puts load_url
    
    html = ScraperWiki.scrape(load_url)
    @doc = Nokogiri::HTML(html)
    for tr in @doc.search("tr.tid-14")
      cells = tr.search("td")
      tour_data = {
        "date" => cells[0].content.strip,
        "location" => cells[1].content.strip,
        "venue" => cells[2].content.strip,
        "ticket" => cells[3].content.strip
      }
      @tour_dates.push(tour_data)
      self.scrape(self.next_url) if (self.has_next? && sleep(3))
    end
    
  end
  
  def has_next?
    return !@doc.search("li.pager-next > a").count.zero?;
  end
  
  def next_url
    return self.has_next? && URI.parse(@current_url).merge(@doc.search("li.pager-next > a").attribute("href").to_s).to_s()
  end
end

avril_scraper = AvrilScraper.new
avril_scraper.scrape()

tour_dates = avril_scraper.tour_dates
ScraperWiki.save_sqlite(unique_keys=['date'], data=tour_dates) 
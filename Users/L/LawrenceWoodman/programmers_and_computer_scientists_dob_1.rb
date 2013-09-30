require 'date'
require 'nokogiri'

module StarSign
  # Dates from: http://my.horoscope.com/astrology/horoscope-sign-index.html
  STAR_SIGN_DATES = {
    'aries' =>       ['21 March 2011', '19 April 2011'],
    'taurus' =>      ['20 April 2011', '20 May 2011'],
    'gemini' =>      ['21 May 2011', '20 June 2011'],
    'cancer' =>      ['21 June 2011', '22 July 2011'],
    'leo' =>         ['23 July 2011', '22 August 2011'],
    'virgo' =>       ['23 August 2011', '22 September 2011'],
    'libra' =>       ['23 September 2011', '22 October 2011'],
    'scorpio' =>     ['23 October 2011', '21 November 2011'],
    'sagittarius' => ['22 November 2011', '21 December 2011'],
    'capricorn' =>   ['22 December 2011', '19 January 2012'],
    'aquarius' =>    ['20 January 2011', '18 February 2011'],
    'pisces' =>      ['19 February 2011', '20 March 2011']
  }

  def star_sign
    compare_date = Date.parse(self.to_s.sub(/^\d+-/, "2011-"))
    STAR_SIGN_DATES.each do |sign, dates|
      if compare_date >= Date.parse(dates[0]) &&
         compare_date <= Date.parse(dates[1])
        return sign
      end
    end
    # FIX:  This is ugly, but it has to be capricorn here.  The problem is due to the years
    return 'capricorn'
  end
end

class Date
  include StarSign
end

class DOBScraper
  attr_reader :population

  def initialize(name_database)
    ScraperWiki.attach(name_database) 
    @population = prize_winners = ScraperWiki.select(           
      "name, url from #{name_database}.swdata 
       order by name"
    )
    @last_saved_name = ScraperWiki.get_var('last_saved_name') 
  end

  def dump_dob(name, dob, star_sign)
    data = {
      'name' => name,
      'dob' => dob,
      'star_sign' => star_sign
    }

    ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
    ScraperWiki.save_var('last_saved_name', name)
    @last_saved_name = name
  end

  def extract_dob(person)
    name,url = person['name'], person['url']
    begin
      html = ScraperWiki.scrape(url)
    rescue StandardError => error
      puts "Error: #{error} (url: #{url})"
    end

    doc = Nokogiri::HTML(html)
    doc.css('table.infobox th').each do |th|
      if th.inner_text == "Born"
        born = th.parent.at('td').inner_text
        dob = born.scan(/.*?1[6789]\d\d/).first
        begin
          star_sign = Date.parse(dob).star_sign
          dump_dob(name, dob, star_sign)
        rescue StandardError => error
          puts "Error: #{error} dob: #{dob} (name: #{name} url: #{url})"
        end
        
      end
    end
  
  end

  def skip_person?(name)
    return false unless @last_saved_name
    name_index = @population.find_index{|winner| winner['name'] == name}
    last_saved_index = @population.find_index{|winner| winner['name'] == @last_saved_name}
    last_saved_index >= name_index && last_saved_index != @population.size-1
  end

  def scrape
    @population.each do |person|
      unless skip_person?(person['name'])
        extract_dob(person)
      end
    
    end
  end
end



dob_scraper = DOBScraper.new('programmers_and_computer_scientists_names_and_wiki')
dob_scraper.scrape

require 'date'
require 'nokogiri'

module StarSign
  # Dates from: http://my.horoscope.com/astrology/horoscope-sign-index.html
  STAR_SIGN_DATES = {
    'aries' =>       ['21 March 2011', '19 April 2011'],
    'taurus' =>      ['20 April 2011', '20 May 2011'],
    'gemini' =>      ['21 May 2011', '20 June 2011'],
    'cancer' =>      ['21 June 2011', '22 July 2011'],
    'leo' =>         ['23 July 2011', '22 August 2011'],
    'virgo' =>       ['23 August 2011', '22 September 2011'],
    'libra' =>       ['23 September 2011', '22 October 2011'],
    'scorpio' =>     ['23 October 2011', '21 November 2011'],
    'sagittarius' => ['22 November 2011', '21 December 2011'],
    'capricorn' =>   ['22 December 2011', '19 January 2012'],
    'aquarius' =>    ['20 January 2011', '18 February 2011'],
    'pisces' =>      ['19 February 2011', '20 March 2011']
  }

  def star_sign
    compare_date = Date.parse(self.to_s.sub(/^\d+-/, "2011-"))
    STAR_SIGN_DATES.each do |sign, dates|
      if compare_date >= Date.parse(dates[0]) &&
         compare_date <= Date.parse(dates[1])
        return sign
      end
    end
    # FIX:  This is ugly, but it has to be capricorn here.  The problem is due to the years
    return 'capricorn'
  end
end

class Date
  include StarSign
end

class DOBScraper
  attr_reader :population

  def initialize(name_database)
    ScraperWiki.attach(name_database) 
    @population = prize_winners = ScraperWiki.select(           
      "name, url from #{name_database}.swdata 
       order by name"
    )
    @last_saved_name = ScraperWiki.get_var('last_saved_name') 
  end

  def dump_dob(name, dob, star_sign)
    data = {
      'name' => name,
      'dob' => dob,
      'star_sign' => star_sign
    }

    ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
    ScraperWiki.save_var('last_saved_name', name)
    @last_saved_name = name
  end

  def extract_dob(person)
    name,url = person['name'], person['url']
    begin
      html = ScraperWiki.scrape(url)
    rescue StandardError => error
      puts "Error: #{error} (url: #{url})"
    end

    doc = Nokogiri::HTML(html)
    doc.css('table.infobox th').each do |th|
      if th.inner_text == "Born"
        born = th.parent.at('td').inner_text
        dob = born.scan(/.*?1[6789]\d\d/).first
        begin
          star_sign = Date.parse(dob).star_sign
          dump_dob(name, dob, star_sign)
        rescue StandardError => error
          puts "Error: #{error} dob: #{dob} (name: #{name} url: #{url})"
        end
        
      end
    end
  
  end

  def skip_person?(name)
    return false unless @last_saved_name
    name_index = @population.find_index{|winner| winner['name'] == name}
    last_saved_index = @population.find_index{|winner| winner['name'] == @last_saved_name}
    last_saved_index >= name_index && last_saved_index != @population.size-1
  end

  def scrape
    @population.each do |person|
      unless skip_person?(person['name'])
        extract_dob(person)
      end
    
    end
  end
end



dob_scraper = DOBScraper.new('programmers_and_computer_scientists_names_and_wiki')
dob_scraper.scrape


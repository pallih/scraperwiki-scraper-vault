require "fileutils"
require "open-uri"
##require "RMagick"

class Scraper

  def self.get_issues
    
    # the dates the issues to scrape 
    year = 2010
    month = 1
    start_day = 1
    end_day = 13

    # URIs of the issues 
    newspapers_issues_paths = Scraper.build_kiosko_issues(year, month, start_day, end_day)
    #newspapers_issues_paths = Scraper.build_newyork_times_issues(year, month, start_day, end_day)
    #newspapers_issues_paths = Scraper.build_elpais_issues(year, month, start_day, end_day)
    

    Scraper.scrape newspapers_issues_paths

    puts "Scraping is done"
  end
  
  # scrape method take the URIs of the issues and scrape them
  def self.scrape(newspapers_issues_paths)

    paths = newspapers_issues_paths

    paths.each do |path|
      begin
        open(path) do |source| 

          # pass to save method the path of the issue and the issue it self

          Scraper.save_kiosko_issues path, source
          #Scraper.save_newyork_times_issues path, source
          #Scraper.save_elpais_issues path, source
        end  
      rescue => e
        puts e.message + " => " + path
      end
    end
    
  end

  # formating the issues date for Kiosko.com in "YYYY/MM/DD" based on the specified year, month, start day, and end day
  def self.issues_dates(year, month, start_day, end_day)
    day = start_day
    days = []

    # assume that at least the number of issues is on
    number_of_issues = 1
    
    # calculate the number of issues
    number_of_issues = end_day - start_day + 1 unless end_day == 0 

    number_of_issues.times do 
      if day < 10 
        f_day = String("0" + day.to_s)
      else
        f_day = day.to_s
      end

      # formating the dates part of the images name 
      days << "#{year}/" + "0#{month}/" + f_day

      day += 1
    end
    days
  end

  # building the URIs of the issues based on the passed dates, this works with 2011, 2012 issues only until now
  def self.build_kiosko_issues(year, month, start_day, end_day)

    FileUtils.mkdir "pics/kiosko" unless File.directory? "pics/kiosko" 

    # sample of the countries and their newspapers form http://kiosko.net/
=begin
    es => Spain
    de => Germany
    fr => France
    it => Italy
    uk => United Kingdom
    us => USA
    . . . . . .
=end
    kiosko_newspapers = {"es" => ["elpais", "abc"], "de" => ["faz", "bild"], "fr" => ["lemonde", "lacroix"], "it" => ["corriere_della_sera", "ilmessaggero"], "uk" => ["the_times", ],"us" => ["wsj", "newyork_times", "usa_today"]}


    
    domain = "http://img.kiosko.net/"

    issues = Scraper.issues_dates year, month, start_day, end_day

    newspapers_issues = []
    newspapers_issues_paths = []

    # formating the images name by country name then the newspaper name with '.750.jpg' extention 
    kiosko_newspapers.each do |country, newspaper|
      newspaper.each do |_newspaper| 
        newspapers_issues << "/#{country}/#{_newspaper}.750.jpg" 
        FileUtils.mkdir "pics/kiosko/#{_newspaper}" unless File.directory? "pics/kiosko/#{_newspaper}" 
      end
    end

    # constracting the full URI of each image
    newspapers_issues.each do |newspaper|
      issues.each do |issue| 
        newspapers_issues_paths << domain + issue + newspaper
      end
    end

    newspapers_issues_paths
  end

  # save each image in it's place with name contains the date if the issue
  def self.save_kiosko_issues(path, source)

    newspaper_name = path.split('/').last

    open("pics/kiosko/#{path.split("/")[-1].split(".")[0]}/" + "#{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}-" + newspaper_name ,"wb") do |file|
      file.write(source.read())
      puts "done => #{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}-" + newspaper_name
    end

  end
  
  # building the URIs of the issues based on the passed dates
  def self.build_newyork_times_issues(year, month, start_day, end_day)

    FileUtils.mkdir "pics/newyork_times" unless File.directory? "pics/newyork_times" 

    domain = "http://www.nytimes.com/images/"
    
    newspapers_issues_paths = []

    issues = Scraper.issues_dates year, month, start_day, end_day

    issues.each do |issue| 
      newspapers_issues_paths << domain + issue + "/nytfrontpage/scan.jpg"
    end
    
    newspapers_issues_paths
  end

  # save each image in it's place with name contains the date if the issue
  def self.save_newyork_times_issues(path, source)

    open("pics/newyork_times/" + "#{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}" ,"wb") do |file|
      file.write(source.read())
      puts "done => #{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}"
    end
    
  end

  # building the URIs of the issues based on the passed dates
  def self.build_elpais_issues(year, month, start_day, end_day)

    # scrape a pdf from http://elpais.com/ and convert it to png 
    FileUtils.mkdir "pics/elpais" unless File.directory? "pics/elpais" 

    # fist issue available date is 2012/03/01
    issues = Scraper.issues_dates year, month, start_day, end_day

    newspapers_issues_paths = []

    issues.each do |d| 
      newspapers_issues_paths << "http://srv00.epimg.net/pdf/elpais/1aPagina/" + d[0..7] + "ep-" + d[0..3] + d[5..6] + d[8..11] + ".pdf"
    end

    newspapers_issues_paths
  end

  

end

FileUtils.mkdir "pics" unless File.directory? "pics"
Scraper.get_issues  require "fileutils"
require "open-uri"
##require "RMagick"

class Scraper

  def self.get_issues
    
    # the dates the issues to scrape 
    year = 2010
    month = 1
    start_day = 1
    end_day = 13

    # URIs of the issues 
    newspapers_issues_paths = Scraper.build_kiosko_issues(year, month, start_day, end_day)
    #newspapers_issues_paths = Scraper.build_newyork_times_issues(year, month, start_day, end_day)
    #newspapers_issues_paths = Scraper.build_elpais_issues(year, month, start_day, end_day)
    

    Scraper.scrape newspapers_issues_paths

    puts "Scraping is done"
  end
  
  # scrape method take the URIs of the issues and scrape them
  def self.scrape(newspapers_issues_paths)

    paths = newspapers_issues_paths

    paths.each do |path|
      begin
        open(path) do |source| 

          # pass to save method the path of the issue and the issue it self

          Scraper.save_kiosko_issues path, source
          #Scraper.save_newyork_times_issues path, source
          #Scraper.save_elpais_issues path, source
        end  
      rescue => e
        puts e.message + " => " + path
      end
    end
    
  end

  # formating the issues date for Kiosko.com in "YYYY/MM/DD" based on the specified year, month, start day, and end day
  def self.issues_dates(year, month, start_day, end_day)
    day = start_day
    days = []

    # assume that at least the number of issues is on
    number_of_issues = 1
    
    # calculate the number of issues
    number_of_issues = end_day - start_day + 1 unless end_day == 0 

    number_of_issues.times do 
      if day < 10 
        f_day = String("0" + day.to_s)
      else
        f_day = day.to_s
      end

      # formating the dates part of the images name 
      days << "#{year}/" + "0#{month}/" + f_day

      day += 1
    end
    days
  end

  # building the URIs of the issues based on the passed dates, this works with 2011, 2012 issues only until now
  def self.build_kiosko_issues(year, month, start_day, end_day)

    FileUtils.mkdir "pics/kiosko" unless File.directory? "pics/kiosko" 

    # sample of the countries and their newspapers form http://kiosko.net/
=begin
    es => Spain
    de => Germany
    fr => France
    it => Italy
    uk => United Kingdom
    us => USA
    . . . . . .
=end
    kiosko_newspapers = {"es" => ["elpais", "abc"], "de" => ["faz", "bild"], "fr" => ["lemonde", "lacroix"], "it" => ["corriere_della_sera", "ilmessaggero"], "uk" => ["the_times", ],"us" => ["wsj", "newyork_times", "usa_today"]}


    
    domain = "http://img.kiosko.net/"

    issues = Scraper.issues_dates year, month, start_day, end_day

    newspapers_issues = []
    newspapers_issues_paths = []

    # formating the images name by country name then the newspaper name with '.750.jpg' extention 
    kiosko_newspapers.each do |country, newspaper|
      newspaper.each do |_newspaper| 
        newspapers_issues << "/#{country}/#{_newspaper}.750.jpg" 
        FileUtils.mkdir "pics/kiosko/#{_newspaper}" unless File.directory? "pics/kiosko/#{_newspaper}" 
      end
    end

    # constracting the full URI of each image
    newspapers_issues.each do |newspaper|
      issues.each do |issue| 
        newspapers_issues_paths << domain + issue + newspaper
      end
    end

    newspapers_issues_paths
  end

  # save each image in it's place with name contains the date if the issue
  def self.save_kiosko_issues(path, source)

    newspaper_name = path.split('/').last

    open("pics/kiosko/#{path.split("/")[-1].split(".")[0]}/" + "#{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}-" + newspaper_name ,"wb") do |file|
      file.write(source.read())
      puts "done => #{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}-" + newspaper_name
    end

  end
  
  # building the URIs of the issues based on the passed dates
  def self.build_newyork_times_issues(year, month, start_day, end_day)

    FileUtils.mkdir "pics/newyork_times" unless File.directory? "pics/newyork_times" 

    domain = "http://www.nytimes.com/images/"
    
    newspapers_issues_paths = []

    issues = Scraper.issues_dates year, month, start_day, end_day

    issues.each do |issue| 
      newspapers_issues_paths << domain + issue + "/nytfrontpage/scan.jpg"
    end
    
    newspapers_issues_paths
  end

  # save each image in it's place with name contains the date if the issue
  def self.save_newyork_times_issues(path, source)

    open("pics/newyork_times/" + "#{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}" ,"wb") do |file|
      file.write(source.read())
      puts "done => #{path.split('/')[-3]}-#{path.split('/')[-4]}-#{path.split('/')[-5]}"
    end
    
  end

  # building the URIs of the issues based on the passed dates
  def self.build_elpais_issues(year, month, start_day, end_day)

    # scrape a pdf from http://elpais.com/ and convert it to png 
    FileUtils.mkdir "pics/elpais" unless File.directory? "pics/elpais" 

    # fist issue available date is 2012/03/01
    issues = Scraper.issues_dates year, month, start_day, end_day

    newspapers_issues_paths = []

    issues.each do |d| 
      newspapers_issues_paths << "http://srv00.epimg.net/pdf/elpais/1aPagina/" + d[0..7] + "ep-" + d[0..3] + d[5..6] + d[8..11] + ".pdf"
    end

    newspapers_issues_paths
  end

  

end

FileUtils.mkdir "pics" unless File.directory? "pics"
Scraper.get_issues  
# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

@base_url = "http://en.wikipedia.org" # used to create absolute URLs
@start_url = "http://en.wikipedia.org/wiki/Category:Algorithms" # where you will start recursively getting categories from
@depth_limit = 3
@categories = Hash.new
@pages = Hash.new

def get_categories(current_depth, current_url)
  if current_depth <= @depth_limit
    puts "getting categories at depth = " + current_depth.to_s
    # update the url
    curr_doc = Nokogiri::HTML(open(current_url))
    curr_doc.css(".CategoryTreeLabelCategory").each_with_index do |item|
      # save the category if it doesn't already exist and look for subcategories recursively
      if !@categories.include? item.text
        full_url = @base_url + item['href']
        @categories[item.text] = full_url
        get_categories(current_depth+1, full_url)
      end
    end
  end
end

# iterates over the lines of categories.txt to save the pages
def create_pages
  categories_file = File.open("categories.txt", "r")
  categories_file.each do |category_url|
    category_url = category_url.split("||")[1].gsub(" ","")
    puts "category_url=" + category_url
    doc = Nokogiri::HTML(open(category_url))
    doc.css("#mw-pages li a").each do |item| # grabs each page linked for the category
      if !@pages.include? item.text
        @pages[item.text] = category_url.split("Category:")[1] # inverted hash: page is key, parent category is value
        filename = item.text.gsub("User:","").gsub("/","-")
        page_url = @base_url + item['href']
        puts "file=" + item.text
        page = Nokogiri::HTML(open(page_url))
        file = File.new("wikipedia/" + filename, "w")
        file.puts page # write whole html page to file
        file.close
      end
    end
  end
end

# wrapper for get_categories; grabs all the categories and subcategories recursively from @start_url
def init_get_categories
  get_categories(1, @start_url)
  file = File.new("categories.txt", "w")
  @categories.each_with_index do |item,i|
     file.puts "#{item[0]} || #{item[1]}"
  end
  file.close
end

# turn these on to generate categories.txt or pages
#init_get_categories
#create_pages# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

@base_url = "http://en.wikipedia.org" # used to create absolute URLs
@start_url = "http://en.wikipedia.org/wiki/Category:Algorithms" # where you will start recursively getting categories from
@depth_limit = 3
@categories = Hash.new
@pages = Hash.new

def get_categories(current_depth, current_url)
  if current_depth <= @depth_limit
    puts "getting categories at depth = " + current_depth.to_s
    # update the url
    curr_doc = Nokogiri::HTML(open(current_url))
    curr_doc.css(".CategoryTreeLabelCategory").each_with_index do |item|
      # save the category if it doesn't already exist and look for subcategories recursively
      if !@categories.include? item.text
        full_url = @base_url + item['href']
        @categories[item.text] = full_url
        get_categories(current_depth+1, full_url)
      end
    end
  end
end

# iterates over the lines of categories.txt to save the pages
def create_pages
  categories_file = File.open("categories.txt", "r")
  categories_file.each do |category_url|
    category_url = category_url.split("||")[1].gsub(" ","")
    puts "category_url=" + category_url
    doc = Nokogiri::HTML(open(category_url))
    doc.css("#mw-pages li a").each do |item| # grabs each page linked for the category
      if !@pages.include? item.text
        @pages[item.text] = category_url.split("Category:")[1] # inverted hash: page is key, parent category is value
        filename = item.text.gsub("User:","").gsub("/","-")
        page_url = @base_url + item['href']
        puts "file=" + item.text
        page = Nokogiri::HTML(open(page_url))
        file = File.new("wikipedia/" + filename, "w")
        file.puts page # write whole html page to file
        file.close
      end
    end
  end
end

# wrapper for get_categories; grabs all the categories and subcategories recursively from @start_url
def init_get_categories
  get_categories(1, @start_url)
  file = File.new("categories.txt", "w")
  @categories.each_with_index do |item,i|
     file.puts "#{item[0]} || #{item[1]}"
  end
  file.close
end

# turn these on to generate categories.txt or pages
#init_get_categories
#create_pages# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

@base_url = "http://en.wikipedia.org" # used to create absolute URLs
@start_url = "http://en.wikipedia.org/wiki/Category:Algorithms" # where you will start recursively getting categories from
@depth_limit = 3
@categories = Hash.new
@pages = Hash.new

def get_categories(current_depth, current_url)
  if current_depth <= @depth_limit
    puts "getting categories at depth = " + current_depth.to_s
    # update the url
    curr_doc = Nokogiri::HTML(open(current_url))
    curr_doc.css(".CategoryTreeLabelCategory").each_with_index do |item|
      # save the category if it doesn't already exist and look for subcategories recursively
      if !@categories.include? item.text
        full_url = @base_url + item['href']
        @categories[item.text] = full_url
        get_categories(current_depth+1, full_url)
      end
    end
  end
end

# iterates over the lines of categories.txt to save the pages
def create_pages
  categories_file = File.open("categories.txt", "r")
  categories_file.each do |category_url|
    category_url = category_url.split("||")[1].gsub(" ","")
    puts "category_url=" + category_url
    doc = Nokogiri::HTML(open(category_url))
    doc.css("#mw-pages li a").each do |item| # grabs each page linked for the category
      if !@pages.include? item.text
        @pages[item.text] = category_url.split("Category:")[1] # inverted hash: page is key, parent category is value
        filename = item.text.gsub("User:","").gsub("/","-")
        page_url = @base_url + item['href']
        puts "file=" + item.text
        page = Nokogiri::HTML(open(page_url))
        file = File.new("wikipedia/" + filename, "w")
        file.puts page # write whole html page to file
        file.close
      end
    end
  end
end

# wrapper for get_categories; grabs all the categories and subcategories recursively from @start_url
def init_get_categories
  get_categories(1, @start_url)
  file = File.new("categories.txt", "w")
  @categories.each_with_index do |item,i|
     file.puts "#{item[0]} || #{item[1]}"
  end
  file.close
end

# turn these on to generate categories.txt or pages
#init_get_categories
#create_pages# Blank Ruby

require 'rubygems'
require 'nokogiri'
require 'open-uri'

@base_url = "http://en.wikipedia.org" # used to create absolute URLs
@start_url = "http://en.wikipedia.org/wiki/Category:Algorithms" # where you will start recursively getting categories from
@depth_limit = 3
@categories = Hash.new
@pages = Hash.new

def get_categories(current_depth, current_url)
  if current_depth <= @depth_limit
    puts "getting categories at depth = " + current_depth.to_s
    # update the url
    curr_doc = Nokogiri::HTML(open(current_url))
    curr_doc.css(".CategoryTreeLabelCategory").each_with_index do |item|
      # save the category if it doesn't already exist and look for subcategories recursively
      if !@categories.include? item.text
        full_url = @base_url + item['href']
        @categories[item.text] = full_url
        get_categories(current_depth+1, full_url)
      end
    end
  end
end

# iterates over the lines of categories.txt to save the pages
def create_pages
  categories_file = File.open("categories.txt", "r")
  categories_file.each do |category_url|
    category_url = category_url.split("||")[1].gsub(" ","")
    puts "category_url=" + category_url
    doc = Nokogiri::HTML(open(category_url))
    doc.css("#mw-pages li a").each do |item| # grabs each page linked for the category
      if !@pages.include? item.text
        @pages[item.text] = category_url.split("Category:")[1] # inverted hash: page is key, parent category is value
        filename = item.text.gsub("User:","").gsub("/","-")
        page_url = @base_url + item['href']
        puts "file=" + item.text
        page = Nokogiri::HTML(open(page_url))
        file = File.new("wikipedia/" + filename, "w")
        file.puts page # write whole html page to file
        file.close
      end
    end
  end
end

# wrapper for get_categories; grabs all the categories and subcategories recursively from @start_url
def init_get_categories
  get_categories(1, @start_url)
  file = File.new("categories.txt", "w")
  @categories.each_with_index do |item,i|
     file.puts "#{item[0]} || #{item[1]}"
  end
  file.close
end

# turn these on to generate categories.txt or pages
#init_get_categories
#create_pages
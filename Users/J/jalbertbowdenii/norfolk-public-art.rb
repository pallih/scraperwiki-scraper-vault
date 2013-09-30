###############################################################################
# Scrapes norfolkpublicart.org to pull out images & descriptions and format them
# as structured data. These data can then be decorated with latitude & longitude
# for use in a mobile location app. norfolkpublicart.org belongs to City of
# Norfolk Department of Cultural Affairs. This scraper is part of a project by
# Code for Hampton Roads Brigade in cooperation with this department.
#
# http://codeforhamptonroads.org
#
# norfolkpublicart.org is a WordPress
#
# One reason for using a scraper is that process change is undesirable at this
# time. This approach utilizes the department's existing process. The department
# members continue to use a content management system to manage the content and
# we can extract a data set from it. In the future the department members can be
# trained to add location data to their content. There are likely WordPress
# map plugins and embeddable HTML map widgets that can be utilized by anyone who
# can edit in a WordPress. It is still desirable and useful to extract a dataset
# from that work product.
# 
#
# Algorithm:
# + visit norfolkpublicart.org project installation page
# + extract the'postarea' div and iterate its paragraphs
# + for each paragraph extract the elements for the schema
# sweet xpath ref http://stackoverflow.com/questions/2080799/how-to-use-xpath-nokogiri
# http://nokogiri.org/tutorials/searching_a_xml_html_document.html
# http://ruby.bastardsbook.com/chapters/html-parsing/
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://norfolkpublicart.org/public-art/installed-projects/'

# baseline schema
# SECTION, PLACENAME, TITLE, IMAGE, DESCRIPTION, SOURCE URL, (LAT), (LON)
# (future elements)

# scrape function: gets passed an individual paragraph to scrape
def scrape(para)
  # need SECTION & PLACENAME from para
  # need to follow embedded href to get DESCRIPTION
  links = para.css("a")
  # puts links.length
  # puts links.text

  # grabs href from anchor elements
  links.each{|links| puts links['href']}
  #grabs title from anchor elements
  links.each{|links| puts links['title']}
end

## scrape_items function: extract paras & iterate them
def scrape_items(url)
  page = Nokogiri::HTML(open(url))
  # debug, todo: make conditional, if DEBUG
  print url
  div = page.xpath("//div[@class = 'postarea']")
  paras = div.xpath("//p[position() > 2]")
  # debug, todo: make conditional, if DEBUG
  print paras.count.to_s()
  paras.each {
    |para|
    scrape(para)
paras.length
  }
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL
scrape_items(starting_url)


###############################################################################
# Scrapes norfolkpublicart.org to pull out images & descriptions and format them
# as structured data. These data can then be decorated with latitude & longitude
# for use in a mobile location app. norfolkpublicart.org belongs to City of
# Norfolk Department of Cultural Affairs. This scraper is part of a project by
# Code for Hampton Roads Brigade in cooperation with this department.
#
# http://codeforhamptonroads.org
#
# norfolkpublicart.org is a WordPress
#
# One reason for using a scraper is that process change is undesirable at this
# time. This approach utilizes the department's existing process. The department
# members continue to use a content management system to manage the content and
# we can extract a data set from it. In the future the department members can be
# trained to add location data to their content. There are likely WordPress
# map plugins and embeddable HTML map widgets that can be utilized by anyone who
# can edit in a WordPress. It is still desirable and useful to extract a dataset
# from that work product.
# 
#
# Algorithm:
# + visit norfolkpublicart.org project installation page
# + extract the'postarea' div and iterate its paragraphs
# + for each paragraph extract the elements for the schema
# sweet xpath ref http://stackoverflow.com/questions/2080799/how-to-use-xpath-nokogiri
# http://nokogiri.org/tutorials/searching_a_xml_html_document.html
# http://ruby.bastardsbook.com/chapters/html-parsing/
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://norfolkpublicart.org/public-art/installed-projects/'

# baseline schema
# SECTION, PLACENAME, TITLE, IMAGE, DESCRIPTION, SOURCE URL, (LAT), (LON)
# (future elements)

# scrape function: gets passed an individual paragraph to scrape
def scrape(para)
  # need SECTION & PLACENAME from para
  # need to follow embedded href to get DESCRIPTION
  links = para.css("a")
  # puts links.length
  # puts links.text

  # grabs href from anchor elements
  links.each{|links| puts links['href']}
  #grabs title from anchor elements
  links.each{|links| puts links['title']}
end

## scrape_items function: extract paras & iterate them
def scrape_items(url)
  page = Nokogiri::HTML(open(url))
  # debug, todo: make conditional, if DEBUG
  print url
  div = page.xpath("//div[@class = 'postarea']")
  paras = div.xpath("//p[position() > 2]")
  # debug, todo: make conditional, if DEBUG
  print paras.count.to_s()
  paras.each {
    |para|
    scrape(para)
paras.length
  }
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL
scrape_items(starting_url)



# Blank Ruby
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful mechanize library. Documentation is here: 
# http://mechanize.rubyforge.org/mechanize/
###############################################################################
require 'mechanize'

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
url = "http://easy.co.il/%D7%94%D7%9B%D7%9C/"
agent = Mechanize.new
page=
page.links.each do |link|

  puts link.text
end



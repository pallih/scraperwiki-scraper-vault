###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful mechanize library. Documentation is here: 
# http://mechanize.rubyforge.org/mechanize/
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
url = "http://northgate.liverpool.gov.uk/PlanningExplorer17/GeneralSearch.aspx"
agent = Mechanize.new
page = agent.get(url)
planning_form = page.form('M3Form')
planning_form.q = 'ruby mechanize'
planning_form.radiobuttons_with(:name => 'rbGroup')[1].check
page = agent.submit(planning_form)
pp page
#s = page.form_with(:name => 'M3Form')
#s.radiobuttons_with(:name => 'rbGroup')[1].check

#search_results = agent.submit(s)

#doc = Nokogiri::HTML(search_results)
#  doc.search('td').each do |td|
#   puts td.inner_html
# end
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful mechanize library. Documentation is here: 
# http://mechanize.rubyforge.org/mechanize/
###############################################################################
require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
url = "http://northgate.liverpool.gov.uk/PlanningExplorer17/GeneralSearch.aspx"
agent = Mechanize.new
page = agent.get(url)
planning_form = page.form('M3Form')
planning_form.q = 'ruby mechanize'
planning_form.radiobuttons_with(:name => 'rbGroup')[1].check
page = agent.submit(planning_form)
pp page
#s = page.form_with(:name => 'M3Form')
#s.radiobuttons_with(:name => 'rbGroup')[1].check

#search_results = agent.submit(s)

#doc = Nokogiri::HTML(search_results)
#  doc.search('td').each do |td|
#   puts td.inner_html
# end

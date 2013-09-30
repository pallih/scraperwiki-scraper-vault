###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful mechanize library. Documentation is here: 
# http://mechanize.rubyforge.org/mechanize/
###############################################################################
require 'mechanize'

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
url = "http://www.slforms.universalservice.org/Form470Expert/Search.aspx"
agent = Mechanize.new
page = agent.get(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
page.forms.each do |f|
  puts "--------------------"
  puts "Form name : " + f.name
  # loop through the controls in the form
  puts "Controls:"
  f.fields.each do |field|
    if field.node["type"]
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node["type"]}', '#{field.node["value"]}')"
    elsif field.node.name == 'select'
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node.name}', '#{field.options[0]}')"
      # loop through all the options in any select (drop-down) controls
      field.options.each do |opt|
        puts " - - - (value) = #{opt}"
      end
    else
      puts " - (type) ="
    end
  end
end
###############################################################################
# START HERE: Tutorial for scraping pages behind form, using the
# very powerful mechanize library. Documentation is here: 
# http://mechanize.rubyforge.org/mechanize/
###############################################################################
require 'mechanize'

# We're scraping the National Lottery grants form. You can
# replace this with the URL you're interested in.
url = "http://www.slforms.universalservice.org/Form470Expert/Search.aspx"
agent = Mechanize.new
page = agent.get(url)

#--------------------------------------------------------------------------------------
# Loop through all the forms on the page, and print some information about each one.
# This should work with your own URL.
#--------------------------------------------------------------------------------------
page.forms.each do |f|
  puts "--------------------"
  puts "Form name : " + f.name
  # loop through the controls in the form
  puts "Controls:"
  f.fields.each do |field|
    if field.node["type"]
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node["type"]}', '#{field.node["value"]}')"
    elsif field.node.name == 'select'
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node.name}', '#{field.options[0]}')"
      # loop through all the options in any select (drop-down) controls
      field.options.each do |opt|
        puts " - - - (value) = #{opt}"
      end
    else
      puts " - (type) ="
    end
  end
end

  # open the required libraries
  require 'rubygems'
  require 'nokogiri'
  require 'open-uri'

  # Using nokogiri, fetch Wikipedia's list of presidents page
  list_of_presidents = Nokogiri::HTML(open('http://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States'))

  # Using another nokogiri method, grab the third column from every row, and from those, grab the first hyperlink (which contains the prez's name)
  an_array_of_links = list_of_presidents.xpath("//tr/td[3]/a[1]")

count = 0

    an_array_of_links.each do |link_to_test|

    # This above statement can be read as: for each element in an_array_of_links, do
    # the following code (until the end line)
    # And as you go through each element, the variable use to reference the element will be named "link_to_test"

       last_name = link_to_test.content.split(' ')[-1]   
#remember that between the <a> tags was the president's name, with the last word being the last name
      if last_name.length > 6
        the_link_to_the_presidents_page = link_to_test["href"]

            # OK, the value of href is going to be something like "/wiki/George_Washington". That's an address relative to the                   Wikipedia site so we need to prepend "http://en.wikipedia.org" to have a valid address...

    the_link_to_the_presidents_page = "http://en.wikipedia.org"+the_link_to_the_presidents_page

    # now let's fetch that page

    the_presidents_page = Nokogiri::HTML(open(the_link_to_the_presidents_page))
    death_date = the_presidents_page.xpath("//th[contains(text(), 'Died')]/following-sibling::*")[0].content
    age_at_death = death_date.match(/aged.+?([0-9])/)[1]
    # ... OK, now what?
    puts death_date
    puts age_at_death
  end
      end
    # OK, we're at the end of the each loop. Go back to the top
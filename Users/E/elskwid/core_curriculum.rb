## Using a library / gem
# We need some help
require "mechanize"

## Creating a new thing
# Just like a browser
browser = Mechanize.send(:new)

## Using this "object"
# Get the page
page = browser.get "http://catalog.unr.edu/preview_program.php?catoid=1&poid=3"

## Arrays
# Find all the paragraphs on the page
paragraphs = page.search("p")

## Using an array
# Find our heading
heading = paragraphs.find{ |p| p.text == "General Capstone Courses:" }

## Using the element methods
# The list is the next element (UL) after the heading
list = heading.next_element

## Revisit search from another point in the page
# The course links contain the URL and the text
links = list.search("a")

## More array usage
# Look at each link
# links.each do |link|
#   puts link.text
# end

# There's data here!
# PSC 409K - Jurisprudence

# Department Course number - Course name

links.each do |link|
  department_and_number, name = link.text.split(" - ")
  department, number = department_and_number.split(" ")
  puts "Department: #{department}  Number: #{number}  Name: #{name}"
end





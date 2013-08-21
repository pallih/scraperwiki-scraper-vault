## This tutorial is to help you parse a single page from the Lottery grants database
## We get to these pages using the mechanize library, but that's a different problem.
## The lesson here is about cleaning up the data for one record.
## For this example we will eschew Nokogiri and use old fashioned regular expressions
require 'date'

## the link for single page of data
url = 'http://www.lottery.culture.gov.uk/GrantDetails.aspx?ID=15752755&DBID=AE'

## scrape the text from that page
text = ScraperWiki.scrape(url)
puts 'Original page source:'
puts text
puts 'click on the more... link above to see the whole page'

## Note how the data is you're after comes after <TABLE ...  Table4...

## This next bit extracts just that table text using regular expressions
## Please uncomment the 4 programming lines below by deleting the # character from the start of each line

#if text =~ /<table[^>]*? id="Table4"[^>]*>(.*?)<\/table>/m
#  table4 = $1
#  puts table4
#end

## This next bit separates out all the rows
## (Uncomment the next 2 lines and click run again)
#rows = table4.split('</tr>')
#puts rows

data = {}   # this is where we are going to put the result

## This next section loops through each row on its own
#print 'Look at each row on its own'
#rows.each do |row|
#  if row =~ /<font size="-1">(.*?)<\/font><\/span>\s*<\/td>\s*<td width="\*">\s*<span id=".*?">(.*?)<\/span>\s*<\/td>/
#    data [$1] = $2
#  end
#end

#puts "The data is now represented in the data hash:"
#puts data

## Now we do the clean-up stages

## First turn the monetary amount into a number
#amount = data["Grant Amount"]
#puts "Original form: #{amount}"
#amount = amount.gsub(/[^\d]/,'')
#puts "With everything but the digits removed: #{amount}"
## now we can set it back as an integer number
#data["Grant Amount"] = amount.to_i


## Now convert the date into a real date object
#data["Grant Date"] = Date.strptime(data["Grant Date"],'%d/%m/%Y')
#puts "Finally, the cleaned up date is:", data

## We still should give the constituency and local authorities unique ids to before the job is really done!


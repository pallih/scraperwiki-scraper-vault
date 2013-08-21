import scraperwiki

import re # Python's regular expression package

# Have to use \. sometimes because . by itself is the wildcard symbol
# and similarly with \$ - $ is a special symbol (look at the docs!)
# Here the pattern has been updated to support decimals in the price.
pattern  = '(\w.) -|is \$([0-9\.,]+) to stay for|for ([0-9]+) (hour|day|week|month|year)s?\.'
line     = 'Hotel A - $50 to stay for 6 hours.'
line2   = 'Hotel B - $92 to stay for 2 days.'
line3   = 'Hotel C - $1000 to stay for 1 week.'
line4   = 'Hotel Z is $20 for 1 hour.'

match_result = re.match(pattern, line)

# Check if we got a match
if match_result:
    # Print the elements we extracted in CSV format: Hotel ,92.30,2,day
    print ','.join( match_result.groups() )
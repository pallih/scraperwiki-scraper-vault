import scraperwiki
import re

# Blank Python

full_name = "Glen Edward McGregor"
middle_name = re.search("Glen(.+?)McGregor", full_name)
print middle_name
middle_name = middle_name.group(1)
print middle_name

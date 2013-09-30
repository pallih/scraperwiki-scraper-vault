import scraperwiki
import csv
import requests
import string

global_var = 'links'

alpha = ["A","B","C"]
url_start = "http://chamber.sdncc.com/list/searchalpha/"
url_end = ".htm"
URL = url_start + alpha[0] + url_end


for i in alpha:
    URL = url_start + i + url_end
    print URL

numeric = [1,2,3,4,5,6,7,8,9,10,11]
for i in numeric:
  mod = i%3
  print mod

print "finished"

links = []
links2 = []

def sample_function(var):
    links.append((var,var))
    # print links
    # print "done"
    return links

vars = [1,2,3,4,5]
for i in vars:
    links2.extend(sample_function(i))
    print links
    
    

for info in links:
    data = {
        'var1' : info[0],
        'var2' : info[1]
    }
    scraperwiki.sqlite.save(unique_keys=['var1'], data=data)
import scraperwiki
import csv
import requests
import string

global_var = 'links'

alpha = ["A","B","C"]
url_start = "http://chamber.sdncc.com/list/searchalpha/"
url_end = ".htm"
URL = url_start + alpha[0] + url_end


for i in alpha:
    URL = url_start + i + url_end
    print URL

numeric = [1,2,3,4,5,6,7,8,9,10,11]
for i in numeric:
  mod = i%3
  print mod

print "finished"

links = []
links2 = []

def sample_function(var):
    links.append((var,var))
    # print links
    # print "done"
    return links

vars = [1,2,3,4,5]
for i in vars:
    links2.extend(sample_function(i))
    print links
    
    

for info in links:
    data = {
        'var1' : info[0],
        'var2' : info[1]
    }
    scraperwiki.sqlite.save(unique_keys=['var1'], data=data)

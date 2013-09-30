import scraperwiki

###############################################################################
# Basic scraper
###############################################################################

import re #what is re?

url = 'http://www.lse.co.uk/index-constituents.asp?index=idx:ukx'#target data

data_re = "<td.*?><a.*?/a><a.*?>(.*?)</a></td>" # what is going on here? 

data = scraperwiki.scrape(url)##calls the url variable above

for td in re.findall (data_re, data): ##calls the variable above for/else loop
    cnt = td.count ('(') #why only open parentheses? because the html reads that way:  grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!!
    if cnt == 1:
        code = td[td.index('(')+1:-1] #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
    elif cnt == 2:
        first = td.index('(') #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
        second = td[first+1:].index('(')  #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
        code = td[first+second+2:-1]# how does this work?
    scraperwiki.sqlite.save(["Constituents"], {"Constituents":code})

 
    import scraperwiki

###############################################################################
# Basic scraper
###############################################################################

import re #what is re?

url = 'http://www.lse.co.uk/index-constituents.asp?index=idx:ukx'#target data

data_re = "<td.*?><a.*?/a><a.*?>(.*?)</a></td>" # what is going on here? 

data = scraperwiki.scrape(url)##calls the url variable above

for td in re.findall (data_re, data): ##calls the variable above for/else loop
    cnt = td.count ('(') #why only open parentheses? because the html reads that way:  grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!!
    if cnt == 1:
        code = td[td.index('(')+1:-1] #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
    elif cnt == 2:
        first = td.index('(') #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
        second = td[first+1:].index('(')  #grab only the text AFTER the parentheses example 3i Inf. Ord (3IN)!! but what else is happening here?
        code = td[first+second+2:-1]# how does this work?
    scraperwiki.sqlite.save(["Constituents"], {"Constituents":code})

 
    
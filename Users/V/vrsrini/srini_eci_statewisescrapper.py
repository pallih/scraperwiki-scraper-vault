import scraperwiki
import lxml.html



#SETUP
baseurl = 'http://eciresults.ap.nic.in/Statewise'
result_xpath = '//table[@border="1" ]/tr' #this is probably not good performance wise - but fine for now

# This is the state code for Tripura
state = 's23' 
#Other states are:
# S05 Goa
# S14 Manipur
# S19 Punjab
# S28 Uttarakhand

#states = {'Tripura':'s23', 'Goa':'s05', 'Manipur': 's14', 'Punjab':'s19','Uttarakhand':'s28'}

#DEFS
def process_state(state, number):
    record = {}
    record['state'] = state
    numb = str(number)
    html = scraperwiki.scrape(baseurl+state+numb+'.htm')
    print 'Processing ',state,numb
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    for x in results[4:15]: #skip the first 4 tr's and the last one
        record['constituency'] = x[0].text
        record['constituency_no'] = x[1].text
        record['leading_cand'] =  x[2].text
        record['leading_party'] = x[3].text
        record['trailing_cand'] = x[4].text
        record['trailing_party'] =  x[5].text
        record['margin'] =  x[6].text
        record['status'] =  x[7].text
        scraperwiki.sqlite.save(unique_keys=['constituency_no'], data=record, table_name='tripura-elections')   
#, 'leading_cand', 'leading_party', 'trailing_cand', 'trailing_party', 'margin'
    else:
        pass

#######################

#Scrape the first page to get the list of constituencies
#html = scraperwiki.scrape('http://eciresults.ap.nic.in/ConstituencywiseS2489.htm')

#The list of constituencies for Uttar Pradesh is in this markup:
# <input type="hidden" id="HdnFldUttarPradesh" value=

#Lets get that list with values to add to our baseurl


#root = lxml.html.fromstring(html)
#content = root.xpath (constituency_xpath)

#for c in content:
   # constituencies = c.attrib['value']

#def process_if_next (countern):
    #countern=countern+1
    #print 'the counter is  ',str(countern)
    #if countern <=18:
        #process_state (state, countern)
        #process_if_next(countern)
    # else:
        #pass
    


# A list of numbers and the name of the constituency
#constituencies = constituencies.split(';')

# And now we iterate through the list
#for c in constituencies:
n=""
process_state( state,n )
n=1
for i in range(1,7):
        #print "Inside the Loop", str(i+1)
        process_state (state,i)
else:
    pass
#process_if_next(n)
  import scraperwiki
import lxml.html



#SETUP
baseurl = 'http://eciresults.ap.nic.in/Statewise'
result_xpath = '//table[@border="1" ]/tr' #this is probably not good performance wise - but fine for now

# This is the state code for Tripura
state = 's23' 
#Other states are:
# S05 Goa
# S14 Manipur
# S19 Punjab
# S28 Uttarakhand

#states = {'Tripura':'s23', 'Goa':'s05', 'Manipur': 's14', 'Punjab':'s19','Uttarakhand':'s28'}

#DEFS
def process_state(state, number):
    record = {}
    record['state'] = state
    numb = str(number)
    html = scraperwiki.scrape(baseurl+state+numb+'.htm')
    print 'Processing ',state,numb
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    for x in results[4:15]: #skip the first 4 tr's and the last one
        record['constituency'] = x[0].text
        record['constituency_no'] = x[1].text
        record['leading_cand'] =  x[2].text
        record['leading_party'] = x[3].text
        record['trailing_cand'] = x[4].text
        record['trailing_party'] =  x[5].text
        record['margin'] =  x[6].text
        record['status'] =  x[7].text
        scraperwiki.sqlite.save(unique_keys=['constituency_no'], data=record, table_name='tripura-elections')   
#, 'leading_cand', 'leading_party', 'trailing_cand', 'trailing_party', 'margin'
    else:
        pass

#######################

#Scrape the first page to get the list of constituencies
#html = scraperwiki.scrape('http://eciresults.ap.nic.in/ConstituencywiseS2489.htm')

#The list of constituencies for Uttar Pradesh is in this markup:
# <input type="hidden" id="HdnFldUttarPradesh" value=

#Lets get that list with values to add to our baseurl


#root = lxml.html.fromstring(html)
#content = root.xpath (constituency_xpath)

#for c in content:
   # constituencies = c.attrib['value']

#def process_if_next (countern):
    #countern=countern+1
    #print 'the counter is  ',str(countern)
    #if countern <=18:
        #process_state (state, countern)
        #process_if_next(countern)
    # else:
        #pass
    


# A list of numbers and the name of the constituency
#constituencies = constituencies.split(';')

# And now we iterate through the list
#for c in constituencies:
n=""
process_state( state,n )
n=1
for i in range(1,7):
        #print "Inside the Loop", str(i+1)
        process_state (state,i)
else:
    pass
#process_if_next(n)
  
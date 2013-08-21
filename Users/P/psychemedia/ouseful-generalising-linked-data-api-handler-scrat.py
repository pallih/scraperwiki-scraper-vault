import simplejson
import urllib
import scraperwiki

'''
Scratchpad for messing around with Linked Data API code so we can use the same functions to handle all LD API calls, not just edubase ones

'''

#------- USER SETTINGS ------
# Original API documentation at: http://services.data.gov.uk/education/api/api-config#schools
# Original blog post by @jenit describing the API used: http://data.gov.uk/blog/guest-post-developers-guide-linked-data-apis-jeni-tennison
# Original blog post describing this Scraperwiki page: http://blog.ouseful.info/2010/11/03/accessing-government-education-data-in-scraperwiki-via-the-edubaseeducation-datastore-api/

# The main query
eduPath='school/constituency-name/Horsham'

# Filters, as a list:
eduFilters=['min-statutoryHighAge=7','max-statutoryHighAge=10']

# _views - not considered yet...

# key and label data is displayed in the console for each result, and added to the Scraperwiki database
# keys are the top level attributes we want to display. For a result item, display each item[key]
keys=['establishmentNumber','label']

# labels are used to display labels of top level items, e.g. item[label]['label']
labels=['typeOfEstablishment','phaseOfEducation']
# Note, if you have item[path][wherever][label], or deeper down a path, we don't handle that (yet?!)

# The school ID will always be added to the Scraperwiki database (it's the database ID for a record).
# If latitude/longitude data is available, it will also be added to the database.

# Note that the script doesn't yet handle multiple pages of results either...

#-------------------------- 

  
# This function displays the results, and also adds results to the Scraperwiki database.
# We always look for school ID (this is the table ID) and latlng for mapping, if that data exists
def printDetails(item,keys=['establishmentNumber','label'],labels=[]):
    txt=[]
    record={}
    for key in keys:
        if key in item:
            txt.append(str(item[key]))
            record[key]=item[key]
        else:
            record[key]=''
    if 'establishmentNumber' not in keys:
        record['establishmentNumber']=item['establishmentNumber']
    for attribute in labels:
        if attribute in item:
            txt.append(item[attribute]['label'])
            record[attribute]=item[attribute]['label']
        else:
            record[attribute]=''
    if 'lat' in item:
        latlng=(item['lat'],item['long'])
        scraperwiki.datastore.save(["establishmentNumber"], record,latlng=latlng)
    else:
        scraperwiki.datastore.save(["establishmentNumber"], record)
        pass
    print ', '.join(txt)    

def printDetails2(item,keys=[],labels=[]):
    txt=[]
    record={}
    for key in keys:
        if key in item:
            txt.append(str(item[key].encode('utf-8')))
            record[key]=item[key]
        else:
            record[key]=''
    for attribute in labels:
        if attribute in item:
            txt.append(item[attribute]['label'].encode('utf-8'))
            record[attribute]=item[attribute]['label']
        else:
            record[attribute]=''
    if 'lat' in item:
        latlng=(item['lat'],item['long'])
        scraperwiki.datastore.save([keys[0]], record,latlng=latlng)
    else:
        scraperwiki.datastore.save([keys[0]], record)
        pass
    print ', '.join(txt)    

    
# This is where we construct the Edubase Linked Data API URL, and then call it, returning JSON 
#data=simplejson.load(urllib.urlopen('http://services.data.gov.uk/education/api/'+eduPath+'.json'+'?'+'&'.join(eduFilters)))['result']

url='http://reference.data.gov.uk/doc/department/bis/post.json'
data=simplejson.load(urllib.urlopen(url))['result']
                   
# Need to find a way of handling results spread over several results pages
items=data["items"]
keys=['comment']
labels=[]
for item in items:
    print item
    #maybe use first key as the id?
    printDetails2(item,keys,labels)
    

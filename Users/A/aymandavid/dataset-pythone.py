import simplejson
import urllib
import scraperwiki

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

'''
# Function that digs into a set of results and prints out what they contain...
def dataExplorer(data,depth=0,d=''):
    indent=''
    i=0
    while i<depth:
        indent+='> '
        i+=1
    if depth==1:
        print '------------------'
    if type(data) is dict:
        depth+=1
        for d in data:
            print indent,d
            dataExplorer(data[d],depth,d)
    elif type(data) is list:
        depth+=1
        for item in data:
            dataExplorer(item,depth,d)
    else:
        print indent,data
'''
  
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
    
    
# This is where we construct the Edubase Linked Data API URL, and then call it, returning JSON 
data=simplejson.load(urllib.urlopen('http://services.data.gov.uk/education/api/'+eduPath+'.json'+'?'+'&'.join(eduFilters)))['result']

# Need to find a way of handling results spread over several results pages
items=data["items"]

for item in items:
    printDetails(item,keys,labels)
    print item

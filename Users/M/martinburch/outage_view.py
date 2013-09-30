sourcescraper = 'coned'

import scraperwiki
import datetime           
scraperwiki.sqlite.attach("coned")

data = scraperwiki.sqlite.select(           
    '''DISTINCT `Update`,`Fetch` FROM coned.NYC'''
)

for index, row in enumerate(data):
    if(isinstance(data[index]['Fetch'], unicode)):
        try:
            updatetime = datetime.datetime.strptime(row['Update'], "%Y_%m_%d_%H_%M_%S")
            fetchtime1 = datetime.datetime.strptime(data[index]['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=-4)
            fetchtime2 = datetime.datetime.strptime(data[index+1]['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=-4)
            updatefetchdelta = fetchtime1-updatetime
            fetchdelta = fetchtime2-fetchtime1
            print ("Fetch:" + str(fetchtime1) + " | Time to next fetch:" + str(fetchdelta))
            #print ("Update " + str(updatetime) + " fetched " + str(updatefetchdelta) + " later, " + str(fetchdelta) + " since last fetch")
        except IndexError:
            break

'''

 + str(updatefetchdelta) ", " + str(fetchdelta) + " after last update"
for row in data:
    if(isinstance(row['Fetch'], unicode)):
        updatetime = datetime.datetime.strptime(row['Update'], "%Y_%m_%d_%H_%M_%S")
        fetchtime = datetime.datetime.strptime(row['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")
        fetchtime = fetchtime+datetime.timedelta(hours=-4)
        print fetchtime-updatetime
        print "---"
'''sourcescraper = 'coned'

import scraperwiki
import datetime           
scraperwiki.sqlite.attach("coned")

data = scraperwiki.sqlite.select(           
    '''DISTINCT `Update`,`Fetch` FROM coned.NYC'''
)

for index, row in enumerate(data):
    if(isinstance(data[index]['Fetch'], unicode)):
        try:
            updatetime = datetime.datetime.strptime(row['Update'], "%Y_%m_%d_%H_%M_%S")
            fetchtime1 = datetime.datetime.strptime(data[index]['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=-4)
            fetchtime2 = datetime.datetime.strptime(data[index+1]['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")+datetime.timedelta(hours=-4)
            updatefetchdelta = fetchtime1-updatetime
            fetchdelta = fetchtime2-fetchtime1
            print ("Fetch:" + str(fetchtime1) + " | Time to next fetch:" + str(fetchdelta))
            #print ("Update " + str(updatetime) + " fetched " + str(updatefetchdelta) + " later, " + str(fetchdelta) + " since last fetch")
        except IndexError:
            break

'''

 + str(updatefetchdelta) ", " + str(fetchdelta) + " after last update"
for row in data:
    if(isinstance(row['Fetch'], unicode)):
        updatetime = datetime.datetime.strptime(row['Update'], "%Y_%m_%d_%H_%M_%S")
        fetchtime = datetime.datetime.strptime(row['Fetch'][:-6], "%Y-%m-%d %H:%M:%S")
        fetchtime = fetchtime+datetime.timedelta(hours=-4)
        print fetchtime-updatetime
        print "---"
'''
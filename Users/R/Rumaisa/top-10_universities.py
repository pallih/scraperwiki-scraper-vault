import urllib
import csv

# fill in the input file here
url = "http://www.thecompleteuniversityguide.co.uk/single.htm?ipg=8727"

fin = urllib.urlopen(url)
lines = fin.readlines()
for line in lines:
    print line

#clist = list(csv.reader(lines))
#print clist


#headers = clist.pop(0)
#print "There are %d columns and %d rows" % (len(headers), len(clist))
#print "Headers:", headers

#for row in clist[:10]:
#    print dict(zip(headers, row))

def info():
    import scraperwiki
    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"1","Institution Name":"Warwick", "Student Satisfaction":"3.98","Research Assessment":"2.95","Entry standards":"473","Graduate Prospect":"86","Overall Score":"100.0"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"2","Institution Name":"London School of Economics", "Student Satisfaction":"3.77","Research Assessment":"2.95","Entry standards":"482","Graduate Prospect":"88","Overall Score":"99.6"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"3","Institution Name":"Bath", "Student Satisfaction":"3.81","Research Assessment":"2.95","Entry standards":"452","Graduate Prospect":"","Overall Score":"97.4"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"4","Institution Name":"Strathclyde", "Student Satisfaction":"3.97","Research Assessment":"2.85","Entry standards":"438","Graduate Prospect":"82","Overall Score":"96.8"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"5","Institution Name":"Leeds", "Student Satisfaction":"3.86","Research Assessment":"2.85","Entry standards":"426","Graduate Prospect":"84","Overall Score":"96.2"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"6","Institution Name":"Lancaster", "Student Satisfaction":"4.06","Research Assessment":"2.95","Entry standards":"385","Graduate Prospect":"82","Overall Score":"96.0"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"7","Institution Name":"Loughborough", "Student Satisfaction":"4.02","Research Assessment":"2.70","Entry standards":"412","Graduate Prospect":"84","Overall Score":"95.3"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"8","Institution Name":"Exeter", "Student Satisfaction":"4.30","Research Assessment":"2.60","Entry standards":"405","Graduate Prospect":"80","Overall Score":"94.8"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"9","Institution Name":"Southampton", "Student Satisfaction":"3.88","Research Assessment":"2.60","Entry standards":"425","Graduate Prospect":"82","Overall Score":"93.8"}) 

    scraperwiki.datastore.save(unique_keys=["Rank"], data={"Rank":"10","Institution Name":"Bristol", "Student Satisfaction":"3.83","Research Assessment":"2.55","Entry standards":"430","Graduate Prospect":"84","Overall Score":"93.8"}) 

info()


import scraperwiki
import urllib
import csv



def link1(url):
    lines = urllib.urlopen(url).readlines()
    clist = list(csv.reader(lines))
    
#    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#    def convertdate(d):
#        md = re.match("(\w+) (\d+)$", d)
#        imonth = months.index(md.group(1)) + 1
#        return '%s-%02d'%(md.group(2), imonth)
    
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)   
    header.append("Adviser")
    print header
    #if clist[0][1] != "" and clist[0][0]!="":
    print clist
    adviser = ''
    org = ''
    rownumber = 1
    for row in clist:
        rownumber += 1
        if row[0]=='':
            break
        if row[1] != '':
            org = row[1]
        else:
            row[1] = org
        if row[0][0] == 'F' or row[0][0] == 'N':
            adviser = row[0]
            continue
        row.append(adviser)
        data = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row
        data['Row Number'] = rownumber
        print data
        #scraperwiki.datastore.save(unique_keys=["Row Number"], data=data)

link1("http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/special-advisers-hospitality/hospitality-special-advisers.csv?view=Binary")
link2("http://www.homeoffice.gov.uk/publications/about-us/corporate-publications/special-advisers-hospitality/hospitality-spads-sept.csv?view=Binary")
   

from lxml import etree
import scraperwiki
from urllib2 import Request, urlopen, URLError


#exit() # not do anything for now

def byrow_imper(lod, keylist):
    """Converts a list of dictionaries to a list of lists using the
    values of the dictionaries. Assumes that each dictionary has the
    same keys. 
       lod: list of dictionaries
       keylist: list of keys, ordered as desired
       Returns: a list of lists where the inner lists are rows. 
         i.e. returns a list of rows. """
    # imperative/procedural approach
    lol = []
    for row in lod:
        row2 = []
        for key in keylist:
            row2.append(row[key])
        lol.append(row2)
    return lol

scraperwiki.sqlite.attach('trial_is_company_numbers_1')

'''
select TCode
from Tracking
where not exists (select *
from Task
where Task.TCode = Tracking.TCode
)
'''

#data = scraperwiki.sqlite.select("* iceland_corporate_entities order by date_time DESC")

data = scraperwiki.sqlite.select("CompanyNumber, RegistryUrl from iceland_corporate_entities where not exists(select * from swdata where swdata.CompanyNumber = iceland_corporate_entities.CompanyNumber)") #only select the ones we haven´t done yet

print 'Number to do: ', len(data)
print
print

#keylist = ['CompanyNumber','RegistryUrl','CompanyName','date_time']
#hugelist = byrow_imper(data, keylist)

#print hugelist
#exit()


scraperwiki.sqlite.attach('isat2008')
isat2008 = scraperwiki.sqlite.select("* from isat2008")
#print isat2008


def process_xml(url,number):
    req = Request(url)
    record = {}
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server. Reason: ', e.reason
        elif hasattr(e, 'code'):
            if e.code == 404:
                print "The company is defunct - mark it!"
                record['CompanyNumber'] = number
                record['defunc'] = 1
                #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)
                return record
            else:
                print "The server couldn\'t fulfill the request.'Error code: ", e.code
                # record['CompanyNumber'] = number
                # record['defunc'] = 1
            #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)
            print record
    else:
    # everything is fine
        xml = response.read()
        #print xml
        
        root = etree.fromstring(xml)
        isat2008_number = root.xpath('//isat[@class="2008"]/number')

        isat2008_desc = root.xpath('//isat[@class="2008"]/name')
        isat95_number = root.xpath('//isat[@class="95"]/number')
        isat95_desc = root.xpath('//isat[@class="95"]/name')
        registration_type = root.xpath('//type')
        if isat95_number:
            record['isat95_number']=isat95_number[0].text
            record['isat95_desc']=isat95_desc[0].text
        if (len(isat2008_number)>1):
            print "number of 2008 numbers: ", len(isat2008_number)
            print isat2008_number
            print type(isat2008_number)
            for m in isat2008_number:
                print m.text
                if m.text == '99.99.9':
                    print "oh no"
                
            isat2008_number_list = list(isat2008_number)
            print isat2008_number_list

            #if any(d.get('CompanyNumber') == number for d in done_numbers)
            #if "99.99.9" in isat2008_number_list:
            #    print "oh no!"
            record['isat2008_number']=isat2008_number[0].text
            record['isat2008_desc']=isat2008_desc[0].text
            isic4 = filter( lambda x: x['ISAT2008']==isat2008_number[0].text[:5], isat2008 )
        else:
             isic4 = None   
        record['registration_type']=registration_type[0].text
        if isic4:
            record['isic4_number']= isic4[0]['ISIC4']
            record['isat2008_desc_en']= isic4[0]['description_en']
        record['CompanyNumber'] = number
        print record
        #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)
for d in data:
    url = d['RegistryUrl']
    number = d['CompanyNumber']
    #process_xml(url,number)



xml = process_xml('http://rsk.is/ws/other/enterprisereg/0207535794.xml','555')
print record 


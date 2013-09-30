import scraperwiki

import csv,json,requests

data = scraperwiki.scrape('http://ge.tt/api/1/files/9pOLJig/0/blob?download')
pincodes=[]
reader = csv.reader(data.splitlines())

for row in reader:
    pincodes.append(row[0])

print pincodes[1:10]


def main():
    u='http://www.chevrolet.com/bypass/gmna/dealerlocator/services/getdealers?type=PostalCode&format=JSON&x-country=US&x-language=en&x-brand=Chevrolet&postalcode={0}'

 #   f = csv.writer(open("e:\\gigs\\v1CHEVROLET.csv", "ab+"))
#    f.writerow(['Name','street','City','State','Zip','Website','Phone','Email'])
    header=['dealerId','Name','street','City','State','Zip','Website','Phone','Email']
    
    for p in pincodes[::-1]:
        try:
            content=json.loads(requests.get(u.format(p)).text)
        except ValueError:
            print "unable to process pincode:"+p
            continue
        #total=int(content['Response']['total'])
        try:
            dealers=content
            test=content[0]['brandSiteName']
        except KeyError:
            print "pincode not found:"+ p
            continue


        print "===pincode===:"+p
        try:
            for x in dealers:
                lw=[x["dealerId"],x["brandSiteName"], x["address"]["street"],x["address"]["city"],x["address"]["province"],x["address"]["postCode"],x['url'], x['contact']['phone']]
                dicti = dict(zip(header, lw))

                scraperwiki.sqlite.save(unique_keys=["dealerId"], data=dicti)

                #print lw
        except KeyError:
            print "###pincode cant be dereferenced:"+ p
            continue


main()
import scraperwiki

import csv,json,requests

data = scraperwiki.scrape('http://ge.tt/api/1/files/9pOLJig/0/blob?download')
pincodes=[]
reader = csv.reader(data.splitlines())

for row in reader:
    pincodes.append(row[0])

print pincodes[1:10]


def main():
    u='http://www.chevrolet.com/bypass/gmna/dealerlocator/services/getdealers?type=PostalCode&format=JSON&x-country=US&x-language=en&x-brand=Chevrolet&postalcode={0}'

 #   f = csv.writer(open("e:\\gigs\\v1CHEVROLET.csv", "ab+"))
#    f.writerow(['Name','street','City','State','Zip','Website','Phone','Email'])
    header=['dealerId','Name','street','City','State','Zip','Website','Phone','Email']
    
    for p in pincodes[::-1]:
        try:
            content=json.loads(requests.get(u.format(p)).text)
        except ValueError:
            print "unable to process pincode:"+p
            continue
        #total=int(content['Response']['total'])
        try:
            dealers=content
            test=content[0]['brandSiteName']
        except KeyError:
            print "pincode not found:"+ p
            continue


        print "===pincode===:"+p
        try:
            for x in dealers:
                lw=[x["dealerId"],x["brandSiteName"], x["address"]["street"],x["address"]["city"],x["address"]["province"],x["address"]["postCode"],x['url'], x['contact']['phone']]
                dicti = dict(zip(header, lw))

                scraperwiki.sqlite.save(unique_keys=["dealerId"], data=dicti)

                #print lw
        except KeyError:
            print "###pincode cant be dereferenced:"+ p
            continue


main()

# Blank Python
import re
import scraperwiki
import urllib2
import scrapemark

result_url="http://www.athletepromotions.com/auto-racer-appearance-booking-agent.php?"
contact_url="http://www.athletepromotions.com/athletes/AJ-Allmendinger-appearance-booking-agent.php?"
first_url="nosearchcache"

def pagefetch(p_url,debug=False):
    html=urllib2.urlopen(p_url).read()
    results=scrapemark.scrape("""{*
              <div id="srp">
              <ul id="results">
               {*
               <li>
                <a><img alt="" src={{[thumbs]}}/> </a>
                <div class="result-info">
                    <h3><a href="speaker.php?{{[links]}}">{{[names]}}</a></h3>
                </div>
               </li>
               *}</ul>
               <p class="pagination">
               <a href="results.php?{{[nxurl]}}">Next</a></p>
              </div>
            *}""",html)
    if debug:
        print "Fetched Names:",len(results['names'])
        print "Fetched Relinks:",len(results['links'])
        print "Current Page:",p_url
        print "Next Page:",results['nxurl']
        return results
    else: return results  

def subfetch(d_url,debug=False):
    html=urllib2.urlopen(d_url).read()
    results=scrapemark.scrape("""{*
             <h1>{{name}}</h1>
             <div class="topics contactinfo">
                <h3>Contact Information</h3>
                <ul><li>phone:{{phone}}</li>
                    <li>email: <a class="emailobf">{{bmail|html}}</a></li>
                    <li>website:<a href="{{website}}"></a></li>
                    <li>{{address|html}}</li>
                </ul>
            </div>
            *}""",html)
    results['email']=emailize(results['bmail'],debug)
    addr=unilize(results['address'],debug)
    if len(addr)==4:
        results['company']=addr[0]
        results['street']=addr[1]
        results['city']=addr[2]
        results['country']=addr[3]
    elif len(addr)==3:
        results['company']="Unknown"
        results['street']=addr[0]
        results['city']=addr[1]
        results['country']=addr[2]  
    elif len(addr)==5: # Probably an australian address
        results['company']=addr[0]
        results['street']=addr[2]
        results['city']=addr[3]
        results['country']=addr[4] 
    else:
        print "Address parsing error!"
        return results      
    if debug:
        print "Fetched Names:",results['name']
        print "Fetched Phone:",results['phone']
        print "Fetched Email:",results['email']
        print "Fetched Website:",results['website']
        print "Fetched Company:",results['company']
        print "Fetched Street:",results['street']  
        print "Fetched City:",results['city']
        print "Fetched Country:",results['country']  
        return results
    else: return results  

def emailize(bmail,debug=False):
    if bmail:
        tmps=re.findall(r'\d+',bmail)
        j=len(tmps)
        email=""
        for i in range(j):
            email+=chr(int(tmps[j-i-1]))
    else:
        email="None"
    if debug:
        print "Encoded Email:",bmail
        print "Decoded Email:",email
        return email
    else: return email  

def unilize(address,debug=False):
    addr=re.split("<br>",address)
    if len(addr)==1:
        addr=re.split("<br/>",address)
    if debug:
        print "Original:",address
        print "Parsed:",addr
        return addr
    else: return addr  


def fullfetch(fullurl,debug=False):
    print "Fetching Page:",fullurl
    pgcache=pagefetch(fullurl,debug)
    next_url=pgcache["nxurl"];
    pgs=len(pgcache['names'])
    print "Speakers List Fetched,Total:",pgs
    for id in range(pgs):
        print "InPage Sequence:",id+1
        print "Extract Contact Info of:",pgcache['names'][id]
        print "URL@:",pgcache['links'][id]
        spkcon=subfetch(contact_url+pgcache['links'][id],debug)
        scraperwiki.sqlite.save(unique_keys=["ID"],data={"ID":id,"Name":spkcon['name'],"Phone":spkcon['phone'],"Email":spkcon['email'],\
                    "Website":spkcon['website'],"Company":spkcon['company'],"Address":spkcon['street'],"City":spkcon['city'],"Country":spkcon['country']})
    print "Speakers Contacts Saved!"
    return next_url


#batch run

def main():
    next_url=fullfetch(result_url+first_url,False)
    for id in range(66):
        next_url=fullfetch(result_url+next_url[0],False)
        print "Just Finished Page:",id+1
    print "All Speakers Contacts Saved!"

main()



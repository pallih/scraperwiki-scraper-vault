#kind of working experiment...

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


# find the number of the last page in the search results, given page (already as a BeautifulSoup item)
def findlastpage(soupedurl):
    coins = soupedurl.findAll(href=re.compile("page"))
    coinurls = set()
    lastpage = ""
    for coin in coins:
        if coin.text=="&nbsp;>>&nbsp;": # "&nbsp;>>&nbsp;" is the text linking to the last page
            lastpageurl = coin["href"]
            lastpage = lastpageurl[lastpageurl.find("&page=",lastpageurl.find("&page=")+1)+6:len(lastpageurl)]
    return lastpage


# DONE
# find all the URLs to the individual coin pages in a given page (already as a BeautifulSoup item)
def findcoinurls(soupedurl):
    coins = soupedurl.findAll(href=re.compile("coin_detail"))
    coinurls = set()
    for coin in coins:
        coinid = coin["href"][coin["href"].find("=")+1:len(coin["href"])]
        coinpath = "http://www.coinproject.com/"+coin["href"]
        coinurls.add((coinid,coinpath))
    return coinurls


def coinref(coinid, coinsoup):

     # inizialize the dictionary/record with the coinID
     coinrecord = { "coinid" : coinid } # dictionaries can be written as key=column and value=value: here, the coinid column has value coinid

     # add the entries related to the issuer's name
     issuer_cell = coinsoup.find(text=re.compile("Issuer :&nbsp;&nbsp;"))
     coinrecord["issuer"]=issuer_cell.next.next.next.next.next.text

     # add the Obverse Description
     #obv_des_cell = coinsoup.find(text=re.compile("Obverse Description :&nbsp;&nbsp;"))
     #coinrecord["obv_des"]=obv_des_cell.next.next.next.next.next.text

     # add the entries related to references
     tags_with_references = coinsoup.findAll(id=re.compile("reference")) # get all the tags with the id attribute including reference
     ref_dictionary = findreference(tags_with_references)
     coinrecord.update(ref_dictionary.items())
     return coinrecord
 
 
def findreference(tags_with_references):
    all_references = set() # empty set that will contain all the strings including all the references that we're going to find
    for id in tags_with_references:
        all_references.add(id.text) #id.text is the text inside the HTML tag
    ref_dictionary = dict()
    # to check: print "All collected references:"+str(all_references)+"\n"
    # now we differentiate between standard and other references
    standard_references=("RIC","Cohen","RSC","SRCV","Gnecchi","BMC","Calico","Hunter") # names of the standard references (for column headers)
    other_references = set() # empty set that will cointain all the references that are not standard
    identified_references = set()
    for reference in all_references:
        for name in standard_references:
            if reference.find(name)>=0:
                ref_dictionary[name] = reference
                identified_references.add(reference)
    # to check: print "Identified references:"+str(identified_references)+"\n"
    other_references = all_references - identified_references
    num = 1 # just a counter that will be used for the headers of other references
    # to check: print "Other references:"+str(other_references)+"\n"
    for other_reference in other_references:
        other_ref_num = "other_ref_"+str(num)
        ref_dictionary[other_ref_num] = other_reference # in the column with name other_ref_N, we add the text of the Nth reference
        num = num +1 # incrementing the counter, in case there are severeal other references
    return ref_dictionary

last = int(findlastpage(BeautifulSoup(scraperwiki.scrape("http://www.coinproject.com/search_emperor.php?emp=Gordian-III&city=&type=3&page=1"))))

for i in range(1, last):
    pagina = "http://www.coinproject.com/search_emperor.php?emp=Gordian-III&city=&type=3&page="+str(i)
    index = scraperwiki.scrape(pagina)
    coinurls = findcoinurls(BeautifulSoup(index))
    for coin in coinurls:
        coinrecord = coinref(coin[0], BeautifulSoup(scraperwiki.scrape(coin[1])))
        scraperwiki.datastore.save(["coinid"], coinrecord) # save the record one by one


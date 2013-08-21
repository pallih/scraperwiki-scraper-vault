import scraperwiki
import scraperwiki.metadata
import urllib2
import re
import pygooglechart
from collections import defaultdict


# To do: 
#   A 3rd table applying to the choices
#   Are the questions always paired the same?
#   What analyses can we do regarding consistencies?  (Principle componentwise)


choices = set()  # record this set in case we want to hard code it
def OutputChoices():
    for choice in choices:
        print '\t"%s":"%s",' % (choice, choice[:10])
    
    
def ParseRow(row):
    drow = dict(re.findall('<td class="([^"]*)">\s*<p>(.*?)</p>', row))  # turn pairs into a dict
    choices.add(drow["Question1"])
    choices.add(drow["Question2"])
    assert drow["CutChoice"] in (drow["Question1"], drow["Question2"])
    # could encode the choices into numbers out of 50
    return drow


def MakeAgePie():
    ages = defaultdict(int)
    for ddrow in scraperwiki.datastore.retrieve({"Age":None}):
        age = ddrow["data"]["Age"]
        ages[age] += 1
    print ages
    chart = pygooglechart.PieChart3D(350, 150, colours=["55CC00", "990033"])
    chart.add_data(ages.values())
    chart.set_pie_labels(ages.keys())
    chart.set_title("Age")
    scraperwiki.metadata.save("chart", chart.get_url())

                   
def ParsePage(count):
    url = "http://chopornot.channel4.com/rawdata.php?count=%d" % count
    b = urllib2.urlopen(url).read()
    rows = re.findall('(?s)<tr>\s*<td class="rank">.*?</tr>', b)

    ranks = set()  # used to avoid too many duplicate saves of users
    
    # slow operation!
    for row in rows:
        drow = ParseRow(row)
        rank = drow["rank"]

        # add in person table
        if rank not in ranks:
            dperson = { "rank":rank, "Age":drow["Age"], "Family":drow["Family"], "question":drow["question"], "sex":drow["sex"] }
            scraperwiki.datastore.save(unique_keys=["rank"], data=dperson)
            ranks.add(rank)
            
        # add in choice table
        dchop = { "rank":rank, "Question1":drow["Question1"], "Question2":drow["Question2"], 
                  "CutChoice":drow["CutChoice"], "timestamp":drow["timestamp"] }
        scraperwiki.datastore.save(unique_keys=["rank", "Question1", "Question2"], data=dchop)
                   
    return len(rows)
        


# Run through till we fail
def Scrape1000():
    page1000 = int(scraperwiki.metadata.get("pagescraped1000", "0"))
    print "Parsing page:", page1000
    lenrows = ParsePage(page1000 * 1000)

    # incomplete page
    if lenrows != 1000:  
        print "Incomplete page at:", page1000
        return False
    scraperwiki.metadata.save("pagescraped1000", str(page1000 + 1))
    if page1000 % 10 == 0:
        MakeAgePie()
    return True

def Q():
    dd = scraperwiki.datastore.retrieve({"Question1":"Cut state pensions. No more golden oldies..."})
    print dd
    for ld in dd:
        d = ld["data"]
        s = d["Question1"] == d["CutChoice"]
        print d["rank"], s
        
    
Q()

    
    
        
# main scraping loop
#while Scrape1000():
#    pass


import scraperwiki
import scraperwiki.metadata
import urllib2
import re
import pygooglechart
from collections import defaultdict


# To do: 
#   A 3rd table applying to the choices
#   Are the questions always paired the same?
#   What analyses can we do regarding consistencies?  (Principle componentwise)


choices = set()  # record this set in case we want to hard code it
def OutputChoices():
    for choice in choices:
        print '\t"%s":"%s",' % (choice, choice[:10])
    
    
def ParseRow(row):
    drow = dict(re.findall('<td class="([^"]*)">\s*<p>(.*?)</p>', row))  # turn pairs into a dict
    choices.add(drow["Question1"])
    choices.add(drow["Question2"])
    assert drow["CutChoice"] in (drow["Question1"], drow["Question2"])
    # could encode the choices into numbers out of 50
    return drow


def MakeAgePie():
    ages = defaultdict(int)
    for ddrow in scraperwiki.datastore.retrieve({"Age":None}):
        age = ddrow["data"]["Age"]
        ages[age] += 1
    print ages
    chart = pygooglechart.PieChart3D(350, 150, colours=["55CC00", "990033"])
    chart.add_data(ages.values())
    chart.set_pie_labels(ages.keys())
    chart.set_title("Age")
    scraperwiki.metadata.save("chart", chart.get_url())

                   
def ParsePage(count):
    url = "http://chopornot.channel4.com/rawdata.php?count=%d" % count
    b = urllib2.urlopen(url).read()
    rows = re.findall('(?s)<tr>\s*<td class="rank">.*?</tr>', b)

    ranks = set()  # used to avoid too many duplicate saves of users
    
    # slow operation!
    for row in rows:
        drow = ParseRow(row)
        rank = drow["rank"]

        # add in person table
        if rank not in ranks:
            dperson = { "rank":rank, "Age":drow["Age"], "Family":drow["Family"], "question":drow["question"], "sex":drow["sex"] }
            scraperwiki.datastore.save(unique_keys=["rank"], data=dperson)
            ranks.add(rank)
            
        # add in choice table
        dchop = { "rank":rank, "Question1":drow["Question1"], "Question2":drow["Question2"], 
                  "CutChoice":drow["CutChoice"], "timestamp":drow["timestamp"] }
        scraperwiki.datastore.save(unique_keys=["rank", "Question1", "Question2"], data=dchop)
                   
    return len(rows)
        


# Run through till we fail
def Scrape1000():
    page1000 = int(scraperwiki.metadata.get("pagescraped1000", "0"))
    print "Parsing page:", page1000
    lenrows = ParsePage(page1000 * 1000)

    # incomplete page
    if lenrows != 1000:  
        print "Incomplete page at:", page1000
        return False
    scraperwiki.metadata.save("pagescraped1000", str(page1000 + 1))
    if page1000 % 10 == 0:
        MakeAgePie()
    return True

def Q():
    dd = scraperwiki.datastore.retrieve({"Question1":"Cut state pensions. No more golden oldies..."})
    print dd
    for ld in dd:
        d = ld["data"]
        s = d["Question1"] == d["CutChoice"]
        print d["rank"], s
        
    
Q()

    
    
        
# main scraping loop
#while Scrape1000():
#    pass


import scraperwiki
import scraperwiki.metadata
import urllib2
import re
import pygooglechart
from collections import defaultdict


# To do: 
#   A 3rd table applying to the choices
#   Are the questions always paired the same?
#   What analyses can we do regarding consistencies?  (Principle componentwise)


choices = set()  # record this set in case we want to hard code it
def OutputChoices():
    for choice in choices:
        print '\t"%s":"%s",' % (choice, choice[:10])
    
    
def ParseRow(row):
    drow = dict(re.findall('<td class="([^"]*)">\s*<p>(.*?)</p>', row))  # turn pairs into a dict
    choices.add(drow["Question1"])
    choices.add(drow["Question2"])
    assert drow["CutChoice"] in (drow["Question1"], drow["Question2"])
    # could encode the choices into numbers out of 50
    return drow


def MakeAgePie():
    ages = defaultdict(int)
    for ddrow in scraperwiki.datastore.retrieve({"Age":None}):
        age = ddrow["data"]["Age"]
        ages[age] += 1
    print ages
    chart = pygooglechart.PieChart3D(350, 150, colours=["55CC00", "990033"])
    chart.add_data(ages.values())
    chart.set_pie_labels(ages.keys())
    chart.set_title("Age")
    scraperwiki.metadata.save("chart", chart.get_url())

                   
def ParsePage(count):
    url = "http://chopornot.channel4.com/rawdata.php?count=%d" % count
    b = urllib2.urlopen(url).read()
    rows = re.findall('(?s)<tr>\s*<td class="rank">.*?</tr>', b)

    ranks = set()  # used to avoid too many duplicate saves of users
    
    # slow operation!
    for row in rows:
        drow = ParseRow(row)
        rank = drow["rank"]

        # add in person table
        if rank not in ranks:
            dperson = { "rank":rank, "Age":drow["Age"], "Family":drow["Family"], "question":drow["question"], "sex":drow["sex"] }
            scraperwiki.datastore.save(unique_keys=["rank"], data=dperson)
            ranks.add(rank)
            
        # add in choice table
        dchop = { "rank":rank, "Question1":drow["Question1"], "Question2":drow["Question2"], 
                  "CutChoice":drow["CutChoice"], "timestamp":drow["timestamp"] }
        scraperwiki.datastore.save(unique_keys=["rank", "Question1", "Question2"], data=dchop)
                   
    return len(rows)
        


# Run through till we fail
def Scrape1000():
    page1000 = int(scraperwiki.metadata.get("pagescraped1000", "0"))
    print "Parsing page:", page1000
    lenrows = ParsePage(page1000 * 1000)

    # incomplete page
    if lenrows != 1000:  
        print "Incomplete page at:", page1000
        return False
    scraperwiki.metadata.save("pagescraped1000", str(page1000 + 1))
    if page1000 % 10 == 0:
        MakeAgePie()
    return True

def Q():
    dd = scraperwiki.datastore.retrieve({"Question1":"Cut state pensions. No more golden oldies..."})
    print dd
    for ld in dd:
        d = ld["data"]
        s = d["Question1"] == d["CutChoice"]
        print d["rank"], s
        
    
Q()

    
    
        
# main scraping loop
#while Scrape1000():
#    pass


import scraperwiki
import scraperwiki.metadata
import urllib2
import re
import pygooglechart
from collections import defaultdict


# To do: 
#   A 3rd table applying to the choices
#   Are the questions always paired the same?
#   What analyses can we do regarding consistencies?  (Principle componentwise)


choices = set()  # record this set in case we want to hard code it
def OutputChoices():
    for choice in choices:
        print '\t"%s":"%s",' % (choice, choice[:10])
    
    
def ParseRow(row):
    drow = dict(re.findall('<td class="([^"]*)">\s*<p>(.*?)</p>', row))  # turn pairs into a dict
    choices.add(drow["Question1"])
    choices.add(drow["Question2"])
    assert drow["CutChoice"] in (drow["Question1"], drow["Question2"])
    # could encode the choices into numbers out of 50
    return drow


def MakeAgePie():
    ages = defaultdict(int)
    for ddrow in scraperwiki.datastore.retrieve({"Age":None}):
        age = ddrow["data"]["Age"]
        ages[age] += 1
    print ages
    chart = pygooglechart.PieChart3D(350, 150, colours=["55CC00", "990033"])
    chart.add_data(ages.values())
    chart.set_pie_labels(ages.keys())
    chart.set_title("Age")
    scraperwiki.metadata.save("chart", chart.get_url())

                   
def ParsePage(count):
    url = "http://chopornot.channel4.com/rawdata.php?count=%d" % count
    b = urllib2.urlopen(url).read()
    rows = re.findall('(?s)<tr>\s*<td class="rank">.*?</tr>', b)

    ranks = set()  # used to avoid too many duplicate saves of users
    
    # slow operation!
    for row in rows:
        drow = ParseRow(row)
        rank = drow["rank"]

        # add in person table
        if rank not in ranks:
            dperson = { "rank":rank, "Age":drow["Age"], "Family":drow["Family"], "question":drow["question"], "sex":drow["sex"] }
            scraperwiki.datastore.save(unique_keys=["rank"], data=dperson)
            ranks.add(rank)
            
        # add in choice table
        dchop = { "rank":rank, "Question1":drow["Question1"], "Question2":drow["Question2"], 
                  "CutChoice":drow["CutChoice"], "timestamp":drow["timestamp"] }
        scraperwiki.datastore.save(unique_keys=["rank", "Question1", "Question2"], data=dchop)
                   
    return len(rows)
        


# Run through till we fail
def Scrape1000():
    page1000 = int(scraperwiki.metadata.get("pagescraped1000", "0"))
    print "Parsing page:", page1000
    lenrows = ParsePage(page1000 * 1000)

    # incomplete page
    if lenrows != 1000:  
        print "Incomplete page at:", page1000
        return False
    scraperwiki.metadata.save("pagescraped1000", str(page1000 + 1))
    if page1000 % 10 == 0:
        MakeAgePie()
    return True

def Q():
    dd = scraperwiki.datastore.retrieve({"Question1":"Cut state pensions. No more golden oldies..."})
    print dd
    for ld in dd:
        d = ld["data"]
        s = d["Question1"] == d["CutChoice"]
        print d["rank"], s
        
    
Q()

    
    
        
# main scraping loop
#while Scrape1000():
#    pass



import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield
import scraperwiki
import cgi
import os
import urllib
import json
import math
import re


emergencynumber = "078987892843"

ADMIN_NUMBERS = frozenset()


def ListMusters(latlng=None):
    res = [ ]
    for muster in scraperwiki.datastore.getData("edmonton-voting-subdivisions"):
        llatlng = muster.get("latlng")
        if not llatlng:
            continue
        if latlng:
            lx, ly  =(llatlng[0] - latlng[0]), (llatlng[1] - latlng[1])
            ld = math.sqrt(lx*lx + ly*ly)
        else:
            ld = 0.0
        shortname = "%s [%s]" % (muster.get("voting_sta"), muster.get("name"))

        #print muster.get("name")
        #print shortname
        res.append((ld, shortname, muster))
    res.sort()
    return res


def LookupAddress(pos):
    a = urllib.urlopen("http://maps.google.com/maps/geo?q=" + urllib.quote(pos)).read()
    v = json.loads(a)
    #print v
    #print v['Placemark']
    #print len(v['Placemark'])
    latlng = v['Placemark'][0]["Point"]["coordinates"]
    return latlng



def HandleMessage(phone, message):
    lmessage = message.split()
    
    if not lmessage:
        yield (phone, "Where are you")

    elif lmessage[0] == "commands":
        yield (phone, "listmusters, mustermessage, updatestatus")
        
    elif lmessage[0] == "listmusters":
        lm = " ".join(lmessage[1:]).strip()
        if lm:
            latlng = LookupAddress(lm)
        else:
            latlng = None
        lsm = ListMusters(latlng)
        if lm:  
            lsm = lsm[:3]  #truncate if we've given an address

        yield (phone, ", ".join([llsm[1]  for llsm in lsm]))
        
    elif message == "Help":
        yield (emergencynumber, "%s asks for help")
        yield (phone, "Help is coming")
    else:
        yield (phone, "I don't understand")


def ParseQuery():
    urlquery = os.getenv("URLQUERY")
    if not urlquery:
        urlquery = "phonenumber=012345&message=listmusters+36+avenue,+edmonton,+canada"
    qs = cgi.parse_qs(urlquery)
    qphone = qs.get("phonenumber")
    qmessage = qs.get("message")
    return (qphone and qphone[0].strip() or None), (qmessage and qmessage[0].strip() or None)


def is_admin(phone_number):
    return phone_number in ADMIN_NUMBERS

def Main(use_test_data=False):
    if use_test_data:
        phone = "012345"# Blank Python

        message = "listmusters"
    else:
        phone, message = ParseQuery()
    if phone:
        for rphone, rmessage in HandleMessage(phone, message):
            print "<p><b>%s</b>: %s</p>" % (rphone, rmessage)
    else:
        print "<p><b>PHONE NUMBER MISSING</b></p>"

Main(use_test_data=False)    

# use the url:
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters
# sources:  http://scraperwiki.com/scrapers/birmingham-leisure-centres/
# http://scraperwikiviews.com/run/mustersms/?phonenumber=012345&message=listmusters+Sutton+Coldfield

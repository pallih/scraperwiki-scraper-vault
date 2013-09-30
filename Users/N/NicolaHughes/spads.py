"""
            spads.py - Phenny Spads Module
            Copyright 2011, Nicola Hughes
            Licensed under the Eiffel Forum License 2.
            
"""
import urllib2
import urllib
import urlparse
import json

def spads(phenny, input):
    """.spads Returns the lastest meeting by a given Special Adviser in Number 10 or a given organisation for a given number
    Current Spads are: Robert Riddell, Flora Coleman, Naweed Khan, Laura Trott, James McGory, Chris Saunders, Richard Reeves, Jonny Oates, Alan Sendorek, Michael Salter, Lena Pietsch, James O'Shaugnessy, Craig Oliver, Polly Mackenzie, Ed Llewellyn, Sean Kemp, Steve Hilton, Tim Colbourne, Tim Chatwin, Gabby Bertin, Martha Varney, Alison Suttie, Rohan Silva, Henry Macrory, Catherine Fall, Andy Coulson, Sean Worth, and Chris White"""
    userinput = input.group(2).split(',')[0]
    try:
        userdate = input.group(2).split(',')[2].strip(' ')
    except:
        userdate = None
    
    try:
        Number = int(input.group(2).split(',')[1].strip(' '))
    except:
        Number = 1
        
    spadapi = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=special_advisers_gifts_and_hospitality&query=SELECT%20%60Name%20of%20Special%20Adviser%60%20FROM%20swdata%20GROUP%20BY%20%60Name%20of%20Special%20Adviser%60'
    jsonspadapi = json.loads(urllib2.urlopen(spadapi).read())
    listspad = []
    for name in jsonspadapi:
        listspad.append(name["Name of Special Adviser"])
    print listspad    
    print userinput
        
    orgapi = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=special_advisers_gifts_and_hospitality&query=SELECT%20%60Name%20of%20Organisation%60%20FROM%20swdata%20GROUP%20BY%20%60Name%20of%20Organisation%60'
    jsonorgapi = json.loads(urllib2.urlopen(orgapi).read())
    listorg = []
    for org in jsonorgapi:
        listorg.append(org["Name of Organisation"])
        
    type = 'jsondict'
    scraper = 'special_advisers_gifts_and_hospitality'
    site = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?'
    
    # Not found anything yet
    userinput_found = False
    
    if userinput in listspad:
        # User input exactly matches a special advisor, do queries etc here
        if userdate != None:
            query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Special Adviser` = "%s" AND `Date of Hospitality` BETWEEN "%s" + "-32" AND "%s" + "-00" ORDER BY `Date of Hospitality` desc' % (userinput, userdate, userdate))
        else:
            query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Special Adviser` = "%s" ORDER BY `Date of Hospitality` desc' % userinput)
    
        params = { 'format': type, 'name': scraper, 'query': query}    
    
        url = site + urllib.urlencode(params)
    
        jsonurl = urllib2.urlopen(url).read()
        swjson = json.loads(jsonurl)
    
        for entry in swjson[:Number]:
            ans = ('On ' + entry["Date of Hospitality"] + ' %s' % userinput + ' got ' + 
                   entry["Type of hospitality received"] + ' from ' + entry["Name of Organisation"])
            phenny.say(ans)
        pass
        # Let program know we've found something
        userinput_found = True
    else:
        # User input not found, check all the orgs
        for org in listorg:
            # Do a case insensitive substring check
            if userinput.lower() in org.lower():
                # Found the org, do queries etc here
                if userdate != None:
                    query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Date of Hospitality` BETWEEN "%s" + "-32" AND "%s" + "-00" AND `Name of Organisation` LIKE  "%%%s%%"  ORDER BY `Date of Hospitality` desc' % (userdate, userdate, userinput))
                else:
                    query = "SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Organisation` LIKE  '%" + userinput + "%' ORDER BY `Date of Hospitality` desc"
                phenny.say(query)
                params = { 'format': type, 'name': scraper, 'query': query}    
    
                url = site + urllib.urlencode(params)
                print url
                jsonurl = urllib2.urlopen(url).read()
                swjson = json.loads(jsonurl)
                
                for entry in swjson[:Number]:
                    ans = ('On ' + entry["Date of Hospitality"] + ' ' + entry["Name of Special Adviser"] + ' got ' + 
                            entry["Type of hospitality received"] + ' from ' + entry["Name of Organisation"])
                    phenny.say(ans)
                pass
                # Let program know we've found something
                userinput_found = True
                # Should not continue checking orgs
                break
    
    if not userinput_found:
        # Didn't find anything, error message
        phenny.say("%s is not a Special Adviser or had not met with one, please try another" % userinput)
        pass

    
        
spads.commands = ["spads"]
spads.priority = 'medium'
spads.example = '.spads name of special adviser OR organisation, number i.e. .spads Andy Coulson, 4 OR .spads BBC, 3'

if __name__ == '__main__':
    print __doc__.strip()
        
    
    """
            spads.py - Phenny Spads Module
            Copyright 2011, Nicola Hughes
            Licensed under the Eiffel Forum License 2.
            
"""
import urllib2
import urllib
import urlparse
import json

def spads(phenny, input):
    """.spads Returns the lastest meeting by a given Special Adviser in Number 10 or a given organisation for a given number
    Current Spads are: Robert Riddell, Flora Coleman, Naweed Khan, Laura Trott, James McGory, Chris Saunders, Richard Reeves, Jonny Oates, Alan Sendorek, Michael Salter, Lena Pietsch, James O'Shaugnessy, Craig Oliver, Polly Mackenzie, Ed Llewellyn, Sean Kemp, Steve Hilton, Tim Colbourne, Tim Chatwin, Gabby Bertin, Martha Varney, Alison Suttie, Rohan Silva, Henry Macrory, Catherine Fall, Andy Coulson, Sean Worth, and Chris White"""
    userinput = input.group(2).split(',')[0]
    try:
        userdate = input.group(2).split(',')[2].strip(' ')
    except:
        userdate = None
    
    try:
        Number = int(input.group(2).split(',')[1].strip(' '))
    except:
        Number = 1
        
    spadapi = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=special_advisers_gifts_and_hospitality&query=SELECT%20%60Name%20of%20Special%20Adviser%60%20FROM%20swdata%20GROUP%20BY%20%60Name%20of%20Special%20Adviser%60'
    jsonspadapi = json.loads(urllib2.urlopen(spadapi).read())
    listspad = []
    for name in jsonspadapi:
        listspad.append(name["Name of Special Adviser"])
    print listspad    
    print userinput
        
    orgapi = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=special_advisers_gifts_and_hospitality&query=SELECT%20%60Name%20of%20Organisation%60%20FROM%20swdata%20GROUP%20BY%20%60Name%20of%20Organisation%60'
    jsonorgapi = json.loads(urllib2.urlopen(orgapi).read())
    listorg = []
    for org in jsonorgapi:
        listorg.append(org["Name of Organisation"])
        
    type = 'jsondict'
    scraper = 'special_advisers_gifts_and_hospitality'
    site = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?'
    
    # Not found anything yet
    userinput_found = False
    
    if userinput in listspad:
        # User input exactly matches a special advisor, do queries etc here
        if userdate != None:
            query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Special Adviser` = "%s" AND `Date of Hospitality` BETWEEN "%s" + "-32" AND "%s" + "-00" ORDER BY `Date of Hospitality` desc' % (userinput, userdate, userdate))
        else:
            query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Special Adviser` = "%s" ORDER BY `Date of Hospitality` desc' % userinput)
    
        params = { 'format': type, 'name': scraper, 'query': query}    
    
        url = site + urllib.urlencode(params)
    
        jsonurl = urllib2.urlopen(url).read()
        swjson = json.loads(jsonurl)
    
        for entry in swjson[:Number]:
            ans = ('On ' + entry["Date of Hospitality"] + ' %s' % userinput + ' got ' + 
                   entry["Type of hospitality received"] + ' from ' + entry["Name of Organisation"])
            phenny.say(ans)
        pass
        # Let program know we've found something
        userinput_found = True
    else:
        # User input not found, check all the orgs
        for org in listorg:
            # Do a case insensitive substring check
            if userinput.lower() in org.lower():
                # Found the org, do queries etc here
                if userdate != None:
                    query = ('SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Date of Hospitality` BETWEEN "%s" + "-32" AND "%s" + "-00" AND `Name of Organisation` LIKE  "%%%s%%"  ORDER BY `Date of Hospitality` desc' % (userdate, userdate, userinput))
                else:
                    query = "SELECT `Name of Special Adviser`, `Type of hospitality received`, `Name of Organisation`, `Date of Hospitality` FROM swdata WHERE `Name of Organisation` LIKE  '%" + userinput + "%' ORDER BY `Date of Hospitality` desc"
                phenny.say(query)
                params = { 'format': type, 'name': scraper, 'query': query}    
    
                url = site + urllib.urlencode(params)
                print url
                jsonurl = urllib2.urlopen(url).read()
                swjson = json.loads(jsonurl)
                
                for entry in swjson[:Number]:
                    ans = ('On ' + entry["Date of Hospitality"] + ' ' + entry["Name of Special Adviser"] + ' got ' + 
                            entry["Type of hospitality received"] + ' from ' + entry["Name of Organisation"])
                    phenny.say(ans)
                pass
                # Let program know we've found something
                userinput_found = True
                # Should not continue checking orgs
                break
    
    if not userinput_found:
        # Didn't find anything, error message
        phenny.say("%s is not a Special Adviser or had not met with one, please try another" % userinput)
        pass

    
        
spads.commands = ["spads"]
spads.priority = 'medium'
spads.example = '.spads name of special adviser OR organisation, number i.e. .spads Andy Coulson, 4 OR .spads BBC, 3'

if __name__ == '__main__':
    print __doc__.strip()
        
    
    
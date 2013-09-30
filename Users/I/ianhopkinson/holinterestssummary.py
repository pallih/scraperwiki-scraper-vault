# Viewer to show some brief summary data on the House of Lords interests data
# TODO: Sort output so that categories appear in neat order

import scraperwiki
from random import randrange

sourcescraper = 'houseoflordsinterests'

scraperwiki.sqlite.attach(sourcescraper)

#Category descriptions
CategoriesDict={'1':'Category 1: Directorships',
 '2':'Category 2: Remunerated employment, office, profession etc.',
 '3':'Category 3: Clients',
 '4a':'Category 4: Shareholdings (a)',
 '4b':'Category 4: Shareholdings (b)',
 '5':'Category 5: Land and property',
 '6':'Category 6: Sponsorship',
 '7':'Category 7: Overseas visits',
 '8':'Category 8: Gifts, benefits and hospitality',
 '9':'Category 9: Miscellaneous financial interests',
 '10a':'Category 10: Non-financial interests (a)',
 '10b':'Category 10: Non-financial interests (b)',
 '10c':'Category 10: Non-financial interests (c)',
 '10d':'Category 10: Non-financial interests (d)',
 '10e':'Category 10: Non-financial interests (e)',
 '11':'Nil',
 'None':'None'}

#Header
print "<h1>House of Lords, register of member's interests</h1>"

#Count the total number of Lords
Lords = scraperwiki.sqlite.select(           
    ''' Distinct Name from houseoflordsinterests.swdata'''
)

nLords=len(Lords)

print "There are %d Lords in the list of members interests" %nLords



#Count the number of entries in each category
data = scraperwiki.sqlite.select(           
    '''InterestCategory, count(*) from houseoflordsinterests.swdata group by InterestCategory'''
)

print "<table>"           
print "<tr><th>Category</th><th>Number of entries</th>"
for d in data:
    print "<tr>"
    #print type(d["InterestCategory"])
    print "<td>", CategoriesDict[str(d["InterestCategory"])], "</td>"
    #print "<td>", d["InterestCategory"], "</td>"
    print "<td>", d["count(*)"], "</td>"
    print "</tr>"
print "</table>"

#Display a random Lord's entries
print "<h2>The entries of a randomly selected Lord</h2>"

LordIndex=randrange(nLords)
LordName=Lords[LordIndex]["Name"]

print "The randomly selected Lord is %s" % LordName

LordEntry = scraperwiki.sqlite.select(           
    '''* from houseoflordsinterests.swdata where Name=? group by InterestCategory''',LordName
)

print "<table>"           
print "<tr><th>Interest Category</th><th>interest description</th>"
for d in LordEntry:
     print "<tr>"
     print "<td>", d["InterestCategory"], "</td>"
     print "<td>", d["InterestDescription"], "</td>"
     print "</tr>"
print "</table>"
    
# Viewer to show some brief summary data on the House of Lords interests data
# TODO: Sort output so that categories appear in neat order

import scraperwiki
from random import randrange

sourcescraper = 'houseoflordsinterests'

scraperwiki.sqlite.attach(sourcescraper)

#Category descriptions
CategoriesDict={'1':'Category 1: Directorships',
 '2':'Category 2: Remunerated employment, office, profession etc.',
 '3':'Category 3: Clients',
 '4a':'Category 4: Shareholdings (a)',
 '4b':'Category 4: Shareholdings (b)',
 '5':'Category 5: Land and property',
 '6':'Category 6: Sponsorship',
 '7':'Category 7: Overseas visits',
 '8':'Category 8: Gifts, benefits and hospitality',
 '9':'Category 9: Miscellaneous financial interests',
 '10a':'Category 10: Non-financial interests (a)',
 '10b':'Category 10: Non-financial interests (b)',
 '10c':'Category 10: Non-financial interests (c)',
 '10d':'Category 10: Non-financial interests (d)',
 '10e':'Category 10: Non-financial interests (e)',
 '11':'Nil',
 'None':'None'}

#Header
print "<h1>House of Lords, register of member's interests</h1>"

#Count the total number of Lords
Lords = scraperwiki.sqlite.select(           
    ''' Distinct Name from houseoflordsinterests.swdata'''
)

nLords=len(Lords)

print "There are %d Lords in the list of members interests" %nLords



#Count the number of entries in each category
data = scraperwiki.sqlite.select(           
    '''InterestCategory, count(*) from houseoflordsinterests.swdata group by InterestCategory'''
)

print "<table>"           
print "<tr><th>Category</th><th>Number of entries</th>"
for d in data:
    print "<tr>"
    #print type(d["InterestCategory"])
    print "<td>", CategoriesDict[str(d["InterestCategory"])], "</td>"
    #print "<td>", d["InterestCategory"], "</td>"
    print "<td>", d["count(*)"], "</td>"
    print "</tr>"
print "</table>"

#Display a random Lord's entries
print "<h2>The entries of a randomly selected Lord</h2>"

LordIndex=randrange(nLords)
LordName=Lords[LordIndex]["Name"]

print "The randomly selected Lord is %s" % LordName

LordEntry = scraperwiki.sqlite.select(           
    '''* from houseoflordsinterests.swdata where Name=? group by InterestCategory''',LordName
)

print "<table>"           
print "<tr><th>Interest Category</th><th>interest description</th>"
for d in LordEntry:
     print "<tr>"
     print "<td>", d["InterestCategory"], "</td>"
     print "<td>", d["InterestDescription"], "</td>"
     print "</tr>"
print "</table>"
    

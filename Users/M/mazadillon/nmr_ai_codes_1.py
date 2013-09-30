import scraperwiki
sourcescraper = 'nmr_ai_codes'
scraperwiki.sqlite.attach(sourcescraper)

count = scraperwiki.sqlite.select( 'count(*) FROM swdata')
print 'Database contains '+str(count[0]['count(*)'])+' bulls<br />'
print '<form action="https://views.scraperwiki.com/run/nmr_ai_codes_1/" method="get">'
print '<fieldset><legend>Bull Search</legend>'
print '<label for="hbn">Herd Book Number</label> <input type="text" name="hbn" id="hbn" /><br />'
print 'Short Name <input type="text" name="shortname" /><br />'
print 'Name <input type="text" name="name" /><br />'
print 'AI Code <input type="text" name="code" /><br />'
print 'Breed Number <input type="text" name="breed" /><br />'
print 'Country Code <input type="text" name="country" /><br />'
print '<input type="submit" value="Search" /></fieldset></form>'

get = scraperwiki.utils.GET()
search_keys = ['hbn','shortname','name','code','breed','country']
if len(get) > 0:
    key = get.keys()[0]
    if key in search_keys:
        data = scraperwiki.sqlite.select( '* from swdata where '+key+' like "%'+get[key]+'%"')
        if len(data) > 0:
            print 'Search results for "'+get[key]+'" in '+key+'<br />'
            print '<table border="1"><tr><th>AI Code</th><th>Name</th><th>Country</th><th>Breed</th><th>HBN</th><th>Short Name</th></tr>'
            for line in data:
                print '<tr>'
                for i in line:
                    print '<td>'+line[i]+'</td>'
                print '</tr>'
            print '</table>'
        else:
            print 'No results'
import scraperwiki
sourcescraper = 'nmr_ai_codes'
scraperwiki.sqlite.attach(sourcescraper)

count = scraperwiki.sqlite.select( 'count(*) FROM swdata')
print 'Database contains '+str(count[0]['count(*)'])+' bulls<br />'
print '<form action="https://views.scraperwiki.com/run/nmr_ai_codes_1/" method="get">'
print '<fieldset><legend>Bull Search</legend>'
print '<label for="hbn">Herd Book Number</label> <input type="text" name="hbn" id="hbn" /><br />'
print 'Short Name <input type="text" name="shortname" /><br />'
print 'Name <input type="text" name="name" /><br />'
print 'AI Code <input type="text" name="code" /><br />'
print 'Breed Number <input type="text" name="breed" /><br />'
print 'Country Code <input type="text" name="country" /><br />'
print '<input type="submit" value="Search" /></fieldset></form>'

get = scraperwiki.utils.GET()
search_keys = ['hbn','shortname','name','code','breed','country']
if len(get) > 0:
    key = get.keys()[0]
    if key in search_keys:
        data = scraperwiki.sqlite.select( '* from swdata where '+key+' like "%'+get[key]+'%"')
        if len(data) > 0:
            print 'Search results for "'+get[key]+'" in '+key+'<br />'
            print '<table border="1"><tr><th>AI Code</th><th>Name</th><th>Country</th><th>Breed</th><th>HBN</th><th>Short Name</th></tr>'
            for line in data:
                print '<tr>'
                for i in line:
                    print '<td>'+line[i]+'</td>'
                print '</tr>'
            print '</table>'
        else:
            print 'No results'

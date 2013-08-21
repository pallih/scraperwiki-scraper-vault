import os, urlparse, cgi
urlquery = os.getenv('URLQUERY')

if urlquery:
     querydata = urlparse.parse_qsl(urlquery);
     for pair in querydata:
        if pair[0] == "js" and pair[1] == "jquery.js":
            print 'js-sourcecode'
            exit(0)

import urllib2, json, re
import yaml

url = "https://api.scraperwiki.com/api/1.0/scraper/search?format=jsondict&maxrows=200&searchquery=nuug-postliste-endyaml"
json_data = json.load(urllib2.urlopen(url))
print '''<html>
<head>
<link rel="stylesheet" href="https://views.scraperwiki.com/run/jquery-tablesorter/?file=style-blue.css" type="text/css" />
<script type="text/javascript" src="https://views.scraperwiki.com/run/jquery-tablesorter/?file=jquery-1-4-2-min.js"></script>
<script type="text/javascript" src="https://views.scraperwiki.com/run/jquery-tablesorter/?file=jquery.tablesorter.2-0-5.min.js"></script>
'''

print '''</head><body>
<p>This view lists scrapers with yaml-combatible comments (containing the string "nuug-postliste-endyaml" like the following in their description
<pre>
&lt;!-- nuug-postliste-yaml --&gt;
YAML-tagger:&lt;br&gt;
Type: kommune&lt;br&gt;
Status: finished&lt;br&gt;
Name: Lillesteinsmyr kommune&lt;br&gt;
Format: PDF&lt;br&gt;
Datatype: ePhorte&lt;br&gt;
Run: daily&lt;br&gt;
&lt;!-- nuug-postliste-endyaml --&gt;
</pre></p>
<table id="myTable" class="tablesorter">'''

print '<thead><tr><th>Name</th><th>type</th><th>status</th><th>schedule</th><th>format</th><th>datatype</th><th>created</th><th>URL</th></tr></thead><tbody>'
counter = {}
for scraper in json_data:
    #print "<!-- %s -->" % cgi.escape("%s" % scraper)
    comment = re.findall(r'<!-- nuug-postliste-yaml -->(.*)<!-- nuug-postliste-endyaml -->', 
                    scraper['description'], re.DOTALL)
    assert len(comment) == 1
    data = yaml.load(comment[0].strip().replace('<br>',''))

    if data['Type'] in counter:
        counter[data['Type']] = counter[data['Type']] + 1
    else:
        counter[data['Type']] = 1

    if  'Run' in data: Run = data['Run']
    else: Run = 'unknown'

    if  'Format' in data: Format = data['Format']
    else: Format = 'unknown'

    if  'Datatype' in data: Type = data['Datatype']
    else: Type = 'unknown'


    print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="https://scraperwiki.com/scrapers/%s/">URL</a></td></tr>' % \
    (data['Name'],data['Type'],data['Status'], Run, Format, Type, scraper['created'], scraper['short_name'])
print '''</tbody></table><table id="myTable2" class="tablesorter"><thead><tr><th>type</th><th>count</th></tr></thead><tbody>'''

for key in counter:
    print '<tr><td>%s</td><td>%d</td></tr>' % (key, counter[key])
print '</tbody></table>'

num_kommune = float(429)
num_fylke = float(19)
print '<table class="tablesorter"><thead><tr><td>Type</td><td>Prosent</td></tr></thead><tbody>'
try:
    print "<tr><td>Kommune</td><td>%.2f%% (%d av %d)</td></tr>" % \
    ((float(counter['kommune'])/float(num_kommune))*100, counter['kommune'], num_kommune)
except KeyError: pass
try:
    print "<tr><td>Fylkeskommune</td><td>%.2f%% (%d av %d)</td></tr>" % \
    ((float(counter['fylkeskommune'])/float(num_fylke))*100, counter['fylkeskommune'], num_fylke)
except KeyError: pass
#http://stackoverflow.com/questions/7561026/jquery-tablesorter-parser-for-datetime-in-mm-dd-yyyy-hhmi-am-format
#http://stackoverflow.com/questions/1707840/date-sorting-problem-with-jquery-tablesorter
print '''</tbody></table>
<script type="text/javascript">
    $(document).ready(function() 
        { 
            $("#myTable").tablesorter(
                {
                    debug: true,
                    headers:
                    {  
                        6 : { sorter: "text"  },
                        7: {sorter: false}
                    }
                }
            );
            //$("#myTable2").tablesorter(); 
        } 
    );

$(function() {

});


</script>
</body></html>'''
import scraperwiki
scraperwiki.sqlite.attach("bromley_parkrun")

data = scraperwiki.sqlite.select(
    '''* from bromley_parkrun.races 
    order by racename,time '''
)
oldracename = ""

print """
<html>
<style>
body { font: 75%/2 Arial,Helvetica,sans-serif;color:#9E0051;margin:0; }
table { margin-bottom:1.5em; font-size:1.2em }
table td, table th { text-align:left; border: solid 1px #ccc; padding:5px; border-collapse:collapse; }
table th { background-color:#9E0051;color:#fff;font-weight:normal; }
table td { color:#666; }
table th:first-child { width:180px; }
h1 { font-size:2em; margin:0 0 1em 0; background-color:#FFdddd; padding:0.5em}
h2 { font-size:1.5em; margin:0.5em 0; color:#333; }
h3 { font-size:1.3em; margin:0 0 0.2em 0;}
a,a:visited,a:active {color:#66f;}
.main { margin: 0.5em; }
#scraperwikipane { display:none !important; }
</style>
<body>
"""
#print "<h1>Beckenham Running Club</h1>"

print "<div class=""main"">"
#print "<h2>This weeks parkrun results</h2>"

for d in data:   
    if d["racename"] <> oldracename:       
        if oldracename <> "":
            print "</table>"        
        print "<h3>", d["racename"], "</h3>"
        print "<table border='0' cellpadding='0' cellspacing='0'>"
        print "<tr><th class=""name"">Name</th><th>Position</th><th>Time</th><th>Age Grade</th><th>Note</th><th>Runs</th><th>Athlete History</th>"    
    print "<tr>"
    print "<td>", d["name"], "</td>"
    print "<td>", d["position"], "</td>"
    print "<td>", d["time"], "</td>"
    print "<td>", d["agegrade"], "</td>"
    print "<td>", d["note"], "</td>"
    print "<td>", d["totalruns"], "</td>"    
    print "<td><a target='_athlete' href='http://www.parkrun.org.uk/athleteresultshistory?athleteNumber=",d["id"],"'>Link</a></td>"
    print "</tr>"
    oldracename = d["racename"]
print "</table></body></html>"


# Blank Python
import scraperwiki
import re, ast, cgi, os
import datetime

sourcescraper = 'imdb_ratings_spectrum'
scraperwiki.sqlite.attach(sourcescraper, "imdb")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

DEBUG = "2013-01-06"


def main():
    now = datetime.datetime.utcnow()
    outputHtml(outputNavigation, outputContent)




def outputContent():
    dataset = scraperwiki.sqlite.select("* from imdb.films where id=?", str(_params_.get("id")))
    if not dataset: return
    film = dataset[0]
    spectrum = ast.literal_eval(film["spectrum"])
    print "<caption><h4>Modified at %s</h4> <h5>Updated at %s</h5></caption>" % (film["modifiedDate"], film["updateTime"][:16])
    for key, item in sorted(spectrum.items(), key=lambda x: x[1]["index"]):
        for hist in item["history"]:
            print "<tr class='history'> <td></td>  <td></td>  <td>%s</td>  <td>%s</td>  <td>%s</td> </tr>" % hist
        changed = item["date"]==film["modifiedDate"] and 'changed' or ''
        print "<tr class='%s'> <td>%s</td>  <td>%s</td>  <td>%s</td>  <td class='%s'>%s</td>  <td>%s</td> </tr>" % (
            changed, key, item["votes"], item["vstart"], changed, item["value"], item["date"]
        )




def outputNavigation():
    active = str( datetime.datetime.utcnow() + datetime.timedelta(days=-5) )
    dataset = scraperwiki.sqlite.select("id, title, rank, year, modifiedDate from imdb.films where updateTime>? order by rank limit 30", active)
    for data in dataset:
        data["latest"] = data["modifiedDate"]>DEBUG
        print "<li id='tt%(id)s' class='latest%(latest)s'><a href='?id=%(id)s'>%(rank)s. %(title)s (%(year)s)</a></li>" % data




def outputHtml(navigation, content):
    print """
<html><head>
    <title>IMDb Ratings Spectrum</title>
    <style>
        * {font-family:courier new;}
        ul {font-size:0.6em}
        td {font-size:0.84em}
        body {width:900px}
        div#nav  {display:inline-block; vertical-align:top; width:270px; margin:0 26px 0 4px; padding:12px 0 24px 0; border-right:1px solid #dddddd}
        div#main {display:inline-block; vertical-align:top; width:500px;}
        ul {list-style:none; margin:0; padding:0;}
        li a{display:block; padding:5px 0 5px 8px; color:black; border:1px solid transparent; text-decoration:none}
        li#tt%s a{border:1px solid #bbbbbb; color:#aa2222; font-weight:bold;}
        caption {padding:12px 0;}
        h4, h5 {margin: 6px 0}
        tr.changed {color:red}
        td.changed {font-weight:bold}
        li.latestTrue {background:#ffccff}
        tr.history {background:white; color:#999999}
        table {border-collapse:collapse; background:#f9f9f9}
    </style>
</head>
<body>
<div id="nav"><ul>
""" % (_params_.get("id"))

    navigation()
    print "</ul></div> <div id='main'><table border='1' cellpadding='5'>"
    content()
    print"</table></div></body></html>"


#######
main()
# Blank Python
import scraperwiki
import re, ast, cgi, os
import datetime

sourcescraper = 'imdb_ratings_spectrum'
scraperwiki.sqlite.attach(sourcescraper, "imdb")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

DEBUG = "2013-01-06"


def main():
    now = datetime.datetime.utcnow()
    outputHtml(outputNavigation, outputContent)




def outputContent():
    dataset = scraperwiki.sqlite.select("* from imdb.films where id=?", str(_params_.get("id")))
    if not dataset: return
    film = dataset[0]
    spectrum = ast.literal_eval(film["spectrum"])
    print "<caption><h4>Modified at %s</h4> <h5>Updated at %s</h5></caption>" % (film["modifiedDate"], film["updateTime"][:16])
    for key, item in sorted(spectrum.items(), key=lambda x: x[1]["index"]):
        for hist in item["history"]:
            print "<tr class='history'> <td></td>  <td></td>  <td>%s</td>  <td>%s</td>  <td>%s</td> </tr>" % hist
        changed = item["date"]==film["modifiedDate"] and 'changed' or ''
        print "<tr class='%s'> <td>%s</td>  <td>%s</td>  <td>%s</td>  <td class='%s'>%s</td>  <td>%s</td> </tr>" % (
            changed, key, item["votes"], item["vstart"], changed, item["value"], item["date"]
        )




def outputNavigation():
    active = str( datetime.datetime.utcnow() + datetime.timedelta(days=-5) )
    dataset = scraperwiki.sqlite.select("id, title, rank, year, modifiedDate from imdb.films where updateTime>? order by rank limit 30", active)
    for data in dataset:
        data["latest"] = data["modifiedDate"]>DEBUG
        print "<li id='tt%(id)s' class='latest%(latest)s'><a href='?id=%(id)s'>%(rank)s. %(title)s (%(year)s)</a></li>" % data




def outputHtml(navigation, content):
    print """
<html><head>
    <title>IMDb Ratings Spectrum</title>
    <style>
        * {font-family:courier new;}
        ul {font-size:0.6em}
        td {font-size:0.84em}
        body {width:900px}
        div#nav  {display:inline-block; vertical-align:top; width:270px; margin:0 26px 0 4px; padding:12px 0 24px 0; border-right:1px solid #dddddd}
        div#main {display:inline-block; vertical-align:top; width:500px;}
        ul {list-style:none; margin:0; padding:0;}
        li a{display:block; padding:5px 0 5px 8px; color:black; border:1px solid transparent; text-decoration:none}
        li#tt%s a{border:1px solid #bbbbbb; color:#aa2222; font-weight:bold;}
        caption {padding:12px 0;}
        h4, h5 {margin: 6px 0}
        tr.changed {color:red}
        td.changed {font-weight:bold}
        li.latestTrue {background:#ffccff}
        tr.history {background:white; color:#999999}
        table {border-collapse:collapse; background:#f9f9f9}
    </style>
</head>
<body>
<div id="nav"><ul>
""" % (_params_.get("id"))

    navigation()
    print "</ul></div> <div id='main'><table border='1' cellpadding='5'>"
    content()
    print"</table></div></body></html>"


#######
main()

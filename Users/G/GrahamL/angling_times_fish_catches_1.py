import scraperwiki
scraperwiki.sqlite.attach("angling_times_fish_catches")

data = scraperwiki.sqlite.select('''* from angling_times_fish_catches.swdata 
    order by Timestamp asc limit 20'''
)
print "<html>"
print "<head>"
print "<link href='http://fonts.googleapis.com/css?family=PT+Sans|Bitter:400,700' rel='stylesheet' type='text/css'/>"
print "<style>a#scraperwikipane{display:none!important;}div#scraperwikipane{display:none!important;}a:hover {color:#3d85c6;} li{font-family:PT Sans, arial;color:#555555; font-size:12px; line-height:1.6;} .news_source {font-size:10px;font-family:arial,helvetica;color:#555555;} .news_source a {color:#555555;}</style>"
print "</head>"
print "<body style='margin:0;padding:0;color:#555555;'>"
print "<ul style='list-style-type:square; margin-left:-20px;'>"
for d in data:
    print "<li><a target='_blank' style='color:#555555;' href='", d["URL"] +"'>",d["Headline"], "</a>"
print "</ul>"
print "<div class='news_source'>Source: <a target='_blank' href='http://www.gofishing.co.uk/'>Angling Times</a></div>"
import scraperwiki
scraperwiki.sqlite.attach("angling_times_fish_catches")

data = scraperwiki.sqlite.select('''* from angling_times_fish_catches.swdata 
    order by Timestamp asc limit 20'''
)
print "<html>"
print "<head>"
print "<link href='http://fonts.googleapis.com/css?family=PT+Sans|Bitter:400,700' rel='stylesheet' type='text/css'/>"
print "<style>a#scraperwikipane{display:none!important;}div#scraperwikipane{display:none!important;}a:hover {color:#3d85c6;} li{font-family:PT Sans, arial;color:#555555; font-size:12px; line-height:1.6;} .news_source {font-size:10px;font-family:arial,helvetica;color:#555555;} .news_source a {color:#555555;}</style>"
print "</head>"
print "<body style='margin:0;padding:0;color:#555555;'>"
print "<ul style='list-style-type:square; margin-left:-20px;'>"
for d in data:
    print "<li><a target='_blank' style='color:#555555;' href='", d["URL"] +"'>",d["Headline"], "</a>"
print "</ul>"
print "<div class='news_source'>Source: <a target='_blank' href='http://www.gofishing.co.uk/'>Angling Times</a></div>"

import scraperwiki

# Blank Python
sourcescraper = 'rss_1'

scraperwiki.sqlite.attach("rss_1")
data = scraperwiki.sqlite.select("* from rss_1.swdata order by rating desc")

print """
<head>
<style type="text/css">
#table-2 {
    border: 1px solid #eee;
    background-color: #f2f2f2;
        width: 100%;
    border-radius: 6px;
    -webkit-border-radius: 6px;
    -moz-border-radius: 6px;
}
#table-2 td, #table-2 th {
    padding: 5px;
    color: #333;
}
#table-2 thead {
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
    padding: .2em 0 .2em .5em;
    text-align: center;
    color: #4B4B4B;
    background-color: #C8C8C8;
    background-image: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#e3e3e3), color-stop(.6,#B3B3B3));
    background-image: -moz-linear-gradient(top, #D6D6D6, #B0B0B0, #B3B3B3 90%);
    border-bottom: solid 1px #999;
}
#table-2 th {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 17px;
    line-height: 20px;
    font-style: normal;
    font-weight: normal;
    text-align: center;
    text-shadow: white 1px 1px 1px;
}
#table-2 td {
    line-height: 20px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 14px;
    border-bottom: 0px solid #fff;
    border-top: 0px solid #fff;
}
</style>
</head>
"""

print "<body>"
print """<table id="table-2">"""
print "<tr><th>Poster</th><th>Title</th><th>Rating</th><th>Genre</th><th>Description</th></tr>"
for d in data:
    rating = float(d["rating"])
    bg_color = "#FFFFF5"
    if (rating < 5):
        bg_color = "#FAE6E6"
    if (rating >= 7):
        bg_color = "#E6FAE6"        
    
    print "<tr style='background-color:", bg_color ,"'>"
    print "<td><a href='",d['imdb'], "'> <img width='100px' src='", d["img"], "'/></a></td>"

    print "<td>", d["title"],"<strong>", d["year"], "</strong><br/>"
    if d["trailer"]:
        print "<a target='blank' href='", d["trailer"], "'>Trailer</a><br/>"
    print "<a href='", d["url"], "'>Download</a></td>"

    print "<td><strong>", d["rating"], "</strong></td>"
    print "<td>", d["genre"], "</td>"
    print "<td>", d["description"], "</td>"

    print "</tr>"
print "</table>"
print "</body>"
import scraperwiki

# Blank Python
sourcescraper = 'rss_1'

scraperwiki.sqlite.attach("rss_1")
data = scraperwiki.sqlite.select("* from rss_1.swdata order by rating desc")

print """
<head>
<style type="text/css">
#table-2 {
    border: 1px solid #eee;
    background-color: #f2f2f2;
        width: 100%;
    border-radius: 6px;
    -webkit-border-radius: 6px;
    -moz-border-radius: 6px;
}
#table-2 td, #table-2 th {
    padding: 5px;
    color: #333;
}
#table-2 thead {
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
    padding: .2em 0 .2em .5em;
    text-align: center;
    color: #4B4B4B;
    background-color: #C8C8C8;
    background-image: -webkit-gradient(linear, left top, left bottom, from(#f2f2f2), to(#e3e3e3), color-stop(.6,#B3B3B3));
    background-image: -moz-linear-gradient(top, #D6D6D6, #B0B0B0, #B3B3B3 90%);
    border-bottom: solid 1px #999;
}
#table-2 th {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 17px;
    line-height: 20px;
    font-style: normal;
    font-weight: normal;
    text-align: center;
    text-shadow: white 1px 1px 1px;
}
#table-2 td {
    line-height: 20px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 14px;
    border-bottom: 0px solid #fff;
    border-top: 0px solid #fff;
}
</style>
</head>
"""

print "<body>"
print """<table id="table-2">"""
print "<tr><th>Poster</th><th>Title</th><th>Rating</th><th>Genre</th><th>Description</th></tr>"
for d in data:
    rating = float(d["rating"])
    bg_color = "#FFFFF5"
    if (rating < 5):
        bg_color = "#FAE6E6"
    if (rating >= 7):
        bg_color = "#E6FAE6"        
    
    print "<tr style='background-color:", bg_color ,"'>"
    print "<td><a href='",d['imdb'], "'> <img width='100px' src='", d["img"], "'/></a></td>"

    print "<td>", d["title"],"<strong>", d["year"], "</strong><br/>"
    if d["trailer"]:
        print "<a target='blank' href='", d["trailer"], "'>Trailer</a><br/>"
    print "<a href='", d["url"], "'>Download</a></td>"

    print "<td><strong>", d["rating"], "</strong></td>"
    print "<td>", d["genre"], "</td>"
    print "<td>", d["description"], "</td>"

    print "</tr>"
print "</table>"
print "</body>"

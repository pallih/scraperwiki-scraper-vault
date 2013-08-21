import scraperwiki
import re
import collections
from datetime import date

sourcescraper = 'waterside_series_results'

params = scraperwiki.utils.GET()

show = 'summary' if 'show' not in params else params['show']
race = None if 'race' not in params else params['race']
club = None if 'club' not in params else params['club']
name = None if 'name' not in params else params['name']
year = date.today().year if 'year' not in params else params['year']
start_html = None

scraperwiki.sqlite.attach(sourcescraper)

def all_years():
    return range(date.today().year, 1998, -1)

def format_race_name(race_id):
    year = re.sub(r'[^\d]+', '', race_id)
    racename = re.sub(r'[\d]+', '', race_id)
    return '%s Race %s' % (year, racename.upper())

def pdf_url(race_id):
    year = re.sub(r'[^\d]+', '', race_id)
    racename = re.sub(r'[\d]+', '', race_id)
    return 'http://www.watersideseries.org.uk/results/%sres%s.pdf' % (year, racename.lower())

sections = collections.OrderedDict()
colnames = []
title = "Waterside Series Results"

if show == 'club' or club is not None:
    if club is not None:
        title = "Waterside Series Results - %s" % (club)
        start_html = '<form action="." method="GET">\n'
        start_html += '<p>Year: <select name="year">\n'
        for y in all_years():
            start_html += '<option value="%(year)s"%(selected)s>%(year)s</option>\n' % {'year': y, 'selected': ' selected="selected"' if str(y) == year else ''}
        start_html += '</select>\n'
        start_html += '<input type="hidden" name="club" value="%s" />\n' % (club)
        start_html += '<input type="submit" value="Go" name="" />\n'
        start_html += '</form>\n'
        colnames = ['Class', 'Position', 'Names', 'Club', 'Time']
        query = "race, race_class, position, names, club, time, boat_number from `results` where race LIKE '%s%%' and club like '%%%s%%' order by race desc, time" % (year, club)
        data = scraperwiki.sqlite.select(query)
        for row in data:
            key = format_race_name(row['race'])
            if key not in sections:
                sections[key] = ['<p><a href=".?race=%s#club=%s">Show in full results</a></p>' % (row['race'], club), [], '<p>Total starters: 0</p>']
            sections[key][1].append(['<a href=".?race=%s#%s">%s</a>' % (row['race'], row['race_class'], row['race_class']), '<a name="boat_%s">%s</a>' % (row['boat_number'], row['position'] or ''), '<a href=".?race=%s#boat_%s">%s</a>' % (row['race'], row['boat_number'], row['names']), row['club'], row['time']])
            sections[key][2] = '<p>Total starters: %d</p>' % (len(sections[key][1]))
    else:
        raise Exception('No club specified!')
elif show == 'name' or name is not None:
    if name is not None:
        colnames = ['Race', 'Class', 'Position', 'Names', 'Club', 'Time']
        for term in name.split("|"):
            query = "race, race_class, position, names, club, time, boat_number from `results` where names LIKE '%%%s%%' order by race desc, time" % (term.strip())
            data = scraperwiki.sqlite.select(query)
            key = "Matches for '%s'" % (term)
            for row in data:
                if key not in sections:
                    sections[key] = [[], '<p>Total races: 0</p>']
                sections[key][0].append(['<a href=".?race=%s">%s</a>' % (row['race'], format_race_name(row['race'])), '<a href=".?race=%s#%s">%s</a>' % (row['race'], row['race_class'], row['race_class']), '<a name="boat_%s">%s</a>' % (row['boat_number'], row['position'] or ''), '<a href=".?race=%s#boat_%s">%s</a>' % (row['race'], row['boat_number'], row['names']), '<a href=".?club=%s">%s</a>' % (row['club'], row['club']), row['time']])
                sections[key][1] = '<p>Total races: %d</p>' % (len(sections[key][0]))
    else:
        raise Exception('No club specified!')
elif show == 'results' or race is not None:
    title = "Waterside Series Results - %s" % (format_race_name(race))
    if club is None:
        start_html = '<a href="%s">Download official PDF results</a>' % (pdf_url(race))
        colnames = ['Position', 'Names', 'Club', 'Time']
        query = "race_class, position, names, club, time, boat_number from `results` where race = '" + race + "' order by race_class, time"
        data = scraperwiki.sqlite.select(query)
        for row in data:
            key = row['race_class']
            if key not in sections:
                sections[key] = [[], '']
            sections[key][0].append(['<a name="boat_%s">%s</a>' % (row['boat_number'], row['position'] or ''), row['names'], '<a href=".?club=%s">%s</a>' % (row['club'], row['club']), row['time']])
            sections[key][1] = '<p>Total starters: %d</p>' % (len(sections[key][0]))
    else:
        colnames = ['Class', 'Position', 'Names', 'Club', 'Time']
        query = "race_class, position, names, club, time, boat_number from `results` where race = '" + race + "' and club like '%" + club + "%' order by time"
        data = scraperwiki.sqlite.select(query)
        key = 'Results for %s' % (club)
        sections[key] = ['<p><a href=".">Show all results</a></p>', [], '<p>Total starters: 0</p>']
        for row in data:
            sections[key][1].append(['<a href=".#%s">%s</a>' % (row['race_class'], row['race_class']), '<a name="boat_%s">%s</a>' % (row['boat_number'], row['position'] or ''), '<a href=".#boat_%s">%s</a>' % (row['boat_number'], row['names']), row['club'], row['time']])
            sections[key][2] = '<p>Total starters: %d</p>' % (len(sections[key][1]))
elif show == 'summary':
    start_html = 'This site provides current and past results of the <a href="http://www.watersideseries.org.uk/">Waterside Series</a> of canoe races organised by Newbury Canoe Club in HTML format. The site is not affiliated to or endorsed by Newbury CC in any way. Please use the official site for the latest news and official race results in PDF format.'
    search_html = '<form action="." method="GET">\n'
    search_html += '<p><em>Enter a name or multiple names separated using pipe (|) symbols.</em></p>'
    search_html += '<p>Name(s): '
    search_html += '<input type="text" name="name" value="" size="40" /></p>\n'
    search_html += '<input type="submit" value="Search" name="" />\n'
    search_html += '</form>\n'
    sections['Current Results'] = (" | ".join(row) for row in [[ '<a href="?race=%s%s">%s</a>' % (y, r, format_race_name(str(y) + r)) for r in ['a', 'b', 'c', 'd'] ] for y in all_years()[:1]])
    sections['Search Results'] = [search_html]
    sections['Past Results'] = [[[ '<a href="?race=%s%s">%s</a>' % (y, r, format_race_name(str(y) + r)) for r in ['a', 'b', 'c', 'd'] ] for y in all_years()[1:]]]

print """<html>
<head>
<title>%s</title>
<style type="text/css">
body {
    font-family: arial, helvetica, sans-serif;
    font-size: 0.85em;
    margin: 0;
    padding: 0;
}
.wrapper {
    min-height: 100%%;
}
table {
    border-collapse: collapse;
}
table td, table th {
    font-size: 0.85em;
    border-bottom: 1px solid #999999;
    padding: 5px;
    text-align: left;
}
.highlight {
    background-color: #FFFBCC;
}
.header {
    background-color: #69c;
}
.header p {
    font-size: 2em;
    padding: 0.5em;
    margin: 0;
    font-weight: bold;
    border-bottom: 1px solid #999;
}
.header p a {
    text-decoration: none;
    color: #fff;
}
.body {
    margin: 1em;
    min-height: 100%%;
}
.footer {
    padding: 1em;
}
.footer {
    background-color: f0f0f0;
    border-top: 1px solid #999;
    color: #666;
    margin-top: 3em;
}
</style>
<script src="http://yui.yahooapis.com/3.4.1/build/yui/yui-min.js"></script>
</head>
<body>
<div class="wrapper">
<div class="header">
<p><a href=".">Waterside Series Results</a></p>
</div>
<div class="body">
""" % (title)

print "<h1>%s</h1>\n" % (title)

if start_html is not None:
    print start_html

for (k, v) in sections.items():
    print '<h2><a name="%s">%s</a></h2>\n' % (k, k)
    for item in v:
        if type(item) == str or type(item) == unicode:
            print item
        elif type(item) == list:
            print "<table>\n"
            if colnames is not None and len(colnames) > 0:
                print "<tr>\n"
                for colname in colnames:
                    print "<th>%s</th>\n" % (colname)
                print "</tr>\n"
            for row in item:
                print "<tr>\n"
                for val in row:
                    print "<td>%s</td>\n" % (val)
                print "</tr>\n"
            print "</table>\n"

print """<script type="text/javascript">
YUI().use('node', 'selector-css3', function (Y) {
    if (location.hash && location.hash.length > 1 && location.hash.indexOf("#boat") == 0) {
        Y.Node.one("tr a[name=" + location.hash.replace("#", "") + "]").ancestor().ancestor().addClass("highlight");
    }
    if (location.hash && location.hash.length > 1 && location.hash.indexOf("#club=") == 0) {
        var clubName = location.hash.replace("#club=", "");
        Y.Node.all("table tr").each(function(rowNode) {
            rowNode.get('children').each(function (cellNode) {
                if (cellNode.getContent().indexOf(clubName) >= 0) {
                    rowNode.addClass("highlight");
                }
            });
        });
    }
});
</script>
</div>
<div class="footer"><p>Waterside Series Results by Will Abson. Data based on official PDFs from Newbury Canoe Club's <a href="http://www.watersideseries.org.uk/">Watersides</a> site and <a href="https://scraperwiki.com/scrapers/waterside_series_results/">scraped using ScraperWiki</a>.</p><p>This site is not affiliated to or endorsed by Newbury CC in any way. Please use the official site for the latest news and official race results in PDF format.</p></div>
</div>
</body>
</html>"""
import scraperwiki
from datetime import datetime

sourcescraper = 'ea_river_thames_conditions'
scraperwiki.sqlite.attach(sourcescraper)

select = "location, MAX(`pubdate` || ' ' || `status`) AS last_status from `conditions` group by `location`"
data = scraperwiki.sqlite.select(select)
conditions_by_loc = dict([(d['location'], d['last_status']) for d in data])

# Important to get the right order of locks
sections = ["Upstream to St John's Lock",
"St John's Lock to Buscot Lock",
"Buscot Lock to Grafton Lock",
"Grafton Lock to Radcot Lock",
"Radcot Lock to Rushey Lock",
"Rushey Lock to Shifford Lock",
"Shifford Lock to Northmoor Lock",
"Northmoor Lock to Pinkhill Lock",
"Pinkhill Lock to Eynsham Lock",
"Eynsham Lock to King's Lock",
"King's Lock to Godstow Lock",
"Godstow Lock to Osney Lock",
"Osney Lock to Iffley Lock",
"Iffley Lock to Sandford Lock",
"Sandford Lock to Abingdon Lock",
"Abingdon Lock to Culham Lock",
"Culham Lock to Clifton Lock",
"Clifton Lock to Day's Lock",
"Day's Lock to Benson Lock",
"Benson Lock to Cleeve Lock",
"Cleeve Lock to Goring Lock",
"Goring Lock to Whitchurch Lock",
"Whitchurch Lock to Mapledurham Lock",
"Mapledurham Lock to Caversham Lock",
"Upstream of Blake's Lock",
"Caversham Lock to Sonning Lock",
"Sonning Lock to Shiplake Lock",
"Shiplake Lock to Marsh Lock",
"Marsh Lock to Hambleden Lock",
"Hambleden Lock to Hurley Lock",
"Hurley Lock to Temple Lock",
"Temple Lock to Marlow Lock",
"Marlow Lock to Cookham Lock",
"Cookham Lock to Boulters Lock",
"Boulters Lock to Bray Lock",
"Bray Lock to Boveney Lock",
"Boveney Lock to Romney Lock",
"Romney Lock to Old Windsor Lock",
"Old Windsor Lock to Bell Weir Lock",
"Bell Weir Lock to Penton Hook Lock",
"Penton Hook Lock to Chertsey Lock",
"Chertsey Lock to Shepperton Lock",
"Shepperton Lock to Sunbury Lock",
"Sunbury Lock to Molesey Lock",
"Molesey Lock to Teddington Lock"]

# From http://stackoverflow.com/a/5164027/1582415
def prettydate(d):
    diff = datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{} minutes ago'.format(s/60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{} hours ago'.format(s/3600)

title = "River Thames Conditions"

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
div.section, div.detail {
    /*font-size: 0.85em;
    border-bottom: 1px solid #999999;*/
    padding: 5px 0;
    text-align: left;
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
div.section {
    margin: 0 0;
}
div.section-name, div.section-conditions, div.section-when {
    display: inline-block;
}
div.section-name {
    width: 25em;
}
div.section-conditions {
    width: 12em;
}
div.section-when {
    width: 10em;
}
span.conditions  {
     border-radius: 10px;
     -moz-border-radius: 10px;
    padding: 5px;
}
.stream-increasing {
    background-color: #FFE010;
}
.stream-decreasing {
    background-color: #FFE010;
}
.strong-stream {
    background-color: #F00;
    color: #fff;
}
.no-warnings {
    color: #666;
}
.detail {
    display: none;
}
div.section {
    cursor: hand;
}
.section > div, .detail > div {
    min-height: 2.5em;
}
</style>
<script src="http://yui.yahooapis.com/3.9.0/build/yui/yui-min.js"></script>
</head>
<body>
<div class="wrapper">
<div class="header">
<p><a href=".">River Thames Conditions</a></p>
</div>
<div class="body">
""" % (title)

#print "<h1>%s</h1>\n" % (title)

print '<div class="list">\n'
sections.reverse() # Reverse so that London is first
for s in sections:
    if s in conditions_by_loc:
        timestamp = conditions_by_loc[s].split(' ', 1)[0]
        conditions = conditions_by_loc[s].split(' ', 1)[1]
        conditions_html = '<span class="conditions">%s</span>' % (conditions)
        if conditions.lower() == "caution stream decreasing":
            conditions_html = '<span class="conditions stream-decreasing">%s</span>' % ("Stream Decreasing")
        elif conditions.lower() == "caution stream increasing":
            conditions_html = '<span class="conditions stream-increasing">%s</span>' % ("Stream Increasing")
        elif conditions.lower() == "caution strong stream":
            conditions_html = '<span class="conditions strong-stream">%s</span>' % ("Strong Stream")
        elif conditions.lower() == "no stream warnings":
            conditions_html = '<span class="conditions no-warnings">%s</span>' % ("No Warnings")
        updated = datetime.fromtimestamp(float(timestamp))
        date_html = '<span title="%s">%s</span>' % (updated.strftime("%A, %d %B %Y %H:%M"), prettydate(updated))
        print '<div class="section"><div><div class="section-name">%s</div><div class="section-conditions">%s</div><div class="section-when">%s</div></div><div class="detail">Loading...</div></div>\n' % (s, conditions_html, date_html)
print '</div>\n'

print """<script type="text/javascript">
relativeTime = function(from, to)
{
   if (!to)
   {
      to = new Date();
   }

   var seconds_ago = ((to - from) / 1000),
      minutes_ago = Math.floor(seconds_ago / 60);

   if (minutes_ago <= 0)
   {
      return "" + seconds_ago + " seconds ago";
   }
   if (minutes_ago == 1)
   {
      return "1 minute ago";
   }
   if (minutes_ago < 45)
   {
      return "" + minutes_ago + " minutes ago";
   }
   if (minutes_ago < 90)
   {
      return "1 hour ago";
   }
   var hours_ago  = Math.round(minutes_ago / 60);
   if (minutes_ago < 1440)
   {
      return "" + hours_ago + " hours ago";
   }
   if (minutes_ago < 2880)
   {
      return "1 day ago";
   }
   var days_ago  = Math.round(minutes_ago / 1440);
   return "" + days_ago + " days ago";
};
YUI().use('node', 'selector-css3', 'event', 'datasource', "datasource-get", "datasource-jsonschema", function (Y) {
    function handleClick(e) {
        var detailrow = e.target.ancestor(".section").one(".detail");
        detailrow.setStyle("display", (detailrow.getStyle("display") == "block") ? "none" : "block")
        if (detailrow.getHTML() == "Loading...") {
            var myDataSource = new Y.DataSource.Get({
                source: "https://api.scraperwiki.com/api/1.0/datastore/sqlite?"
            });
            myDataSource.plug(Y.Plugin.DataSourceJSONSchema, {
                schema: {
                    //resultListLocator: "query.results.result",
                    resultFields: ["status", "location", "pubdate"]
                }
            });
            myDataSource.sendRequest({
                request: "format=jsondict&name=ea_river_thames_conditions&query=select%20*%20from%20%60conditions%60%20where%20location%3D%27Molesey%20Lock%20to%20Teddington%20Lock%27%20order%20by%20pubdate%20desc%20limit%2010",
                callback: {
                    success: function populateDetail(e) {
                        var html = "";
                        for (var i=1; i<e.data.length; i++)
                        {
                            var item = e.data[i];
                            var conditions = item.status;
                            var conditions_html = '<span class="conditions">' + item.status + '</span>';
                            if (conditions.toLowerCase() == "caution stream decreasing") {
                                conditions_html = '<span class="conditions stream-decreasing">Stream Decreasing</span>';
                            } else if (conditions.toLowerCase() == "caution stream increasing") {
                                conditions_html = '<span class="conditions stream-increasing">Stream Increasing</span>';
                            } else if (conditions.toLowerCase() == "caution strong stream") {
                                conditions_html = '<span class="conditions strong-stream">Strong Stream</span>';
                            } else if (conditions.toLowerCase() == "no stream warnings") {
                                conditions_html = '<span class="conditions no-warnings">No Warnings</span>';
                            }
                            html += "<div><div class=\\"section-name\\"></div><div class=\\"section-conditions\\">" + conditions_html + "</div><div class=\\"section-when\\">" + relativeTime(parseInt(item.pubdate, 10)*1000) + "</div></div>";
                        }
                        detailrow.setHTML(html);
                    },
                    failure: function (e) { alert("failure!") }
                }
            });
        }
    }
    Y.one("div.list").delegate("click", handleClick, ".section")
    if (location.hash && location.hash.length > 1 && location.hash.indexOf("#boat") == 0) {
        Y.Node.one("tr a[name=" + location.hash.replace("#", "") + "]").ancestor().ancestor().addClass("highlight");
    }
});
</script>
</div>
<div class="footer"><p>River Thames Conditions by Will Abson. Data from the Environment Agency's <a href="http://riverconditions.environment-agency.gov.uk/">River Conditions</a> site and <a href="https://scraperwiki.com/scrapers/ea_river_thames_conditions/">scraped using ScraperWiki</a>.</p><p>This site is not affiliated to or endorsed by the Environment Agency. Data may not be accurate and should not be relied upon for navigation or other purposes.</p></div>
</div>
</body>
</html>"""

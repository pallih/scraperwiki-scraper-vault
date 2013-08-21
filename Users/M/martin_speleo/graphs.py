import scraperwiki

class library:
    def __init__(self, content):
        self.content = content
    def write(self):
        return self.content

excanvas = library('<!--[if lte IE 8]><script language="javascript" type="text/javascript" src="http://people.iola.dk/olau/flot/excanvas.min.js"></script><![endif]-->')
jQuery = library('<script language="javascript" type="text/javascript" src="http://people.iola.dk/olau/flot/jquery.js"></script>')
flot = library('<script language="javascript" type="text/javascript" src="http://people.iola.dk/olau/flot/jquery.flot.js"></script>')

class series:
    def __init__(self, apiurl, srcname, sqlselect, x_sql_title, y_sql_title, hover_text_sql_title=None, link_sql_title=None, plot_style = ".", title=None):
        self.apiurl= apiurl
        self.srcname= srcname
        self.sqlselect= sqlselect
        self.x_sql_title = x_sql_title
        self.y_sql_title = y_sql_title
        self.hover_text_sql_title = hover_text_sql_title
        self.link_sql_title = link_sql_title
        self.plot_style = plot_style
        self.title = title

class html_page:
    def __init__(self, title):
        self.libraries = []
        self.body = ""

    def add_content(self, content):
        self.body += content

    def add_library(self, library):
        if library not in self.libraries:
            self.libraries.append(library)

    def add_graph(self, id, graphtype, series, x_min=None, x_max=None, y_min=None, y_max=None):
        """where type is 'line_flot', or 'bar_google' etc
                    series is (sql, x_sql_title, y_sql_title,
hover_text_sql_title, link_sql_title, plot_style)
                    sql is the sql to execute on a particular scraper wiki
        This could be implemented using either including the data, or
getting via ajax.  For some stuff I need at work I am want to look at
pannable and zoomable graphs that get their data from ajax."""
        if graphtype== "timeplot_flot":
             self.add_content("<div id='%s' style='width:600px;height:300px;'></div>" % id)
             self.add_library(excanvas)
             self.add_library(jQuery)
             self.add_library(flot)
             graphscript= """<script type="text/javascript">
var graph_%(id)s = Array();

function graph_update_%(id)s(){
    $.plot($("#%(id)s"), graph_%(id)s, { xaxis: { mode: "time" }, legend: {show:true} });
}

$(function () {
""" % {"id": id}
             for sid in range(len(series)):
                 s = series[sid];
                 graphscript += """
$.ajax({url:'%(api_url)s', 
        dataType:"jsonp", 
        data:{name:'%(srcname)s', 
              query:'%(query)s', 
              format:"json"}, 
        success:function(tdata) { 
            var a = [];
            for (line in tdata) {
                d = new Date(tdata[line]['%(x_sql_title)s']);
                a.push([d.getTime(), tdata[line]['%(y_sql_title)s']]);
                }
            graph_%(id)s[%(sid)i] = {data: a, label:'%(title)s'};
            graph_update_%(id)s();
        }
       });""" % {"api_url": s.apiurl, "srcname": s.srcname, "query": s.sqlselect, "x_sql_title": s.x_sql_title, "y_sql_title": s.y_sql_title, "id":id, "sid":sid, "title": s.title};
             graphscript += """
});
</script>""";
             self.add_library(library(graphscript));

    def write(self):
        def concatenate(x, y):
            return x + "\n" + y
        return "<html>\n<head>%s\n</head>\n<body>\n%s\n</body>\n</html>" % (reduce(concatenate, [l.write() for l in self.libraries], ""),
             self.body)

page = html_page("My Graph")
page.add_content("<H1>My Graph</H1>")
page.add_graph("mygraph", "timeplot_flot", [series("https://api.scraperwiki.com/api/1.0/datastore/sqlite", "uk_lottery_scrapedownload_1", 'SELECT SUM(`Grant amount`) AS amount, (julianday(date(`Grant date`,"start of month"))-2440587.5)*86400000.0 AS date_month_start FROM swdata WHERE `Local authority` = "West Dorset" GROUP BY date(`Grant date`,"start of month")', "date_month_start", "amount", title="West Dorset"), series("https://api.scraperwiki.com/api/1.0/datastore/sqlite", "uk_lottery_scrapedownload_1", 'SELECT SUM(`Grant amount`) AS amount, (julianday(date(`Grant date`,"start of month"))-2440587.5)*86400000.0 AS date_month_start FROM swdata WHERE `Local authority` = "Bedford" GROUP BY date(`Grant date`,"start of month")', "date_month_start", "amount", title="Bedford")])
print page.write()

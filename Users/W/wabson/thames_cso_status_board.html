<html>
<head>
<script src="http://yui.yahooapis.com/3.4.1/build/yui/yui-min.js"></script>
<!--Load the AJAX API-->
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});
</script>
<style type="text/css">
  html { height: 100% }
  body { font-size: 0.8em; font-family: arial, helvetica, sans-serif; margin: 5em; }
</style>
<title>Thames CSO Status Board</title>
</head>
<body>
<!--Div that will hold the pie chart-->
<h1>Thames CSO Status Board</h1>
<p class="intro">This page shows the number of Combined Sewer Overflow events for each month, as reported by Thames Water's <a href="http://www.thameswater.co.uk/cps/rde/xchg/corp/hs.xsl/3644_9989.htm">email notification service</a>.</p>
<div id="chart_div"></div>
<p>For alerts and more info you can follow <a href="https://twitter.com/ThamesCSOAlerts">@ThamesCSOAlerts</a> on Twitter.</p>
<script>
// Create a YUI sandbox on your page.
var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
YUI().use('node', 'event', 'datasource', function (Y) {
    // The Node and Event modules are loaded and ready to use.
    // Your code goes here
    var myDataSource = new Y.DataSource.Get({
        source: "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=thames_cso_alerts&"
    });
    var now = new Date(), month = now.getMonth() + 1, monthStr = month < 10 ? "0" + month : "" + month, year = now.getFullYear();
    //var query = "select loc_name, loc_desc, substr(published, 0, 8) as month, count(loc_name) as n from `alerts` where month='" + year + "-" + monthStr + "' group by loc_name limit 10";
    var query = "select loc_name, loc_desc, substr(published, 0, 8) as month, count(substr(published, 0, 8)) as n from `alerts` group by loc_name, month order by month, loc_name";
    // Normalize the data sent to myCallback
    myDataSource.plug({fn: Y.Plugin.DataSourceJSONSchema, cfg: {
        schema: {
            resultFields: ["loc_name", "loc_desc", "month", "n"]
        }
    }});
    myDataSource.sendRequest({
        request: "query=" + encodeURIComponent(query),
        callback: {
            success: function(e){
                // Create the data table.
                var sites = ['Hammersmith', 'Mogden'], bymonth = {};
                var getMonthLabel = function(ym) {
                    var arr = ym.split('-'), y = parseInt(arr[0].substring(2,4), 10), m = parseInt(arr[1], 10);
                    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                    return months[m - 1] + ' ' + y;
                }
                for (var i=0; i<e.data.length; i++) {
                    var m = e.data[i]['month'];
                    bymonth[m] = bymonth[m] || {};
                    for (var j=0; j<sites.length; j++) {
                        if (sites[j] == e.data[i]['loc_name']) {
                            bymonth[m][sites[j]] = e.data[i]['n'];
                        }
                    }
                }
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'Month');
                for (var j=0; j<sites.length; j++) {
                    data.addColumn('number', sites[j]);
                }
                var total = 0, monthdata;
                for (var month in bymonth) {
                    monthdata = [getMonthLabel(month)];
                    for (var j=0; j<sites.length; j++) {
                        monthdata.push(bymonth[month][sites[j]] || 0);
                    }
                    data.addRow(monthdata);
                }
/*
                for (var i=0; i<e.data.length; i++) {
                    data.addRow([e.data[i]['month'], e.data[i]['loc_desc'], e.data[i]['n']]);
                    total += e.data[i]['n'];
                }*/
        
                // Set chart options
                var options = {
                    'vAxis': {'title': 'Discharge events', 'maxValue': 12},
                    'hAxis': {'title': 'Month'},
                    'width': 800,
                    'height': 450
                };
        
                // Instantiate and draw our chart, passing in some options.
                var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
                chart.draw(data, options);
            },
            failure: function(e){
                alert(e.error.message);
            }
        }
    });
});
</script>
</body>
</html>

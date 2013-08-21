<html>
<head>
<script src="http://yui.yahooapis.com/3.4.1/build/yui/yui-min.js"></script>
<!--Load the AJAX API-->
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart', 'table']});
</script>
<style type="text/css">
  html { height: 100% }
  body { font-size: 0.8em; font-family: arial, helvetica, sans-serif; margin: 2em; }
  #table_div { max-width: 1200px; }
</style>
<title>Hasler Series League Table</title>
</head>
<body><div id="scraperwikipane" style="border:thin #aaf solid; display:block; position:fixed; top:0px; right:0px; background:#eef; margin: 0em; padding: 6pt; font-size: 10pt; z-index: 8675309; ;"><a href="https://scraperwiki.com/views/thames_cso_status_board/" id="scraperwikipane" style="width:167px; height:17px; margin:0; padding: 0; border-style: none; "><img style="border-style: none" src="https://media.scraperwiki.com/images/powered.png" alt="Powered by ScraperWiki"></a></div>
<!--Div that will hold the pie chart-->
<h1>Hasler Series League Table</h1>

<p class="intro">The Hasler season runs from September to August of each year. This page shows the club points allocated to each club within the region so far in the current season.</p>
<div id="chart_div"></div>
<div id="table_div"></div>
<script>
var now = new Date(), month = now.getMonth() + 1, year = now.getFullYear(), defaultYear = month < 9 ? year : year + 1;
var defaultRegion = 'LS';
// Create a YUI sandbox on your page.
var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ]
YUI().use('node', 'event', 'datasource', 'history', function (Y) {
    function showHaslerRankings(region, year) {
        // The Node and Event modules are loaded and ready to use.
        // Your code goes here!
        var myDataSource = new Y.DataSource.Get({
            source: "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=hasler_marathon_results&"
        });
        var query = "select club_name, races.race_name as race_name, races.race_date as race_date, position from `club_points` inner join races on races.results_url=club_points.race_url inner join hasler_marathon_club_list.swdata as club_list on club_points.club_name=club_list.name where region_code='" + region + "' AND hasler_year=" + year + " AND races.race_name <> 'Hasler Final' ORDER BY race_date, race_name, club_name";
        // Normalize the data sent to myCallback
        myDataSource.plug({fn: Y.Plugin.DataSourceJSONSchema, cfg: {
            schema: {
                resultFields: ["club_name", "race_name", "race_date", "position"]
            }
        }});
        myDataSource.sendRequest({
            request: "query=" + encodeURIComponent(query) + "&attach=hasler_marathon_club_list",
            callback: {
                success: function(e) {
                    // Create the data table.
                    var clubPoints = {}, races = [], totalPoints = {};
    
                    var findRace = function(name) {
                        for (var i=0; i<races.length; i++) {
                            if (races[i].name == name) {
                                return true;
                            }
                        }
                        return false;
                    };
                    
                    var addRace = function(name, date) {
                        if (!findRace(name)) {
                            races.push({name: name, date: date});
                        }
                    };
                    
                    var getMonthLabel = function(ym) {
                        var arr = ym.split('-'), y = parseInt(arr[0]), m = parseInt(arr[1]);
                        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                        return months[m - 1] + ' ' + y;
                    }
                    for (var i=0; i<e.data.length; i++) {
                        var raceName = e.data[i]['race_name'], clubName = e.data[i]['club_name'];
                        addRace(raceName, e.data[i]['race_date']);
                        clubPoints[clubName] = clubPoints[clubName] || {};
                        clubPoints[clubName][raceName] = e.data[i]['position'];
                        totalPoints[clubName] = (totalPoints[clubName] || 0) + e.data[i]['position'];
                    }
                    var data = new google.visualization.DataTable();
    
                    // Add columns
                    data.addColumn('string', 'Club');
                    for (var i=0; i<races.length; i++) {
                        data.addColumn('number', races[i].name + " (" + races[i].date + ")");
                    }
                    data.addColumn('number', 'Total');
    
                    rows = [];
                    // Add rows
                    for (var clubName in clubPoints) {
                        var rowData = [clubName];
                        for (var i=0; i<races.length; i++) {
                            rowData.push(clubPoints[clubName][races[i].name] || 0);
                        }
                        rowData.push(totalPoints[clubName]);
                        rows.push(rowData);
                    }
    
                    // Sort the rows by total points, largest first
                    rows.sort(function(a, b) { return (a[a.length-1] > b[b.length-1] ? -1 : (a[a.length-1] < b[b.length-1] ? 1 : 0)) });
    
                    for (var i=0; i<rows.length; i++) {
                        //rows[i].pop(); // remove total now we are done with it
                        data.addRow(rows[i]);
                    }
            
                    // Set chart options
                    var options = {
                        'vAxis': {'title': 'Club'},
                        'hAxis': {'title': 'Points'},
                        'width': 800,
                        'height': 450,
                        'isStacked': true,
                        'titlePosition': 'none'
                    };
    
                    // Set rows in a data view.
                    var dataView1 = new google.visualization.DataView(data);
                    var chartRows = [];
                    for (var i=0; i<=races.length; i++) { chartRows.push(i); } // do not add total or min points
                    dataView1.setColumns(chartRows);
            
                    // Instantiate and draw our chart, passing in some options.
                    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
                    chart.draw(dataView1, options);
    
                    // Set rows in a data view.
                    var dataView2 = new google.visualization.DataView(data);
                    //dataView2.setRows([0, 1, 3]);
                    var table3 = new google.visualization.Table(document.getElementById('table_div'), { width: 600 });
                    table3.draw(dataView2, null);
    
                },
                failure: function(e){
                    alert(e.error.message);
                }
            }
        });
    }
    var history = new Y.HistoryHash({
        initialState: {
            year: defaultYear,
            region: defaultRegion
        }
    });
    Y.on('history:change', function (e) {
        showHaslerRankings(history.get('region'), history.get('year'));
    });
    showHaslerRankings(history.get('region'), history.get('year'));
});
</script>
</body>
</html>

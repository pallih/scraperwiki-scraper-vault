#!/usr/bin/python

# ------------ TODO: Save various swaps to database. No need to recalculate. (method column to describe calculation method, PKEY(method, round)
# ------------ TODO: Add compare function?

import scraperwiki    
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
import random
import cgi
import os
import copy
import re

scrapersource = 'afl_2012'       
scraperwiki.sqlite.attach(scrapersource)

queryString = os.getenv("QUERY_STRING", "")
round = ''
search  = ''
stats = 'points_avg_calc'
exact = False
if queryString != '':
    get = dict(cgi.parse_qsl(queryString))    
    round = get['round'] if get.has_key('round') else ''
    stats = get['stats'] if get.has_key('stats') else 'points_avg_calc'
    search = get['search'] if get.has_key('search') else ''
    if get.has_key('exact'):
        exact = True if get['exact'] == 'True' else False

round = round if round != '' else scraperwiki.sqlite.execute("select max(round) from afl_2012.swdata")['data'][0][0]

chartNo = 0

#-------------------------------------- Round 6 Team -----------------------------------------

kitty = 41000

defenders = ['Scotland, Heath', 'Goddard, Brendon', 'Hunt, Karmichael', 'Darley, Sam',
                     'Patfull, Joel', 'Smedts, Billie', 'Houli, Bachar' ] # 7 Defenders

midfielders = ['Boyd, Matthew', 'Stanton, Brent',
                'Pendlebury, Scott', 'Parker, Luke', 'Wingard, Chad', 'Kennedy, Adam'] # 6 Mids

rucks = ['Cox, Dean', 'Giles, Jonathan'] # 2 Rucks

forwards = ['Beams, Dayne [MID]', 'Whitecross, Brendan', 'Dangerfield, Patrick [MID]', 'Adams, Taylor',
            'Blair, Jarryd', 'Cornes, Chad', 'Goodes, Adam'] # 7 Forwards

reserves = ['Browne, Alex', 'Astbury, David',
            'Reid, Sam J.', 'Hogan, Simon',
            'Ryder, Patrick', 'Stephenson, Orren',
            'McKinley, Ben', 'Warren, Ben'] # 8 reserves

team = []
team += defenders
team += midfielders
team += rucks
team += forwards
#team += reserves

# -------------- Queries -------------------------

roundCountData = scraperwiki.sqlite.select(           
    'round, count(round) from swdata group by round'
)

topPlayerData = scraperwiki.sqlite.select(           
    '* from swdata'
    + ' where round = ' + str(round)
    + ' order by rank_last_round asc limit 10'
)

topPlayerNames = scraperwiki.sqlite.select(           
        'distinct name from swdata'
        + ' order by rank_last_round asc limit 5')

topPlayerNames = [name["name"] for name in topPlayerNames]

# ---------------- HTML Header -------------------------
head = \
'<html>' + \
'<head>' + \
    '<title>AFL Dream Team ~ Round ' + str(round) + (' | Search: %s' % search if search != '' else '')  + '</title>' + \
    '<script src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>' + \
    '<script src="http://www.danvk.org/dragtable/dragtable.js"></script>' + \
    '<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>' + \
    '<script src="http://code.highcharts.com/highcharts.js"></script>' + \
    '<script src="http://code.highcharts.com/modules/exporting.js"></script>' + \
'</head>' + \
'''<style type="text/css">

html, body{
    margin:0;
    background-color: white;
}

table, th, td, tr {
    padding: 5px;
    border-collapse: collapse;
    background-color: white;
    margin:0 auto;
}

th {
    background-color: 0033FF;
    color: white;
    padding: 5px;
}

div.header, div.footer {
    background-color: black;
    color: white;
    padding: 5px;
}

div.page {
    text-align: center;
    align: center;
    margin:0 auto;
    width: 1100px;
    height: 100%;
    background-color: white;
}

*.great {
    background-color: green;
    color: white;
}

*.bad {
    background-color: red;
    color: white;
}

a:link {color:white;}      /* unvisited link */
a:visited {color:gray;}  /* visited link */
a:hover {color:yellow;}  /* mouse over link */
a:active {color:orange;}  /* selected link */

a.black:link {color:black;}      /* unvisited link */
a.black:visited {color:gray;}  /* visited link */
a.black:hover {color:orange;}  /* mouse over link */
a.black:active {color:yellow;}  /* selected link */

</style>

<script>
    function aflChart(title, subtitle, type, container, names, comparison) {
        var comparison = comparison;
        var names = names;
        var title = title;
        var subtitle = subtitle;
        var type = type;
        var container = container;
        this.chart;
        
        var xAxisLabels = [];
        var dataSet = [];
            
        this.getPlayerData = function(name) {
            var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite";            
            var srcname = "afl_2012"; 
            var sqlselect = "select name, round, " + comparison + " from swdata where name='" + name + "'"; 
            return $.ajax({
                url: apiurl, 
                dataType: "jsonp", 
                data:{
                    name: srcname, 
                    query: sqlselect, 
                    format: "jsondict"
                }, 
                success: this.processJson
            });    
        };
        
        this.processJson = function(json) {
            var data = [];
            for(var i = 0; i < json.length; i++) {
                data.push(json[i][comparison]);
            }
            dataSet.push({name: json[0]["name"], data: data});
            
            // Do the xAxisLabels Separately
            for(var i = 0; i < json.length; i++) {
                xAxisLabels.push("R " + json[i]["round"]);
            }
            
            chart = createChart(title, subtitle, type, container, xAxisLabels, comparison, dataSet);
        }
        
        this.build = function() {
            var deferredCollection = [];
            for(i in names){
                deferredCollection.push(this.getPlayerData(names[i]));
            }
        }
    }
    
    function jsonTable(tdata)           
    {
        var keys = tdata["keys"]; 
        var data = tdata["data"]; 
        
        var table=document.getElementById("table");
        
        var header=table.insertRow(0);
        for(var i = 0; i < keys.length; i++){
            var cell=header.insertCell(i);
            cell.innerHTML=keys[i];
        }
        
        for (var i = 0; i < data.length; i++){
            var row=table.insertRow(i+1);
            for(var j = 0; j < data[0].length; j++){
                var cell=row.insertCell(j);
                cell.innerHTML=data[i][j];
            }
        }
    }
    
    function createChart(title, subtitle, type, divId, xAxisLabels, yAxisTitle, data) {
            return new Highcharts.Chart({
                chart: {
                    renderTo: divId,
                    type: type,
                    marginRight: 130,
                    marginBottom: 25
                },
                title: {
                    text: title,
                    x: -20 //center
                },
                subtitle: {
                    text: subtitle,
                    x: -20
                },
                xAxis: {
                    categories: xAxisLabels
                },
                yAxis: {
                    title: {
                        text: yAxisTitle
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'}]
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.series.name + '</b><br/>' + this.x + ': ' + this.y;
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -10,
                    y: 100,
                    borderWidth: 0
                },
                series: data
            });
    }</script>

<body>
<div class="page">'''

# ---------------- Methods -------------------------
def br():
    print "<br />"
    print "<br />"

def random_colour(min=20, max=200):
    func = lambda: int(random.random() * (max-min) + min)
    r, g, b = func(), func(), func()
    return '%02X%02X%02X' % (r, g, b)

def getChart2(playerNames, stat):
    # Set the vertical range from 0 to max_y
    max_y = 50

    dataRows = []

    for name in playerNames:
        rowSelection = scraperwiki.sqlite.select(
        'name, ' + stat + ' from swdata '
        + 'where name = \"' + name + '\"')

        dataRow = []
        for row in rowSelection:
            rowStat = row[stat] if row[stat] is not None else 0
            dataRow.append(rowStat)
            if(int(rowStat) > max_y):
                max_y = int(rowStat) + 10
        dataRows.append(dataRow)



    chart = SimpleLineChart(800, 250, y_range=[0, max_y])
        
    # add all the data
    for data in dataRows:
        chart.add_data(data)
    
    chart.set_legend(playerNames)

    # Set the line colour to blue
    chart.set_colours([random_colour() for name in topPlayerNames])
    
    # Set the vertical stripes
    #chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)
    
    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # The Y axis labels contains 0 to 100 skipping every 25, but remove the
    # first number because it's obvious and gets in the way of the first X
    # label.
    left_axis = range(0, max_y + 1, max_y/5)
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)
    
    rounds = scraperwiki.sqlite.execute("select distinct round from afl_2012.swdata")['data']
    roundLabels = ["R " + str(round[0]) for round in rounds]

    # X axis labels
    chart.set_axis_labels(Axis.BOTTOM, \
        roundLabels)

    return chart

def generateLinks():
    for i, d in enumerate(roundCountData):
        roundNum = str(d["round"])
        print '<a href="/run/afl_dreamteam/?round=' + roundNum + '">Round ' + roundNum + '</a>'
        if(i+1 != len(roundCountData)):
            print ' | '

    br()

    statColumns = ['points_avg_calc', 'points_avg','points_total', 'points_last_3_rounds_avg_calc', 'points_last_3_rounds_avg', 'rank_last_round', 'points_last_round']
    for i, statColumn in enumerate(statColumns):
        print '<a href="/run/afl_dreamteam/?round=' + str(round) + '&stats=' + statColumn + ('&search=%s&exact=%s' % (search, exact) if search != '' else '') + '">' + statColumn + '</a>'
        if(i+1 != len(statColumns)):
            print ' | '
    

def calculateSwaps(team, pointsCompareColumn):
    try:
        inFirst = {}
        outFirst = {}
        inSecond = {}
        outSecond = {}
        inThird = {}
        outThird = {}
        firstPointsDiff = 0
        secondPointsDiff = 0
        thirdPointsDiff = 0
    
        for player in team:
            playerInfo = scraperwiki.sqlite.select("* from swdata where round="+ str(round) + " and name like '%" + player + "%'")
            
            if len(playerInfo) != 0:
                # TODO Implement functionality to allow bi-position players to swap properly
                # I.e Handle defenders, midfielders, forwards, rucks all separately
                # At the moment if a player has position = "defender, midfielder" then they can only swap with other "defender, midfielder"'s
                possibleSwaps = scraperwiki.sqlite.select("* from swdata where round=" + str(round)
                + " and position like '%" + playerInfo[0]['position'] + "%' and price <= " + str(int(playerInfo[0]['price']) + kitty/2)
                + " and (name NOT like '%" + "%' or name NOT like '%".join(team) + "%' )")
        
                playerAvg = playerInfo[0][pointsCompareColumn]
                for swap in possibleSwaps:
                    swapPointsDiff = int(swap[pointsCompareColumn]) - int(playerAvg)
        
                    if firstPointsDiff < swapPointsDiff and swap['points_last_round'] != 0 and int(swap['games_played']) >= int(playerInfo[0]['games_played']) - 4:
                        
                        if(swap != inFirst and playerInfo[0] != outFirst):
                            # Assign first values to second
                            secondPointsDiff = firstPointsDiff
                            inSecond = inFirst
                            outSecond = outFirst
                        else:
                            # Assign first values to third
                            thirdPointsDiff = firstPointsDiff
                            inThird = inFirst
                            outThird = outFirst
        
                        # Now assign swap values to first
                        firstPointsDiff = swapPointsDiff              
                        inFirst = swap
                        outFirst = playerInfo[0]
    
                    elif(swap != inFirst and playerInfo[0] != outFirst and secondPointsDiff < swapPointsDiff and swap['points_last_round'] != 0 and swap['games_played'] >= playerInfo[0]['games_played']):
                        inSecond = swap
                        outSecond = playerInfo[0]
                        secondPointsDiff = swapPointsDiff
    
        
        if(len(inFirst) != 0):
            print "<b>Suggested Swaps for Dylan's Team in Round " + str(round) + " (Based on '" + pointsCompareColumn + "')</b>"
            br()
            print '<table class="draggable sortable" border="1" style="text-align: center;">' 
            print "<tr><th>Out</th><th>In</th><th>Compare Column</th><th>Points Avg</th><th>Points Total</th><th>Points Last 3 Rounds</th><th>Rank Last Round</th><th>Points Last Round</th><th>Selections</th><th>Price</th></tr>"
    
            for swap in [{'out':outFirst, 'in':inFirst}, {'out':outSecond, 'in':inSecond}]:
                print "<tr>"
                print "<td class='bad'>", searchUrl(swap['out']['name']),  "</td>"
                print "<td class='great'>", searchUrl(swap['in']['name']), "</td>"
                for improvement in [pointsCompareColumn, 'points_avg','points_total', 'points_last_3_rounds_avg', 'rank_last_round', 'points_last_round', 'num_selections', 'price']:
                    print "<td>", int(swap['in'][improvement]) - int(swap['out'][improvement]), "</td>"
                print "</tr>"
            print "</table>"
            br()
    
            print "<b><br />"
            
            newTeam = copy.deepcopy(team)
            newTeam.remove(re.sub(r"(\[*\])", "", outFirst['name']).strip())
            newTeam.remove(re.sub(r"(\[*\])", "", outSecond['name']).strip())
            newTeam.append(inFirst['name'])
            newTeam.append(inSecond['name'])
        
            print '<table class="draggable sortable" border="1" style="text-align: center;">' 
            print "<tr><th>Old</th><th>Proposed New</th></tr>"
            print "<tr>"
            print "<td class='bad'>"
            teamInfo(round, team, False)
            print "</td>"
            print "<td class='great'>"
            teamInfo(round, newTeam, False)
            print '</td>'
            print '</tr>'
            print '</table>'
            br()
    
            playerNames = [outFirst['name'], inFirst['name'], inSecond['name'], outSecond['name']]
            getChart(playerNames, stats)
    
            br()
            print "<b>Proposed Switch Players for Round " + str(round) + "</b><br />"
            playersTable([inFirst, outFirst, inSecond, outSecond])
    except Exception, e:
        print "Couldn't calculate swaps due to an exception: " + str(e)
        print "<br />"
            

def playersTable(data):
    print '<table class="draggable sortable" border="1" style="text-align: center;">'         
    print '<tr><th>No.</th><th>Position</th><th>Name</th><th>Team</th><th>Price</th><th>Rank</th><th>Points in Round</th><th>Calc Points Avg.</th><th>Points Avg.</th><th>Calc Points Avg. (Last 3 Rounds)</th><th>Points Avg. (Last 3 Rounds)</th><th>Points Total</th><th>Points (Highest)</th><th>Points (Lowest)</th><th>Games Played</th><th>Round</th><th>Value (Avg points per $100k)</th><th>Value (Total points per $100k)</th></tr>'
    for i, d in enumerate(data):
        print "<tr>"
        print "<td>", int(i+1), "</td>"
        print "<td>", d["position"], "</td>"
        print "<td>", d["name"], "</td>"
        print "<td>", d["team"], "</td>"
        print "<td>", '$' + str(d["price"]), "</td>"
        print "<td>", d["rank_last_round"], "</td>"
        print "<td>", d["points_last_round"], "</td>"
        print "<td>", "%.2f" % d["points_avg_calc"], "</td>"
        print "<td>", d["points_avg"], "</td>"
        print "<td>", "%.2f" % d["points_last_3_rounds_avg_calc"], "</td>"
        print "<td>", d["points_last_3_rounds_avg"], "</td>"
        print "<td>", d["points_total"], "</td>"
        print "<td>", d["points_highest"], "</td>"
        print "<td>", d["points_lowest"], "</td>"
        print "<td>", d["games_played"], "</td>"
        print "<td>", d["round"], "</td>"

        avgValue = int(d["points_avg"])*100*1000/int(d["price"])
        print "<td", "class='great'" if avgValue > 20 else '' , ">", avgValue, "</td>"

        totalValue = int(d["points_total"])*100*1000/int(d["price"])
        print "<td", "class='great'" if totalValue > 130 else '' , ">", totalValue, "</td>"
        print "</tr>"
    print "</table>"

def teamInfo(round, team, showTable):
    data = scraperwiki.sqlite.select("* from swdata where round="+ str(round) + " and (name like '%" + "%' or name like '%".join(team) + "%' )")
    
    if(showTable):
        playersTable(data)
        br()

    comparePredTotal = 0
    avgPredTotal = 0
    highestPredTotal = 0
    lowestPredTotal = 0
    totalSums = 0
    for d in data[:22]:
        comparePredTotal += int(d[stats])
        avgPredTotal += int(d["points_avg"])
        lowestPredTotal += int(d["points_lowest"])
        highestPredTotal += int(d["points_highest"])
        totalSums += int(d["points_total"])           
    comparePredTotal += int(data[0][stats])
    avgPredTotal +=  int(data[0]["points_avg"])
    highestPredTotal += int(data[0]["points_highest"])
    lowestPredTotal += int(data[0]["points_lowest"])
    totalSums += int(data[0]["points_total"])

    print "<b>Compare Col Predicted Total: </b>" + str(comparePredTotal) + "<br>"
    print "<b>Avg Predicted Total: </b>" + str(avgPredTotal) + "<br>"
    print "<b>Highest Predicted Total: </b>" + str(highestPredTotal)  + "<br>"
    print "<b>Lowest Predicted Total: </b>" + str(lowestPredTotal) + "<br>"
    print "<b>Total Sums: </b>" + str(totalSums) + "<br>"

def scraperStats():
    print "<b>Scraped Data Stats by Round</b><br />"
    print '<table class="draggable sortable" border="1" style="text-align: center;">'
    print '<tr><th>Round</th><th>Rows</th></tr>'
    for d in roundCountData:
        print "<tr>"
        print "<td>", d["round"], "</td>"
        print "<td>", d["count(round)"], "</td>"
        print "</tr>"
    print "</table>"

# --------- Page Generation ---------------------
def generatePage():
    print head
    print '<div class="header">'
    searchBar()
    print '<h2>Round ' + str(round) + ' Stats</h2>'
    generateLinks()
    print '</div>'
    br()

    if(search != ''):
        searchName(search)
    else:
        generateStats()
    br()

    # Footer
    print '<div class="footer">'
    generateLinks()
    print '</div>'
    print '</div>'
    print '</body>'
    print '</html>'

def generateStats():
    getChart(topPlayerNames, stats)
    br()
    calculateSwaps(team, stats)
    #calculateSwaps(team, 'points_last_3_rounds_avg_calc')
    #calculateSwaps(team, 'points_avg_calc')
    #calculateSwaps(team, 'points_avg')
    #calculateSwaps(team, 'points_avg')
    #calculateSwaps(team, 'games_played')
    #br()
    #calculateSwaps(team, 'points_total')
    #calculateSwaps(team, 'points_last_3_rounds_avg')
    #calculateSwaps(team, 'num_selections')
    #calculateSwaps(team, 'rank_last_round')
    #calculateSwaps(team, 'points_last_round')
    
    # Top 10 Players by rank
    br()
    print "<b>Top 10 Players by rank in Round " + str(round) + "</b><br />"
    playersTable(topPlayerData)
    br()
    
    print "<b>Team Stats for Round " + str(round) + "</b><br />"
    teamInfo(round, team, True)

    br()
    scraperStats()
    br()

def searchBar():

    print '<div align=right>'
    print '    <form action="/run/afl_dreamteam/" method="get">'
    print '        <input type="text" name="search" id="search" size="20" value="">'
    print '        <input type="submit" value="Search">'
    print '        <input type="hidden" name="stats" value="' + stats + '">'
    print '        <input type="hidden" name="exact" value="False">'
    print '    </form>'
    print '</div>'

def searchName(name):
    name.replace("'", "''")
    compareStr = "LIKE '%" + name + "%'" if exact == True else "='" + name + "'"
    searchData = scraperwiki.sqlite.select(
        "* from swdata" + \
        " where name " + compareStr + \
        " order by round limit 25")
    print "search: " + str(searchData)
    nameData = scraperwiki.sqlite.select(           
    "name from swdata"
    + " where name LIKE '%" + name
    + "%' group by name"
    )
    names = [aname['name'] for aname in nameData]
    print "<br />names: " + str(names)
    dataCount = len(searchData)
    nameCount = len(names)

    if(dataCount != 0):
        getChart(names, stats)

    br()
    print "<b>Search for " + name + "</b>"
    print "<br />"
    
    if(nameCount != 1):
        print str(nameCount) + " players found."
        
        print '<ol style="text-align: left;">'
        for player in names:
            print '<li><a class="black" href="/run/afl_dreamteam/?stats=' + stats + '&round=' + str(round) + '&search=' + player + '&exact=True">' + player + '</a></li>'
        print '</ol>'
    else:
        print str(dataCount) + " results found."
    
        if(dataCount != 0):
            br()
            playersTable(searchData)
    
def searchUrl(name):
    return '<a href="/run/afl_dreamteam/?round=' + str(round) + '&stats=' + stats + '&search=' + name + '&exact=True">' + name + '</a>'

def getChart(playerNames, stat, title = ""):
    global chartNo
    chartNo += 1
    container = "container" + str(chartNo)
    namesStr = "['" + "', '".join(playerNames) + "']"
    print '<script>'
    print """    document.write("<div id='""" + container + """' style='max-width: 80%; min-width: 400px; height: 300px; margin: 0 auto'></div>");"""
    print "      var chart = new aflChart('" + title + "', 'Based on " + stat + "', 'line', '" + container + "', " + namesStr + ', "' + stat + '");'
    print '    chart.build()'
    print '</script>'

generatePage()#!/usr/bin/python

# ------------ TODO: Save various swaps to database. No need to recalculate. (method column to describe calculation method, PKEY(method, round)
# ------------ TODO: Add compare function?

import scraperwiki    
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
import random
import cgi
import os
import copy
import re

scrapersource = 'afl_2012'       
scraperwiki.sqlite.attach(scrapersource)

queryString = os.getenv("QUERY_STRING", "")
round = ''
search  = ''
stats = 'points_avg_calc'
exact = False
if queryString != '':
    get = dict(cgi.parse_qsl(queryString))    
    round = get['round'] if get.has_key('round') else ''
    stats = get['stats'] if get.has_key('stats') else 'points_avg_calc'
    search = get['search'] if get.has_key('search') else ''
    if get.has_key('exact'):
        exact = True if get['exact'] == 'True' else False

round = round if round != '' else scraperwiki.sqlite.execute("select max(round) from afl_2012.swdata")['data'][0][0]

chartNo = 0

#-------------------------------------- Round 6 Team -----------------------------------------

kitty = 41000

defenders = ['Scotland, Heath', 'Goddard, Brendon', 'Hunt, Karmichael', 'Darley, Sam',
                     'Patfull, Joel', 'Smedts, Billie', 'Houli, Bachar' ] # 7 Defenders

midfielders = ['Boyd, Matthew', 'Stanton, Brent',
                'Pendlebury, Scott', 'Parker, Luke', 'Wingard, Chad', 'Kennedy, Adam'] # 6 Mids

rucks = ['Cox, Dean', 'Giles, Jonathan'] # 2 Rucks

forwards = ['Beams, Dayne [MID]', 'Whitecross, Brendan', 'Dangerfield, Patrick [MID]', 'Adams, Taylor',
            'Blair, Jarryd', 'Cornes, Chad', 'Goodes, Adam'] # 7 Forwards

reserves = ['Browne, Alex', 'Astbury, David',
            'Reid, Sam J.', 'Hogan, Simon',
            'Ryder, Patrick', 'Stephenson, Orren',
            'McKinley, Ben', 'Warren, Ben'] # 8 reserves

team = []
team += defenders
team += midfielders
team += rucks
team += forwards
#team += reserves

# -------------- Queries -------------------------

roundCountData = scraperwiki.sqlite.select(           
    'round, count(round) from swdata group by round'
)

topPlayerData = scraperwiki.sqlite.select(           
    '* from swdata'
    + ' where round = ' + str(round)
    + ' order by rank_last_round asc limit 10'
)

topPlayerNames = scraperwiki.sqlite.select(           
        'distinct name from swdata'
        + ' order by rank_last_round asc limit 5')

topPlayerNames = [name["name"] for name in topPlayerNames]

# ---------------- HTML Header -------------------------
head = \
'<html>' + \
'<head>' + \
    '<title>AFL Dream Team ~ Round ' + str(round) + (' | Search: %s' % search if search != '' else '')  + '</title>' + \
    '<script src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>' + \
    '<script src="http://www.danvk.org/dragtable/dragtable.js"></script>' + \
    '<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>' + \
    '<script src="http://code.highcharts.com/highcharts.js"></script>' + \
    '<script src="http://code.highcharts.com/modules/exporting.js"></script>' + \
'</head>' + \
'''<style type="text/css">

html, body{
    margin:0;
    background-color: white;
}

table, th, td, tr {
    padding: 5px;
    border-collapse: collapse;
    background-color: white;
    margin:0 auto;
}

th {
    background-color: 0033FF;
    color: white;
    padding: 5px;
}

div.header, div.footer {
    background-color: black;
    color: white;
    padding: 5px;
}

div.page {
    text-align: center;
    align: center;
    margin:0 auto;
    width: 1100px;
    height: 100%;
    background-color: white;
}

*.great {
    background-color: green;
    color: white;
}

*.bad {
    background-color: red;
    color: white;
}

a:link {color:white;}      /* unvisited link */
a:visited {color:gray;}  /* visited link */
a:hover {color:yellow;}  /* mouse over link */
a:active {color:orange;}  /* selected link */

a.black:link {color:black;}      /* unvisited link */
a.black:visited {color:gray;}  /* visited link */
a.black:hover {color:orange;}  /* mouse over link */
a.black:active {color:yellow;}  /* selected link */

</style>

<script>
    function aflChart(title, subtitle, type, container, names, comparison) {
        var comparison = comparison;
        var names = names;
        var title = title;
        var subtitle = subtitle;
        var type = type;
        var container = container;
        this.chart;
        
        var xAxisLabels = [];
        var dataSet = [];
            
        this.getPlayerData = function(name) {
            var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite";            
            var srcname = "afl_2012"; 
            var sqlselect = "select name, round, " + comparison + " from swdata where name='" + name + "'"; 
            return $.ajax({
                url: apiurl, 
                dataType: "jsonp", 
                data:{
                    name: srcname, 
                    query: sqlselect, 
                    format: "jsondict"
                }, 
                success: this.processJson
            });    
        };
        
        this.processJson = function(json) {
            var data = [];
            for(var i = 0; i < json.length; i++) {
                data.push(json[i][comparison]);
            }
            dataSet.push({name: json[0]["name"], data: data});
            
            // Do the xAxisLabels Separately
            for(var i = 0; i < json.length; i++) {
                xAxisLabels.push("R " + json[i]["round"]);
            }
            
            chart = createChart(title, subtitle, type, container, xAxisLabels, comparison, dataSet);
        }
        
        this.build = function() {
            var deferredCollection = [];
            for(i in names){
                deferredCollection.push(this.getPlayerData(names[i]));
            }
        }
    }
    
    function jsonTable(tdata)           
    {
        var keys = tdata["keys"]; 
        var data = tdata["data"]; 
        
        var table=document.getElementById("table");
        
        var header=table.insertRow(0);
        for(var i = 0; i < keys.length; i++){
            var cell=header.insertCell(i);
            cell.innerHTML=keys[i];
        }
        
        for (var i = 0; i < data.length; i++){
            var row=table.insertRow(i+1);
            for(var j = 0; j < data[0].length; j++){
                var cell=row.insertCell(j);
                cell.innerHTML=data[i][j];
            }
        }
    }
    
    function createChart(title, subtitle, type, divId, xAxisLabels, yAxisTitle, data) {
            return new Highcharts.Chart({
                chart: {
                    renderTo: divId,
                    type: type,
                    marginRight: 130,
                    marginBottom: 25
                },
                title: {
                    text: title,
                    x: -20 //center
                },
                subtitle: {
                    text: subtitle,
                    x: -20
                },
                xAxis: {
                    categories: xAxisLabels
                },
                yAxis: {
                    title: {
                        text: yAxisTitle
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'}]
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.series.name + '</b><br/>' + this.x + ': ' + this.y;
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -10,
                    y: 100,
                    borderWidth: 0
                },
                series: data
            });
    }</script>

<body>
<div class="page">'''

# ---------------- Methods -------------------------
def br():
    print "<br />"
    print "<br />"

def random_colour(min=20, max=200):
    func = lambda: int(random.random() * (max-min) + min)
    r, g, b = func(), func(), func()
    return '%02X%02X%02X' % (r, g, b)

def getChart2(playerNames, stat):
    # Set the vertical range from 0 to max_y
    max_y = 50

    dataRows = []

    for name in playerNames:
        rowSelection = scraperwiki.sqlite.select(
        'name, ' + stat + ' from swdata '
        + 'where name = \"' + name + '\"')

        dataRow = []
        for row in rowSelection:
            rowStat = row[stat] if row[stat] is not None else 0
            dataRow.append(rowStat)
            if(int(rowStat) > max_y):
                max_y = int(rowStat) + 10
        dataRows.append(dataRow)



    chart = SimpleLineChart(800, 250, y_range=[0, max_y])
        
    # add all the data
    for data in dataRows:
        chart.add_data(data)
    
    chart.set_legend(playerNames)

    # Set the line colour to blue
    chart.set_colours([random_colour() for name in topPlayerNames])
    
    # Set the vertical stripes
    #chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)
    
    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # The Y axis labels contains 0 to 100 skipping every 25, but remove the
    # first number because it's obvious and gets in the way of the first X
    # label.
    left_axis = range(0, max_y + 1, max_y/5)
    left_axis[0] = ''
    chart.set_axis_labels(Axis.LEFT, left_axis)
    
    rounds = scraperwiki.sqlite.execute("select distinct round from afl_2012.swdata")['data']
    roundLabels = ["R " + str(round[0]) for round in rounds]

    # X axis labels
    chart.set_axis_labels(Axis.BOTTOM, \
        roundLabels)

    return chart

def generateLinks():
    for i, d in enumerate(roundCountData):
        roundNum = str(d["round"])
        print '<a href="/run/afl_dreamteam/?round=' + roundNum + '">Round ' + roundNum + '</a>'
        if(i+1 != len(roundCountData)):
            print ' | '

    br()

    statColumns = ['points_avg_calc', 'points_avg','points_total', 'points_last_3_rounds_avg_calc', 'points_last_3_rounds_avg', 'rank_last_round', 'points_last_round']
    for i, statColumn in enumerate(statColumns):
        print '<a href="/run/afl_dreamteam/?round=' + str(round) + '&stats=' + statColumn + ('&search=%s&exact=%s' % (search, exact) if search != '' else '') + '">' + statColumn + '</a>'
        if(i+1 != len(statColumns)):
            print ' | '
    

def calculateSwaps(team, pointsCompareColumn):
    try:
        inFirst = {}
        outFirst = {}
        inSecond = {}
        outSecond = {}
        inThird = {}
        outThird = {}
        firstPointsDiff = 0
        secondPointsDiff = 0
        thirdPointsDiff = 0
    
        for player in team:
            playerInfo = scraperwiki.sqlite.select("* from swdata where round="+ str(round) + " and name like '%" + player + "%'")
            
            if len(playerInfo) != 0:
                # TODO Implement functionality to allow bi-position players to swap properly
                # I.e Handle defenders, midfielders, forwards, rucks all separately
                # At the moment if a player has position = "defender, midfielder" then they can only swap with other "defender, midfielder"'s
                possibleSwaps = scraperwiki.sqlite.select("* from swdata where round=" + str(round)
                + " and position like '%" + playerInfo[0]['position'] + "%' and price <= " + str(int(playerInfo[0]['price']) + kitty/2)
                + " and (name NOT like '%" + "%' or name NOT like '%".join(team) + "%' )")
        
                playerAvg = playerInfo[0][pointsCompareColumn]
                for swap in possibleSwaps:
                    swapPointsDiff = int(swap[pointsCompareColumn]) - int(playerAvg)
        
                    if firstPointsDiff < swapPointsDiff and swap['points_last_round'] != 0 and int(swap['games_played']) >= int(playerInfo[0]['games_played']) - 4:
                        
                        if(swap != inFirst and playerInfo[0] != outFirst):
                            # Assign first values to second
                            secondPointsDiff = firstPointsDiff
                            inSecond = inFirst
                            outSecond = outFirst
                        else:
                            # Assign first values to third
                            thirdPointsDiff = firstPointsDiff
                            inThird = inFirst
                            outThird = outFirst
        
                        # Now assign swap values to first
                        firstPointsDiff = swapPointsDiff              
                        inFirst = swap
                        outFirst = playerInfo[0]
    
                    elif(swap != inFirst and playerInfo[0] != outFirst and secondPointsDiff < swapPointsDiff and swap['points_last_round'] != 0 and swap['games_played'] >= playerInfo[0]['games_played']):
                        inSecond = swap
                        outSecond = playerInfo[0]
                        secondPointsDiff = swapPointsDiff
    
        
        if(len(inFirst) != 0):
            print "<b>Suggested Swaps for Dylan's Team in Round " + str(round) + " (Based on '" + pointsCompareColumn + "')</b>"
            br()
            print '<table class="draggable sortable" border="1" style="text-align: center;">' 
            print "<tr><th>Out</th><th>In</th><th>Compare Column</th><th>Points Avg</th><th>Points Total</th><th>Points Last 3 Rounds</th><th>Rank Last Round</th><th>Points Last Round</th><th>Selections</th><th>Price</th></tr>"
    
            for swap in [{'out':outFirst, 'in':inFirst}, {'out':outSecond, 'in':inSecond}]:
                print "<tr>"
                print "<td class='bad'>", searchUrl(swap['out']['name']),  "</td>"
                print "<td class='great'>", searchUrl(swap['in']['name']), "</td>"
                for improvement in [pointsCompareColumn, 'points_avg','points_total', 'points_last_3_rounds_avg', 'rank_last_round', 'points_last_round', 'num_selections', 'price']:
                    print "<td>", int(swap['in'][improvement]) - int(swap['out'][improvement]), "</td>"
                print "</tr>"
            print "</table>"
            br()
    
            print "<b><br />"
            
            newTeam = copy.deepcopy(team)
            newTeam.remove(re.sub(r"(\[*\])", "", outFirst['name']).strip())
            newTeam.remove(re.sub(r"(\[*\])", "", outSecond['name']).strip())
            newTeam.append(inFirst['name'])
            newTeam.append(inSecond['name'])
        
            print '<table class="draggable sortable" border="1" style="text-align: center;">' 
            print "<tr><th>Old</th><th>Proposed New</th></tr>"
            print "<tr>"
            print "<td class='bad'>"
            teamInfo(round, team, False)
            print "</td>"
            print "<td class='great'>"
            teamInfo(round, newTeam, False)
            print '</td>'
            print '</tr>'
            print '</table>'
            br()
    
            playerNames = [outFirst['name'], inFirst['name'], inSecond['name'], outSecond['name']]
            getChart(playerNames, stats)
    
            br()
            print "<b>Proposed Switch Players for Round " + str(round) + "</b><br />"
            playersTable([inFirst, outFirst, inSecond, outSecond])
    except Exception, e:
        print "Couldn't calculate swaps due to an exception: " + str(e)
        print "<br />"
            

def playersTable(data):
    print '<table class="draggable sortable" border="1" style="text-align: center;">'         
    print '<tr><th>No.</th><th>Position</th><th>Name</th><th>Team</th><th>Price</th><th>Rank</th><th>Points in Round</th><th>Calc Points Avg.</th><th>Points Avg.</th><th>Calc Points Avg. (Last 3 Rounds)</th><th>Points Avg. (Last 3 Rounds)</th><th>Points Total</th><th>Points (Highest)</th><th>Points (Lowest)</th><th>Games Played</th><th>Round</th><th>Value (Avg points per $100k)</th><th>Value (Total points per $100k)</th></tr>'
    for i, d in enumerate(data):
        print "<tr>"
        print "<td>", int(i+1), "</td>"
        print "<td>", d["position"], "</td>"
        print "<td>", d["name"], "</td>"
        print "<td>", d["team"], "</td>"
        print "<td>", '$' + str(d["price"]), "</td>"
        print "<td>", d["rank_last_round"], "</td>"
        print "<td>", d["points_last_round"], "</td>"
        print "<td>", "%.2f" % d["points_avg_calc"], "</td>"
        print "<td>", d["points_avg"], "</td>"
        print "<td>", "%.2f" % d["points_last_3_rounds_avg_calc"], "</td>"
        print "<td>", d["points_last_3_rounds_avg"], "</td>"
        print "<td>", d["points_total"], "</td>"
        print "<td>", d["points_highest"], "</td>"
        print "<td>", d["points_lowest"], "</td>"
        print "<td>", d["games_played"], "</td>"
        print "<td>", d["round"], "</td>"

        avgValue = int(d["points_avg"])*100*1000/int(d["price"])
        print "<td", "class='great'" if avgValue > 20 else '' , ">", avgValue, "</td>"

        totalValue = int(d["points_total"])*100*1000/int(d["price"])
        print "<td", "class='great'" if totalValue > 130 else '' , ">", totalValue, "</td>"
        print "</tr>"
    print "</table>"

def teamInfo(round, team, showTable):
    data = scraperwiki.sqlite.select("* from swdata where round="+ str(round) + " and (name like '%" + "%' or name like '%".join(team) + "%' )")
    
    if(showTable):
        playersTable(data)
        br()

    comparePredTotal = 0
    avgPredTotal = 0
    highestPredTotal = 0
    lowestPredTotal = 0
    totalSums = 0
    for d in data[:22]:
        comparePredTotal += int(d[stats])
        avgPredTotal += int(d["points_avg"])
        lowestPredTotal += int(d["points_lowest"])
        highestPredTotal += int(d["points_highest"])
        totalSums += int(d["points_total"])           
    comparePredTotal += int(data[0][stats])
    avgPredTotal +=  int(data[0]["points_avg"])
    highestPredTotal += int(data[0]["points_highest"])
    lowestPredTotal += int(data[0]["points_lowest"])
    totalSums += int(data[0]["points_total"])

    print "<b>Compare Col Predicted Total: </b>" + str(comparePredTotal) + "<br>"
    print "<b>Avg Predicted Total: </b>" + str(avgPredTotal) + "<br>"
    print "<b>Highest Predicted Total: </b>" + str(highestPredTotal)  + "<br>"
    print "<b>Lowest Predicted Total: </b>" + str(lowestPredTotal) + "<br>"
    print "<b>Total Sums: </b>" + str(totalSums) + "<br>"

def scraperStats():
    print "<b>Scraped Data Stats by Round</b><br />"
    print '<table class="draggable sortable" border="1" style="text-align: center;">'
    print '<tr><th>Round</th><th>Rows</th></tr>'
    for d in roundCountData:
        print "<tr>"
        print "<td>", d["round"], "</td>"
        print "<td>", d["count(round)"], "</td>"
        print "</tr>"
    print "</table>"

# --------- Page Generation ---------------------
def generatePage():
    print head
    print '<div class="header">'
    searchBar()
    print '<h2>Round ' + str(round) + ' Stats</h2>'
    generateLinks()
    print '</div>'
    br()

    if(search != ''):
        searchName(search)
    else:
        generateStats()
    br()

    # Footer
    print '<div class="footer">'
    generateLinks()
    print '</div>'
    print '</div>'
    print '</body>'
    print '</html>'

def generateStats():
    getChart(topPlayerNames, stats)
    br()
    calculateSwaps(team, stats)
    #calculateSwaps(team, 'points_last_3_rounds_avg_calc')
    #calculateSwaps(team, 'points_avg_calc')
    #calculateSwaps(team, 'points_avg')
    #calculateSwaps(team, 'points_avg')
    #calculateSwaps(team, 'games_played')
    #br()
    #calculateSwaps(team, 'points_total')
    #calculateSwaps(team, 'points_last_3_rounds_avg')
    #calculateSwaps(team, 'num_selections')
    #calculateSwaps(team, 'rank_last_round')
    #calculateSwaps(team, 'points_last_round')
    
    # Top 10 Players by rank
    br()
    print "<b>Top 10 Players by rank in Round " + str(round) + "</b><br />"
    playersTable(topPlayerData)
    br()
    
    print "<b>Team Stats for Round " + str(round) + "</b><br />"
    teamInfo(round, team, True)

    br()
    scraperStats()
    br()

def searchBar():

    print '<div align=right>'
    print '    <form action="/run/afl_dreamteam/" method="get">'
    print '        <input type="text" name="search" id="search" size="20" value="">'
    print '        <input type="submit" value="Search">'
    print '        <input type="hidden" name="stats" value="' + stats + '">'
    print '        <input type="hidden" name="exact" value="False">'
    print '    </form>'
    print '</div>'

def searchName(name):
    name.replace("'", "''")
    compareStr = "LIKE '%" + name + "%'" if exact == True else "='" + name + "'"
    searchData = scraperwiki.sqlite.select(
        "* from swdata" + \
        " where name " + compareStr + \
        " order by round limit 25")
    print "search: " + str(searchData)
    nameData = scraperwiki.sqlite.select(           
    "name from swdata"
    + " where name LIKE '%" + name
    + "%' group by name"
    )
    names = [aname['name'] for aname in nameData]
    print "<br />names: " + str(names)
    dataCount = len(searchData)
    nameCount = len(names)

    if(dataCount != 0):
        getChart(names, stats)

    br()
    print "<b>Search for " + name + "</b>"
    print "<br />"
    
    if(nameCount != 1):
        print str(nameCount) + " players found."
        
        print '<ol style="text-align: left;">'
        for player in names:
            print '<li><a class="black" href="/run/afl_dreamteam/?stats=' + stats + '&round=' + str(round) + '&search=' + player + '&exact=True">' + player + '</a></li>'
        print '</ol>'
    else:
        print str(dataCount) + " results found."
    
        if(dataCount != 0):
            br()
            playersTable(searchData)
    
def searchUrl(name):
    return '<a href="/run/afl_dreamteam/?round=' + str(round) + '&stats=' + stats + '&search=' + name + '&exact=True">' + name + '</a>'

def getChart(playerNames, stat, title = ""):
    global chartNo
    chartNo += 1
    container = "container" + str(chartNo)
    namesStr = "['" + "', '".join(playerNames) + "']"
    print '<script>'
    print """    document.write("<div id='""" + container + """' style='max-width: 80%; min-width: 400px; height: 300px; margin: 0 auto'></div>");"""
    print "      var chart = new aflChart('" + title + "', 'Based on " + stat + "', 'line', '" + container + "', " + namesStr + ', "' + stat + '");'
    print '    chart.build()'
    print '</script>'

generatePage()
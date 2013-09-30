import scraperwiki           
scraperwiki.sqlite.attach("foos_regard")

data = scraperwiki.sqlite.select(           
    '* from foos_regard.foosregard where team_red_score=10'
)
red_wins = len(data)
data = scraperwiki.sqlite.select(           
    '* from foos_regard.foosregard where team_yellow_score=10'
)
yellow_wins = len(data)

def get_teams():
    teams = {}
    for color in ('red', 'yellow'):
        data = scraperwiki.sqlite.select(           
            '* from foos_regard.foosregard where team_%(color)s_score=10 order by team_%(color)s' % {'color': color}
        )
        for row in data:
            update = True
            team_name = row['team_%s' % color]
            if team_name not in teams.keys():
                members = team_name.strip().split('  ')
                if len(members) == 2:
                    if '%s  %s' % (members[1], members[0]) in teams.keys():
                        team_name = '%s  %s' % (members[1], members[0])
                        update = False
                if update: teams.update({team_name: 0})
            teams[team_name] += int(row['team_%s_score' % color])
    return teams

teams = get_teams()
    

print '''
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawCharts);
      function drawCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn("string", "Team");
        data.addColumn("number", "Wins");
        data.addRows(['''
print "          ['Yellow',    ", yellow_wins, "],"
print "          ['Red',    ", red_wins, "],"
print "        ]);"
print """        var options = {
          width: 450, height: 300,
          title: 'Foosregard stats',
          colors: ['yellow', 'red']
        };"""

print '''
        var data2 = new google.visualization.DataTable();
        data2.addColumn("string", "Team");
        data2.addColumn("number", "Score");
        data2.addRows(['''
for team_name, score in teams.items():
    print "          ['%s', %d]," % (team_name, score)

print "        ]);"
print """        var options2 = {
          width: 450, height: 300,
          title: 'Best teams'
        };


        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        var chart2 = new google.visualization.PieChart(document.getElementById('chart2_div'));
        chart.draw(data, options);
        chart2.draw(data2, options2);
      }
    </script>
  </head>
  <body>
    <div id='chart_div'></div>
    <div id='chart2_div'></div>

  </body>
</html>"""




import scraperwiki           
scraperwiki.sqlite.attach("foos_regard")

data = scraperwiki.sqlite.select(           
    '* from foos_regard.foosregard where team_red_score=10'
)
red_wins = len(data)
data = scraperwiki.sqlite.select(           
    '* from foos_regard.foosregard where team_yellow_score=10'
)
yellow_wins = len(data)

def get_teams():
    teams = {}
    for color in ('red', 'yellow'):
        data = scraperwiki.sqlite.select(           
            '* from foos_regard.foosregard where team_%(color)s_score=10 order by team_%(color)s' % {'color': color}
        )
        for row in data:
            update = True
            team_name = row['team_%s' % color]
            if team_name not in teams.keys():
                members = team_name.strip().split('  ')
                if len(members) == 2:
                    if '%s  %s' % (members[1], members[0]) in teams.keys():
                        team_name = '%s  %s' % (members[1], members[0])
                        update = False
                if update: teams.update({team_name: 0})
            teams[team_name] += int(row['team_%s_score' % color])
    return teams

teams = get_teams()
    

print '''
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawCharts);
      function drawCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn("string", "Team");
        data.addColumn("number", "Wins");
        data.addRows(['''
print "          ['Yellow',    ", yellow_wins, "],"
print "          ['Red',    ", red_wins, "],"
print "        ]);"
print """        var options = {
          width: 450, height: 300,
          title: 'Foosregard stats',
          colors: ['yellow', 'red']
        };"""

print '''
        var data2 = new google.visualization.DataTable();
        data2.addColumn("string", "Team");
        data2.addColumn("number", "Score");
        data2.addRows(['''
for team_name, score in teams.items():
    print "          ['%s', %d]," % (team_name, score)

print "        ]);"
print """        var options2 = {
          width: 450, height: 300,
          title: 'Best teams'
        };


        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        var chart2 = new google.visualization.PieChart(document.getElementById('chart2_div'));
        chart.draw(data, options);
        chart2.draw(data2, options2);
      }
    </script>
  </head>
  <body>
    <div id='chart_div'></div>
    <div id='chart2_div'></div>

  </body>
</html>"""





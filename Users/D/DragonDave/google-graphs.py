import scraperwiki, json

a=[0,1,2]
print json.dumps(a)
exit()


def tablemassager(input, topleft='???'):
    def get(col,row):
        for item in input:
            if col==item[0] and row==item[1]:
                return item[2]

    # assumption: each row is three items; col, row and data
    # assumption: each col/row combo is unique
    # assumption: data is numbers.
    # try not to assume: each col/row combo is represented.
    cols=sorted(list(set([x[0] for x in input]))) # list/set gives only unique.
    rows=sorted(list(set([x[1] for x in input]))) # TODO: http://www.peterbe.com/plog/uniqifiers-benchmark #5
    builder=[]
    for row in rows:
        builder2=[row]
        for col in cols:
            builder2.append(get(col,row))
        builder.append(builder2)
    #cols.insert(0,topleft)
    #builder.insert(0,cols)
#    print builder
    return str(builder).replace('None', '0') # use JSON you moron.



# Blank Python
sourcescraper = 'ons-popestimates-by-year'
scraperwiki.sqlite.attach(sourcescraper, 'src')
data=scraperwiki.sqlite.select("age,areacode,pop from src.pop where pop.age != 'all' and pop.gender='all' limit 10000",  verbose=1)

#table=[[int(line['age']),line['areacode'], line['pop']] for line in data]
table=[[line['areacode'], int(line['age']),line['pop']] for line in data]
mtable=tablemassager(table)
# now to massage that table into a 2D table




    # NOTE: you can't use curved brackets - JS doesn't like them.
#table=sorted(table,key=lambda x:x[0])
#table.insert(0,['age','Durham'])


#table=[
#          ['Year', 'Sales', 'Expenses'],
#          ['2004',  1000,      400],
#          ['2005',  1170,      460],
#          ['2006',  660,       1120],
#          ['2007',  1030,      540]
#      ]

options = {'title': 'Company Performance'}

packages = {'packages':["corechart"]}

basehtml="""
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", %s);
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(%s);

        var options = %s;

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""

html=basehtml % (str(packages), mtable, str(options))

print html
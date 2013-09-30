####################################################################
# By simply setting the sourcescraper variable and selecting       #
#  an appropriate date field from sqlite table, this view will     #
#  draw                                                            #
#       -a google line chart of the field populations              #
#       -a bar chart of overall volume by date                     #
#  This will allow easy identification of changes/errors over time #
####################################################################

# POTENTIAL IMPROVEMENTS
# -format tooltips as %
# -display more dates on x-axis

import scraperwiki
import dateutil.parser
import gviz_api

sourcescraper = 'classic_fm_playlist_scraper'

###SET THIS TO NAME OF DATE COLUMN TO BE USED
datecol = 'Track Date'

charttitle = "'Field Population Percentages by Date for "+sourcescraper+"'"
dateaxis = "'"+datecol+"'"


htmlpage = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var json_data = new google.visualization.DataTable(%(json)s, 0.6);
        var options = {
          title: %(charttitle)s,
          titleTextStyle:{fontSize: 20},
          vAxes:{1:{title:'Total Record Volume',textStyle:{color: 'red',fontSize: 12}}, 0:{format:%(vaformat)s,title:'Pct Field Population',textStyle:{color: 'blue',fontSize: 12}}},
          hAxis: {title:%(dateaxis)s,slantedText:true, slantedTextAngle:90,showTextEvery:1, textStyle:{fontSize: 10}},

          seriesType: 'line',
          series: {0: {type: 'bars',targetAxisIndex:1,areaOpacity:0,color:'LightGray'}},
          legend:{position: 'bottom',textStyle:{fontSize: 12}}

        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));

        chart.draw(json_data, options);

      }
    </script>
  </head>
  <body>
    <div id='chart_div' style='width: 1400px; height: 600px;'></div>
  </body>
</html>
"""

#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach(sourcescraper)

#GET COLUMN LIST
popqry=  scraperwiki.sqlite.execute("SELECT * FROM swdata LIMIT 1")

#BUILD COLUMNS AND TABLE STRUCTURE

sel = ' ['+ datecol + '] as "DateColumn", count(*) as TotalVolume'

description = {}
description["DateColumn"] = ("date","DateColumn")
description["TotalVolume"] = ("number", "TotalVolume")

col_order = ["DateColumn","TotalVolume"]

#LOOP THROUGH TABLE COLUMNS TO BUILD SQL
#NULLIF-TRIM COMBO MAKES SURE THAT NON-NULL EMPTY AND SPACES ARE TREATED AS NULL 

for col in popqry['keys']:

    if col != datecol:
        sel  +=  ',COUNT(nullif(trim([' + col + ']),"")) as "' + col + '"'
        description[str(col)] = ("number", str(col))
        #col_order += ', "' + col + '"' 
        col_order.append(col)

sel += ' FROM swdata GROUP BY 1 ORDER BY 1 desc'


# N.B. THE RESULTS OF A .SELECT (DICT OF DICTS) IS DIFF FROM RESULTS OF A .EXECUTE!
#INITIATE SELECT STATEMENT
data = scraperwiki.sqlite.select(sel)

#IS THERE A BETTER WAY TO GET CORRECT VALUES OTHER THAN UPDATING DICT?

#loop through each row (i.e. each day)
for i in data:
    #reformat date as python date for correct ordering etc
    i['DateColumn'] = dateutil.parser.parse(i['DateColumn'])
    #get count of all records for each day
    dailyrecs = i['TotalVolume']
    #loop through all of the columns for eac
    for ind in i:
        if ind != 'DateColumn' and ind != 'TotalVolume':
            #calculate % population of field
            i[ind] = (float(i[ind])/float(dailyrecs))


#CREATE TABLE
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)


#TURN TABLE INTO JSON
json = data_table.ToJSon(columns_order=col_order,order_by=("DateColumn", "desc"))

# USING % IN JS SECTION CAUSES CONFLICT WITH PARAMETERS SO SET FORMAT
#  FOR VAXIS HERE AND PASS AS PARAM
vaformat = "'#,###%'"
 
print htmlpage % vars()

####################################################################
# By simply setting the sourcescraper variable and selecting       #
#  an appropriate date field from sqlite table, this view will     #
#  draw                                                            #
#       -a google line chart of the field populations              #
#       -a bar chart of overall volume by date                     #
#  This will allow easy identification of changes/errors over time #
####################################################################

# POTENTIAL IMPROVEMENTS
# -format tooltips as %
# -display more dates on x-axis

import scraperwiki
import dateutil.parser
import gviz_api

sourcescraper = 'classic_fm_playlist_scraper'

###SET THIS TO NAME OF DATE COLUMN TO BE USED
datecol = 'Track Date'

charttitle = "'Field Population Percentages by Date for "+sourcescraper+"'"
dateaxis = "'"+datecol+"'"


htmlpage = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var json_data = new google.visualization.DataTable(%(json)s, 0.6);
        var options = {
          title: %(charttitle)s,
          titleTextStyle:{fontSize: 20},
          vAxes:{1:{title:'Total Record Volume',textStyle:{color: 'red',fontSize: 12}}, 0:{format:%(vaformat)s,title:'Pct Field Population',textStyle:{color: 'blue',fontSize: 12}}},
          hAxis: {title:%(dateaxis)s,slantedText:true, slantedTextAngle:90,showTextEvery:1, textStyle:{fontSize: 10}},

          seriesType: 'line',
          series: {0: {type: 'bars',targetAxisIndex:1,areaOpacity:0,color:'LightGray'}},
          legend:{position: 'bottom',textStyle:{fontSize: 12}}

        };

        var chart = new google.visualization.ComboChart(document.getElementById('chart_div'));

        chart.draw(json_data, options);

      }
    </script>
  </head>
  <body>
    <div id='chart_div' style='width: 1400px; height: 600px;'></div>
  </body>
</html>
"""

#POINT AT CORRECT SCRAPER
scraperwiki.sqlite.attach(sourcescraper)

#GET COLUMN LIST
popqry=  scraperwiki.sqlite.execute("SELECT * FROM swdata LIMIT 1")

#BUILD COLUMNS AND TABLE STRUCTURE

sel = ' ['+ datecol + '] as "DateColumn", count(*) as TotalVolume'

description = {}
description["DateColumn"] = ("date","DateColumn")
description["TotalVolume"] = ("number", "TotalVolume")

col_order = ["DateColumn","TotalVolume"]

#LOOP THROUGH TABLE COLUMNS TO BUILD SQL
#NULLIF-TRIM COMBO MAKES SURE THAT NON-NULL EMPTY AND SPACES ARE TREATED AS NULL 

for col in popqry['keys']:

    if col != datecol:
        sel  +=  ',COUNT(nullif(trim([' + col + ']),"")) as "' + col + '"'
        description[str(col)] = ("number", str(col))
        #col_order += ', "' + col + '"' 
        col_order.append(col)

sel += ' FROM swdata GROUP BY 1 ORDER BY 1 desc'


# N.B. THE RESULTS OF A .SELECT (DICT OF DICTS) IS DIFF FROM RESULTS OF A .EXECUTE!
#INITIATE SELECT STATEMENT
data = scraperwiki.sqlite.select(sel)

#IS THERE A BETTER WAY TO GET CORRECT VALUES OTHER THAN UPDATING DICT?

#loop through each row (i.e. each day)
for i in data:
    #reformat date as python date for correct ordering etc
    i['DateColumn'] = dateutil.parser.parse(i['DateColumn'])
    #get count of all records for each day
    dailyrecs = i['TotalVolume']
    #loop through all of the columns for eac
    for ind in i:
        if ind != 'DateColumn' and ind != 'TotalVolume':
            #calculate % population of field
            i[ind] = (float(i[ind])/float(dailyrecs))


#CREATE TABLE
data_table = gviz_api.DataTable(description)
data_table.LoadData(data)


#TURN TABLE INTO JSON
json = data_table.ToJSon(columns_order=col_order,order_by=("DateColumn", "desc"))

# USING % IN JS SECTION CAUSES CONFLICT WITH PARAMETERS SO SET FORMAT
#  FOR VAXIS HERE AND PASS AS PARAM
vaformat = "'#,###%'"
 
print htmlpage % vars()


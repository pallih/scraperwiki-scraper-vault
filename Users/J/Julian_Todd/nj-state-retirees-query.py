import scraperwiki
import urllib
import datetime
import sqlite3
import tempfile
import os
import simplejson as json
import pygooglechart

temp = tempfile.NamedTemporaryFile()

def GetBarChartView(c, state, ccount):
    c.execute('''select count(*) as count, 
                   (case WHEN annualpension<5000 THEN 'a 0<5k' 
                        WHEN annualpension<10000 THEN 'b 5k-10k' 
                        WHEN annualpension<20000 THEN 'c 10k-20k' 
                        WHEN annualpension<30000 THEN 'd 20k-30k' 
                        WHEN annualpension<40000 THEN 'e 30k-40k' 
                        WHEN annualpension<50000 THEN 'f 40k-50k' 
                        WHEN annualpension<60000 THEN 'g 50k-60k' 
                        ELSE 'h +60k' END) as pensionband, 
                 avg(annualpension), avg(finalsalary) 
                 from njpension
                 where state=?
                 group by pensionband
                 order by pensionband
              ''', (state,))
    
    rows = list(c)

    yrange = max(60, int(ccount*0.5))
    chart = pygooglechart.StackedVerticalBarChart(150, 50, y_range=(0, yrange), colours=["556600"])
    chart.set_bar_width(13)
    axisbottom = [r[1][-3:-1]  for r in rows]
    axisbottom[-1] = ">60"
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, axisbottom)
    chart.add_data([r[0]  for r in rows])
    return chart.get_url()
    

def Main():
    contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/njstateretirees").read()
    open(temp.name, "wb").write(contents)

    conn = sqlite3.connect(temp.name)
    c = conn.cursor()

    print "<html><body>"
    print "<h4>Top 10 states for New Jersey state employees to live</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>State</th><th>Final<br/>salary</th><th>Average<br/>pension</th>"
    print "<th>Income<br/>distribution</th></tr>"

    c.execute('''select count(*) as count, state, avg(finalsalary), avg(annualpension) 
                 from njpension
                 group by state 
                 order by count desc
                 limit 15
                 ''')
    for row in list(c):
        cimg = GetBarChartView(c, row[1], row[0])
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td>" % row
        print '<td><img src="%s"></td></tr>' % cimg
    print "</table>"
    
    print "<br>"
    print "<h4>Per year retirees</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>Year</th><th>Average<br/>pension</th><th>Average<br/>Final<br/>salary</th></tr>"
    
    c.execute('''select count(*) as count, strftime('%Y', dateretire) as year, avg(annualpension), avg(finalsalary)
                 from njpension
                 group by year 
                 order by year
                 ''')
    for row in c:
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td></tr>" % row
    print "</table>"

    
Main()

def ShowFunc(v):
    print "<h1>Hi there: %s</h1>" % v

import scraperwiki
import urllib
import datetime
import sqlite3
import tempfile
import os
import simplejson as json
import pygooglechart

temp = tempfile.NamedTemporaryFile()

def GetBarChartView(c, state, ccount):
    c.execute('''select count(*) as count, 
                   (case WHEN annualpension<5000 THEN 'a 0<5k' 
                        WHEN annualpension<10000 THEN 'b 5k-10k' 
                        WHEN annualpension<20000 THEN 'c 10k-20k' 
                        WHEN annualpension<30000 THEN 'd 20k-30k' 
                        WHEN annualpension<40000 THEN 'e 30k-40k' 
                        WHEN annualpension<50000 THEN 'f 40k-50k' 
                        WHEN annualpension<60000 THEN 'g 50k-60k' 
                        ELSE 'h +60k' END) as pensionband, 
                 avg(annualpension), avg(finalsalary) 
                 from njpension
                 where state=?
                 group by pensionband
                 order by pensionband
              ''', (state,))
    
    rows = list(c)

    yrange = max(60, int(ccount*0.5))
    chart = pygooglechart.StackedVerticalBarChart(150, 50, y_range=(0, yrange), colours=["556600"])
    chart.set_bar_width(13)
    axisbottom = [r[1][-3:-1]  for r in rows]
    axisbottom[-1] = ">60"
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, axisbottom)
    chart.add_data([r[0]  for r in rows])
    return chart.get_url()
    

def Main():
    contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/njstateretirees").read()
    open(temp.name, "wb").write(contents)

    conn = sqlite3.connect(temp.name)
    c = conn.cursor()

    print "<html><body>"
    print "<h4>Top 10 states for New Jersey state employees to live</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>State</th><th>Final<br/>salary</th><th>Average<br/>pension</th>"
    print "<th>Income<br/>distribution</th></tr>"

    c.execute('''select count(*) as count, state, avg(finalsalary), avg(annualpension) 
                 from njpension
                 group by state 
                 order by count desc
                 limit 15
                 ''')
    for row in list(c):
        cimg = GetBarChartView(c, row[1], row[0])
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td>" % row
        print '<td><img src="%s"></td></tr>' % cimg
    print "</table>"
    
    print "<br>"
    print "<h4>Per year retirees</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>Year</th><th>Average<br/>pension</th><th>Average<br/>Final<br/>salary</th></tr>"
    
    c.execute('''select count(*) as count, strftime('%Y', dateretire) as year, avg(annualpension), avg(finalsalary)
                 from njpension
                 group by year 
                 order by year
                 ''')
    for row in c:
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td></tr>" % row
    print "</table>"

    
Main()

def ShowFunc(v):
    print "<h1>Hi there: %s</h1>" % v

import scraperwiki
import urllib
import datetime
import sqlite3
import tempfile
import os
import simplejson as json
import pygooglechart

temp = tempfile.NamedTemporaryFile()

def GetBarChartView(c, state, ccount):
    c.execute('''select count(*) as count, 
                   (case WHEN annualpension<5000 THEN 'a 0<5k' 
                        WHEN annualpension<10000 THEN 'b 5k-10k' 
                        WHEN annualpension<20000 THEN 'c 10k-20k' 
                        WHEN annualpension<30000 THEN 'd 20k-30k' 
                        WHEN annualpension<40000 THEN 'e 30k-40k' 
                        WHEN annualpension<50000 THEN 'f 40k-50k' 
                        WHEN annualpension<60000 THEN 'g 50k-60k' 
                        ELSE 'h +60k' END) as pensionband, 
                 avg(annualpension), avg(finalsalary) 
                 from njpension
                 where state=?
                 group by pensionband
                 order by pensionband
              ''', (state,))
    
    rows = list(c)

    yrange = max(60, int(ccount*0.5))
    chart = pygooglechart.StackedVerticalBarChart(150, 50, y_range=(0, yrange), colours=["556600"])
    chart.set_bar_width(13)
    axisbottom = [r[1][-3:-1]  for r in rows]
    axisbottom[-1] = ">60"
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, axisbottom)
    chart.add_data([r[0]  for r in rows])
    return chart.get_url()
    

def Main():
    contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/njstateretirees").read()
    open(temp.name, "wb").write(contents)

    conn = sqlite3.connect(temp.name)
    c = conn.cursor()

    print "<html><body>"
    print "<h4>Top 10 states for New Jersey state employees to live</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>State</th><th>Final<br/>salary</th><th>Average<br/>pension</th>"
    print "<th>Income<br/>distribution</th></tr>"

    c.execute('''select count(*) as count, state, avg(finalsalary), avg(annualpension) 
                 from njpension
                 group by state 
                 order by count desc
                 limit 15
                 ''')
    for row in list(c):
        cimg = GetBarChartView(c, row[1], row[0])
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td>" % row
        print '<td><img src="%s"></td></tr>' % cimg
    print "</table>"
    
    print "<br>"
    print "<h4>Per year retirees</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>Year</th><th>Average<br/>pension</th><th>Average<br/>Final<br/>salary</th></tr>"
    
    c.execute('''select count(*) as count, strftime('%Y', dateretire) as year, avg(annualpension), avg(finalsalary)
                 from njpension
                 group by year 
                 order by year
                 ''')
    for row in c:
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td></tr>" % row
    print "</table>"

    
Main()

def ShowFunc(v):
    print "<h1>Hi there: %s</h1>" % v

import scraperwiki
import urllib
import datetime
import sqlite3
import tempfile
import os
import simplejson as json
import pygooglechart

temp = tempfile.NamedTemporaryFile()

def GetBarChartView(c, state, ccount):
    c.execute('''select count(*) as count, 
                   (case WHEN annualpension<5000 THEN 'a 0<5k' 
                        WHEN annualpension<10000 THEN 'b 5k-10k' 
                        WHEN annualpension<20000 THEN 'c 10k-20k' 
                        WHEN annualpension<30000 THEN 'd 20k-30k' 
                        WHEN annualpension<40000 THEN 'e 30k-40k' 
                        WHEN annualpension<50000 THEN 'f 40k-50k' 
                        WHEN annualpension<60000 THEN 'g 50k-60k' 
                        ELSE 'h +60k' END) as pensionband, 
                 avg(annualpension), avg(finalsalary) 
                 from njpension
                 where state=?
                 group by pensionband
                 order by pensionband
              ''', (state,))
    
    rows = list(c)

    yrange = max(60, int(ccount*0.5))
    chart = pygooglechart.StackedVerticalBarChart(150, 50, y_range=(0, yrange), colours=["556600"])
    chart.set_bar_width(13)
    axisbottom = [r[1][-3:-1]  for r in rows]
    axisbottom[-1] = ">60"
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, axisbottom)
    chart.add_data([r[0]  for r in rows])
    return chart.get_url()
    

def Main():
    contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/njstateretirees").read()
    open(temp.name, "wb").write(contents)

    conn = sqlite3.connect(temp.name)
    c = conn.cursor()

    print "<html><body>"
    print "<h4>Top 10 states for New Jersey state employees to live</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>State</th><th>Final<br/>salary</th><th>Average<br/>pension</th>"
    print "<th>Income<br/>distribution</th></tr>"

    c.execute('''select count(*) as count, state, avg(finalsalary), avg(annualpension) 
                 from njpension
                 group by state 
                 order by count desc
                 limit 15
                 ''')
    for row in list(c):
        cimg = GetBarChartView(c, row[1], row[0])
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td>" % row
        print '<td><img src="%s"></td></tr>' % cimg
    print "</table>"
    
    print "<br>"
    print "<h4>Per year retirees</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>Year</th><th>Average<br/>pension</th><th>Average<br/>Final<br/>salary</th></tr>"
    
    c.execute('''select count(*) as count, strftime('%Y', dateretire) as year, avg(annualpension), avg(finalsalary)
                 from njpension
                 group by year 
                 order by year
                 ''')
    for row in c:
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td></tr>" % row
    print "</table>"

    
Main()

def ShowFunc(v):
    print "<h1>Hi there: %s</h1>" % v

import scraperwiki
import urllib
import datetime
import sqlite3
import tempfile
import os
import simplejson as json
import pygooglechart

temp = tempfile.NamedTemporaryFile()

def GetBarChartView(c, state, ccount):
    c.execute('''select count(*) as count, 
                   (case WHEN annualpension<5000 THEN 'a 0<5k' 
                        WHEN annualpension<10000 THEN 'b 5k-10k' 
                        WHEN annualpension<20000 THEN 'c 10k-20k' 
                        WHEN annualpension<30000 THEN 'd 20k-30k' 
                        WHEN annualpension<40000 THEN 'e 30k-40k' 
                        WHEN annualpension<50000 THEN 'f 40k-50k' 
                        WHEN annualpension<60000 THEN 'g 50k-60k' 
                        ELSE 'h +60k' END) as pensionband, 
                 avg(annualpension), avg(finalsalary) 
                 from njpension
                 where state=?
                 group by pensionband
                 order by pensionband
              ''', (state,))
    
    rows = list(c)

    yrange = max(60, int(ccount*0.5))
    chart = pygooglechart.StackedVerticalBarChart(150, 50, y_range=(0, yrange), colours=["556600"])
    chart.set_bar_width(13)
    axisbottom = [r[1][-3:-1]  for r in rows]
    axisbottom[-1] = ">60"
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, axisbottom)
    chart.add_data([r[0]  for r in rows])
    return chart.get_url()
    

def Main():
    contents = urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/njstateretirees").read()
    open(temp.name, "wb").write(contents)

    conn = sqlite3.connect(temp.name)
    c = conn.cursor()

    print "<html><body>"
    print "<h4>Top 10 states for New Jersey state employees to live</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>State</th><th>Final<br/>salary</th><th>Average<br/>pension</th>"
    print "<th>Income<br/>distribution</th></tr>"

    c.execute('''select count(*) as count, state, avg(finalsalary), avg(annualpension) 
                 from njpension
                 group by state 
                 order by count desc
                 limit 15
                 ''')
    for row in list(c):
        cimg = GetBarChartView(c, row[1], row[0])
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td>" % row
        print '<td><img src="%s"></td></tr>' % cimg
    print "</table>"
    
    print "<br>"
    print "<h4>Per year retirees</h4>"
    print '<table style="background-color:#d0ffd0">'
    print "<tr><th>Number</th><th>Year</th><th>Average<br/>pension</th><th>Average<br/>Final<br/>salary</th></tr>"
    
    c.execute('''select count(*) as count, strftime('%Y', dateretire) as year, avg(annualpension), avg(finalsalary)
                 from njpension
                 group by year 
                 order by year
                 ''')
    for row in c:
        print "<tr><td>%d</td><td>%s</td><td>%.0f</td><td>%.0f</td></tr>" % row
    print "</table>"

    
Main()

def ShowFunc(v):
    print "<h1>Hi there: %s</h1>" % v


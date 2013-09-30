import scraperwiki 
from pygooglechart import PieChart2D

scraperwiki.sqlite.attach('deputati')

def chart_MF(gruppo, data):
    f = sum(1 for i in data['data'] if i[0] == 'F' and i[1] == gruppo)
    m = sum(1 for i in data['data'] if i[0] == 'M' and i[1] == gruppo)
    chart = PieChart2D(400, 200)
    chart.add_data([f, m])
    chart.set_pie_labels(['F=' + str(f), 'M=' + str(m)])
    chart.set_title(gruppo)
    chart.set_colours(['FF0000', '0000FF'])
    print "<img src='%s'>" % chart.get_url()


data = scraperwiki.sqlite.execute("select sesso,gruppo from swdata")
gruppi = ["M5S", "PDL", "PD", "SEL", "SCPI", "FDI", "LNA", "MISTO"]
for i in gruppi:
    chart_MF(i, data)

import scraperwiki 
from pygooglechart import PieChart2D

scraperwiki.sqlite.attach('deputati')

def chart_MF(gruppo, data):
    f = sum(1 for i in data['data'] if i[0] == 'F' and i[1] == gruppo)
    m = sum(1 for i in data['data'] if i[0] == 'M' and i[1] == gruppo)
    chart = PieChart2D(400, 200)
    chart.add_data([f, m])
    chart.set_pie_labels(['F=' + str(f), 'M=' + str(m)])
    chart.set_title(gruppo)
    chart.set_colours(['FF0000', '0000FF'])
    print "<img src='%s'>" % chart.get_url()


data = scraperwiki.sqlite.execute("select sesso,gruppo from swdata")
gruppi = ["M5S", "PDL", "PD", "SEL", "SCPI", "FDI", "LNA", "MISTO"]
for i in gruppi:
    chart_MF(i, data)


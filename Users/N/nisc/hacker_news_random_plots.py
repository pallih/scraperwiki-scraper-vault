import scraperwiki.sqlite
import pygooglechart

SOURCESCRAPER = "hacker_news_management_summary"

scraperwiki.sqlite.attach(SOURCESCRAPER, "src")

sdata = scraperwiki.sqlite.execute("select num_comments, points, age from src.swdata")
keys = sdata.get('keys')
rows = sdata.get('data')

# scatterplot: num comments vs score
y = [row[0] for row in rows if str(row[0]).isdigit()]
x = [row[1] for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+100), 100))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+25), 25))
chart.set_title("points vs. num_comments")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()

# scatterplot: age (days) vs num_comments
y = [row[0] for row in rows if str(row[0]).isdigit()]
x = [int(row[2].split()[0]) if row[2].split()[1].startswith("day") else 1 for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+25), 25))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+25), 25))
chart.set_title("age (days) vs. num_comments")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()

# scatterplot: age (days) vs points
y = [row[1] for row in rows if str(row[0]).isdigit()]
x = [int(row[2].split()[0]) if row[2].split()[1].startswith("day") else 1 for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+25), 25))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+50), 50))
chart.set_title("age (days) vs. points")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()import scraperwiki.sqlite
import pygooglechart

SOURCESCRAPER = "hacker_news_management_summary"

scraperwiki.sqlite.attach(SOURCESCRAPER, "src")

sdata = scraperwiki.sqlite.execute("select num_comments, points, age from src.swdata")
keys = sdata.get('keys')
rows = sdata.get('data')

# scatterplot: num comments vs score
y = [row[0] for row in rows if str(row[0]).isdigit()]
x = [row[1] for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+100), 100))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+25), 25))
chart.set_title("points vs. num_comments")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()

# scatterplot: age (days) vs num_comments
y = [row[0] for row in rows if str(row[0]).isdigit()]
x = [int(row[2].split()[0]) if row[2].split()[1].startswith("day") else 1 for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+25), 25))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+25), 25))
chart.set_title("age (days) vs. num_comments")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()

# scatterplot: age (days) vs points
y = [row[1] for row in rows if str(row[0]).isdigit()]
x = [int(row[2].split()[0]) if row[2].split()[1].startswith("day") else 1 for row in rows if str(row[0]).isdigit()]
z = [1]*len(y)

chart = pygooglechart.ScatterChart(400, 400)
chart.set_axis_labels(pygooglechart.Axis.BOTTOM, range(0, (max(x)+25), 25))
chart.set_axis_labels(pygooglechart.Axis.LEFT, range(0, (max(y)+50), 50))
chart.set_title("age (days) vs. points")
for row in rows:
    chart.add_data(x)
    chart.add_data(y)
    chart.add_data(z)

print "<img src='%s' />" % chart.get_url()
# some simple google charts

from pygooglechart import Chart
from pygooglechart import StackedVerticalBarChart, SimpleLineChart
from pygooglechart import Axis


#
# the most simple line chart
#
def simplestChart(data):
    chart = SimpleLineChart(200, 125, y_range=[min(data), max(data)])
    chart.add_data(data)
    return chart

#
# simple line chart with labels
#
def simpleChart(bottom_labels, data):
    # round min and max to nearest integers
    datamin = int(min(data) - 0.5)
    datamax = int(max(data) + 0.5)
    chart = SimpleLineChart(200, 125, y_range=[datamin, datamax])
    chart.add_data(data)
    
    left_axis = [datamin,0,datamax]
    chart.set_axis_labels(Axis.LEFT, left_axis)
    chart.set_axis_labels(Axis.BOTTOM, bottom_labels) 
    return chart

#
# simple line chart with more labels
#
def simpleChart1(bottom_labels, data):
    # round min and max to nearest integers
    datamin = int(min(data) - 0.5)
    datamax = int(max(data) + 0.5)
    chart = SimpleLineChart(200, 125, y_range=[datamin, datamax])
    chart.add_data(data)
    
    left_axis = [datamin,0,datamax]

    chart.set_axis_labels(Axis.LEFT, left_axis)
    chart.set_axis_labels(Axis.BOTTOM, bottom_labels)
    chart.set_axis_labels(Axis.BOTTOM, ['X Axis']) # second label below first one
    chart.set_axis_positions(2, [50.0]) # position, left is 0., right is 100., 50. is center
    return chart
 
#
# simple line chart 2 labels, more decoration
#
def simpleChart2(bottom_labels, data):
    # round min and max to nearest integers
    datamin = int(min(data) - 0.5)
    datamax = int(max(data) + 0.5)
    
    chart = SimpleLineChart(200, 125, y_range=[datamin, datamax])
    chart.add_data(data)    

    left_axis = ['min',0,'max']
    chart.set_axis_labels(Axis.LEFT, left_axis)
    chart.set_axis_labels(Axis.BOTTOM, bottom_labels)
    chart.set_axis_labels(Axis.BOTTOM, ['X Axis']) # second label below first one
    chart.set_axis_positions(2, [50.0]) # position, left is 0., right is 100., 50. is center

    # Set the line colour
    chart.set_colours(['0000FF'])

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # Set vertical stripes
    stripes = ['CCCCCC', 0.2, 'FFFFFF', 0.2]
    chart.fill_linear_stripes(Chart.CHART, 0, *stripes)
    return chart
 
#
# simple line chart 2 labels, 2 datasets, decoration
#
def simpleChart3(bottom_labels, data1, data2):
    datamin, datamax = min(min(data1, data2)), max(max(data1, data2))
    datamin = int(datamin - 0.5)
    datamax = int(datamax + 0.5)
    chart = SimpleLineChart(200, 125, y_range=[datamin, datamax])
    chart.add_data(data1)
    chart.add_data(data2)
    
    left_axis = [datamin,0,datamax]

    left_axis[0] = '' # no label at 0
    chart.set_axis_labels(Axis.LEFT, left_axis)
    chart.set_axis_labels(Axis.BOTTOM, bottom_labels)
    chart.set_axis_labels(Axis.BOTTOM, ['X Axis']) # second label below first one
    chart.set_axis_positions(2, [50.0]) # position, left is 0., right is 100., 50. is center

    # Set the line colour
    chart.set_colours(['0000FF', 'FF0000'])

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # Set vertical stripes
    stripes = ['CCCCCC', 0.2, 'FFFFFF', 0.2]
    chart.fill_linear_stripes(Chart.CHART, 0, *stripes)
    return chart
    
#
# simple line chart 2 labels, 2 datasets, decoration
#
def simpleChart3legend(bottom_labels, data1, legend1, data2, legend2):
    datamin, datamax = min(min(data1, data2)), max(max(data1, data2))
    datamin = int(datamin - 0.5)
    datamax = int(datamax + 0.5)
    chart = SimpleLineChart(200, 125, y_range=[datamin, datamax])
    chart.add_data(data1)
    chart.add_data(data2)
    
    left_axis = [datamin,0,datamax]

    left_axis[0] = '' # no label at 0
    chart.set_axis_labels(Axis.LEFT, left_axis)
    chart.set_axis_labels(Axis.BOTTOM, bottom_labels)
    chart.set_axis_labels(Axis.BOTTOM, ['X Axis']) # second label below first one
    chart.set_axis_positions(2, [50.0]) # position, left is 0., right is 100., 50. is center

    # Set the line colour
    chart.set_colours(['0000FF', 'FF0000'])

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # Set vertical stripes
    stripes = ['CCCCCC', 0.2, 'FFFFFF', 0.2]
    chart.fill_linear_stripes(Chart.CHART, 0, *stripes)

    # legend
    chart.set_legend([legend1, legend2])
    return chart
    

# generate some data
import math
f_x = [ ]
xvals = [ ]
x = -10.
while x <= 10.:
    xvals.append(x)
    f_x.append(math.sin(x))
    x += 0.1

# build these charts    
charts = [ ]
charts.append(simplestChart(f_x))
charts.append(simpleChart([-10,0,10], f_x))
charts.append(simpleChart1([-10,0,10], f_x))
charts.append(simpleChart2([-10,0,10], f_x))
charts.append(simpleChart3([-10,0,10], f_x, [(math.cos(x) * 0.1 * x) for x in xvals]))
charts.append(simpleChart3legend([-10,0,10], f_x, 'sin(x)', [(math.cos(x) * 0.1 * x) for x in xvals], 'x * cos(x)/10'))

# draw the charts using images in a basic html table
cols = 2
print '<table cellspacing="20">'
for ic in range(len(charts)):
    if ic % cols == 0:
        print '%s<tr>' % ic != 0 and '</tr>' or '' 
    print '<td><img src="%s"></img></td>' % charts[ic].get_url()
print '</tr></table>'


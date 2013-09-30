# this could do with an overhaul and be made into a dynamic webpage.
# the charts only seem to fit ca. 1 year, I have hardcoded the start date in the query
# see 'def LoadData'



import scraperwiki
import time, datetime

from pygooglechart import Chart
from pygooglechart import GroupedVerticalBarChart, SimpleLineChart
from pygooglechart import Axis


scrapername = 'wienerluft'
months = ['Jan', 'Feb', 'Apr', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def assertSunday(days):
    global firstday
    vd = firstday + datetime.timedelta(days)
    t = time.mktime((vd.year, vd.month, vd.day, 0, 0, 0, 0, 0, 0))
    assert time.strftime("%w", time.gmtime(t)) == '0'
    

def genColourRange(ncols, rgbfrom = (1.0, 0.9, 0.9), rgbto = (0.9, 0.9, 1.0)):
    import colorsys
    hsvfrom = colorsys.rgb_to_hsv(*rgbfrom)
    hsvto = colorsys.rgb_to_hsv(*rgbto)
    colsteps = ((hsvto[0] - hsvfrom[0])/(ncols - 1), (hsvto[1] - hsvfrom[1])/(ncols - 1), (hsvto[2] - hsvfrom[2])/(ncols - 1))
    colrange = [ ]
    for i in range(ncols):
        hsv = (hsvfrom[0] + i * colsteps[0], hsvfrom[1] + i * colsteps[1], hsvfrom[2] + i * colsteps[2])
        rgb = colorsys.hsv_to_rgb(*hsv)
        strrgb = '%.2x%.2x%.2x' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colrange.append(strrgb)
    return colrange       

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    #l = list(scraperwiki.apiwrapper.getData(scrapername))
    scraperwiki.sqlite.attach(scrapername)
    l = scraperwiki.sqlite.select("* from swdata where Date > 20120000") # THIS IS HARDCODED TO GET DATA FOR 2012
    return l[::-1] # reverse the list

def createChart(title, xaxis, datay, firstweekday):

    # Find the max y value
    max_y = None
    for dd in datay.values():
        max_y = max(max_y, max(dd))

    # Chart size of 400x250 pixels and specifying the range for the Y axis
    if title:
        chart = SimpleLineChart(1000, 250, title=title, y_range=[0, max_y])
    else:
        chart = SimpleLineChart(1000, 250, y_range=[0, max_y])
    
    # add the data
    for dd in datay.values():
        chart.add_data(dd)

    # Set the line colours
    chart.set_colours(['0000FF', 'FF0000', '00FF00', 'F0F000', '0F0F00'])

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # vertical stripes, the width of each stripe is calculated so that it covers one month
    ndatapoints = len(datay.values()[0])
            
    datapermonth = [ ]
    for year in xaxis:
        for month in xaxis[year]:
            datapermonth.append(xaxis[year][month])


    # mark months using range markers
    stripes = [ ]
    stripcols = ('FFFFFF', 'CCCCCC')
    wlast = 0
    for k in datapermonth:
        w = k * 1.0 / ndatapoints
        icol = len(stripes)/2 % 2
        stripes.append(stripcols[icol])
        stripes.append(w)
        wlast += w
    chart.fill_linear_stripes(Chart.CHART, 0, *stripes)

    # y axis labels
    if max_y > 30:
        left_axis = range(0, int(max_y) + 1, 5)
    elif max_y > 10:
        left_axis = range(0, int(max_y) + 1, 1)
    elif max_y > 5:
        left_axis = [ ]
        v = 0.
        while v < max_y + 0.5:
            left_axis.append(v)
            v += 0.5
    else:
        left_axis = [ ]
        v = 0.
        while v < max_y + 0.1:
            left_axis.append(v)
            v += 0.1

    left_axis[0] = '' # no label at 0
    chart.set_axis_labels(Axis.LEFT, left_axis)

    # X axis labels
    monthlabels = [ ]
    for year in xaxis:
        for imonth in xaxis[year]:
            monthlabels.append(months[imonth])

    chart.set_axis_labels(Axis.BOTTOM, monthlabels)
    chart.set_axis_labels(Axis.BOTTOM, xaxis.keys()) # years
    
    # the axis is 100 positions long, position month labels in the centre for each month
    positions = [ ]
    p = 0
    for y in xaxis:
        datax = xaxis[y]
        for k in datax:
            w = datax[k] * 100.0 / ndatapoints
            positions.append(p + w/2)
            p += w
    chart.set_axis_positions(1, positions)
    
    # position year labels at the centre of the year
    positions = [ ]
    p = 0
    for y in xaxis:
        datax = xaxis[y]
        w = sum(datax.values()) * 100.0 / ndatapoints
        positions.append(p + w/2)
        p += w
    chart.set_axis_positions(2, positions)
    
    chart.set_legend([k[0] for k in datay.keys()])
    
    # vertical stripes for marking weeks
    #weeks = [ ]
    nsundays = 0
    daycol = genColourRange(7)
    for p in range(ndatapoints):
        d = firstweekday + p
        if (d % 7) == 0:
            assertSunday(p)
            chart.add_marker(0, p, 'V', 'FF0000', 1)
        #weeks.append(daycol[d % 7])
        #weeks.append(1./ndatapoints) # this does not work if the width is less than 0.01
        #if len(weeks)/2 == 7: # from now it's repeats
        #    break
    #chart.fill_linear_stripes(Chart.CHART, 0, *weeks)
    #chart.add_marker(0, 100, 'V', 'FF0000', 1)
    return chart

def PrintAverageCharts(dataviews):           
    # another chart that shows the deviation from the average over the week, as a bar chart
    print '<table frame="border">'
    ncols = 3
    print '<tr><td colspan="%d" align="center" style="font-family:Arial;">Averaged Pollutants per day of week</td></tr>' % ncols
    icharts = 0
    for title, view in dataviews:
        weekchart = dict([d, dict([k, []] for k in view.keys())] for d in range(7)) # for each day of the week, and for each data type an empty list
    
        # for each dataset in this view, put datapoint into the list of the week day
        for k in view:
            data = view[k]
            for iday in range(len(data)):
                weekchart[(iday + firstweekday) % 7][k].append(data[iday])
    
        # bar chart of averages per day
        datasets = [ ]    
        max_y = None
        for k in view:
            data = [0. for i in range(7)]
            for d in weekchart:
                data[d] = sum(weekchart[d][k]) / len(weekchart[d][k])
            datasets.append(data)        
            max_y = max(max_y, max(data))
                
        # bar chart
        c = GroupedVerticalBarChart(400, 250, y_range=[0, max_y])
        c.set_bar_width(20/len(datasets))
        c.set_bar_spacing(0)
        if len(datasets) > 1:
            c.set_legend([k[0] for k in view.keys()])
        
        # Set the line colours
        c.set_colours(['0000FF', 'FF0000'])
    
        for data in datasets:
            c.add_data(data)
        # y axis labels
        if max_y > 30:
            left_axis = range(0, int(max_y) + 1, 5)
        elif max_y > 10:
            left_axis = range(0, int(max_y) + 1, 1)
        elif max_y > 5:
            left_axis = [ ]
            v = 0.
            while v < max_y + 0.5:
                left_axis.append(v)
                v += 0.5
        else:
            left_axis = [ ]
            v = 0.
            while v < max_y + 0.1:
                left_axis.append(v)
                v += 0.1

        left_axis[0] = '' # no label at 0
        c.set_axis_labels(Axis.LEFT, left_axis)
        c.set_axis_labels(Axis.BOTTOM, [weekdays[d] for d in weekchart.keys()])
        if icharts % ncols == 0:
            print '%s<tr>' % (icharts > 0 and '</tr>' or '')
        print '<td><img src="%s&chtt=%s"></td>' % (c.get_url(), title)
        icharts += 1
    print '</tr></table>'  
    

def PrintTimelineCharts(dataviews):
    print '<table frame="box" style="font-family:Arial;">'
    print '<tr><td colspan="1" align="center">Pollutants per day</td></tr>'
    for title, view in dataviews:
        c = createChart('', yearsandmonths, view, firstweekday)
        print '<tr><td><img src="%s&chtt=%s"></td></tr>' % (c.get_url(), title)
    print '</table>'

  



def PrepareData(datalist):
    # get the list of entries
    dataviews = [('Particulates%20%28%c2%b5g/m3%29', {('PM10',):[], ('PM2c5', 'PM2,5'):[] }), ('Ozone%20%28%c2%b5g/m3%29', {('O3',):[]}), ('Maximum CO%20%28%c2%b5g/m3%29', {('CO max', 'CO_max'):[]}), ('Nitrogen Dioxide%20%28%c2%b5g/m3%29', {('NO2',):[]}), ('Sulphur Dioxide%20%28%c2%b5g/m3%29', {('SO2',):[]})]
    for d in datalist:
        for t, view in dataviews:
            for k in view.keys():
                for kk in k:
                    if kk in d.keys() and d[kk] != None:
                        view[k].append(float(d[kk]))
    return dataviews
                

print '''
<H1>Particulates highest in mid-week!</H1>
<p><a href="http://www.nasa.gov/vision/earth/environment/ny_air.html">Research by NASA</a> shows that particulate density in New York is highest during the week, <quote>believed to be created by the comings and goings of people working in the city</quote>.

<p>The same pattern can be observed in the Austrian capital Vienna. (In the graphs below Sundays are marked with a red vertical line). We believe the noticable increase around beginning of October coincides with the onset of colder temperatures resulting in people heating their homes and offices.'''

daysback = 200 # number of days we go back for the graph (too many days results in google charts request being too long, ca 200 seems maximum)
datalist = LoadData(scrapername)
datalist = datalist[-daysback:]
tpl = (int(datalist[0]['Date'][:4]), int(datalist[0]['Date'][4:6]), int(datalist[0]['Date'][6:8]), 0, 0, 0, 0, 0, 0)
firstweekday = int(time.strftime("%w", time.gmtime(time.mktime(tpl))))
firstday = datetime.date(*(tpl[:3]))

dataviews = PrepareData(datalist )
yearsandmonths = { }
    
for d in datalist:
    imonth = int(d['Date'][4:6]) - 1
    year = int(d['Date'][:4])
    if year not in yearsandmonths:
        yearsandmonths[year] = {}
            
    if imonth not in yearsandmonths[year].keys():
        yearsandmonths[year][imonth] = 0
            
    yearsandmonths[year][imonth] += 1 # number of datapoints for this month
    
PrintAverageCharts(dataviews)
PrintTimelineCharts(dataviews)


                                      
                    
            

# this could do with an overhaul and be made into a dynamic webpage.
# the charts only seem to fit ca. 1 year, I have hardcoded the start date in the query
# see 'def LoadData'



import scraperwiki
import time, datetime

from pygooglechart import Chart
from pygooglechart import GroupedVerticalBarChart, SimpleLineChart
from pygooglechart import Axis


scrapername = 'wienerluft'
months = ['Jan', 'Feb', 'Apr', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def assertSunday(days):
    global firstday
    vd = firstday + datetime.timedelta(days)
    t = time.mktime((vd.year, vd.month, vd.day, 0, 0, 0, 0, 0, 0))
    assert time.strftime("%w", time.gmtime(t)) == '0'
    

def genColourRange(ncols, rgbfrom = (1.0, 0.9, 0.9), rgbto = (0.9, 0.9, 1.0)):
    import colorsys
    hsvfrom = colorsys.rgb_to_hsv(*rgbfrom)
    hsvto = colorsys.rgb_to_hsv(*rgbto)
    colsteps = ((hsvto[0] - hsvfrom[0])/(ncols - 1), (hsvto[1] - hsvfrom[1])/(ncols - 1), (hsvto[2] - hsvfrom[2])/(ncols - 1))
    colrange = [ ]
    for i in range(ncols):
        hsv = (hsvfrom[0] + i * colsteps[0], hsvfrom[1] + i * colsteps[1], hsvfrom[2] + i * colsteps[2])
        rgb = colorsys.hsv_to_rgb(*hsv)
        strrgb = '%.2x%.2x%.2x' % (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colrange.append(strrgb)
    return colrange       

# load all data a scraper that we can work with (this might be part of scraperlibs)
def LoadData(scrapername):
    #l = list(scraperwiki.apiwrapper.getData(scrapername))
    scraperwiki.sqlite.attach(scrapername)
    l = scraperwiki.sqlite.select("* from swdata where Date > 20120000") # THIS IS HARDCODED TO GET DATA FOR 2012
    return l[::-1] # reverse the list

def createChart(title, xaxis, datay, firstweekday):

    # Find the max y value
    max_y = None
    for dd in datay.values():
        max_y = max(max_y, max(dd))

    # Chart size of 400x250 pixels and specifying the range for the Y axis
    if title:
        chart = SimpleLineChart(1000, 250, title=title, y_range=[0, max_y])
    else:
        chart = SimpleLineChart(1000, 250, y_range=[0, max_y])
    
    # add the data
    for dd in datay.values():
        chart.add_data(dd)

    # Set the line colours
    chart.set_colours(['0000FF', 'FF0000', '00FF00', 'F0F000', '0F0F00'])

    # Set the horizontal dotted lines
    chart.set_grid(0, 25, 5, 5)
    
    # vertical stripes, the width of each stripe is calculated so that it covers one month
    ndatapoints = len(datay.values()[0])
            
    datapermonth = [ ]
    for year in xaxis:
        for month in xaxis[year]:
            datapermonth.append(xaxis[year][month])


    # mark months using range markers
    stripes = [ ]
    stripcols = ('FFFFFF', 'CCCCCC')
    wlast = 0
    for k in datapermonth:
        w = k * 1.0 / ndatapoints
        icol = len(stripes)/2 % 2
        stripes.append(stripcols[icol])
        stripes.append(w)
        wlast += w
    chart.fill_linear_stripes(Chart.CHART, 0, *stripes)

    # y axis labels
    if max_y > 30:
        left_axis = range(0, int(max_y) + 1, 5)
    elif max_y > 10:
        left_axis = range(0, int(max_y) + 1, 1)
    elif max_y > 5:
        left_axis = [ ]
        v = 0.
        while v < max_y + 0.5:
            left_axis.append(v)
            v += 0.5
    else:
        left_axis = [ ]
        v = 0.
        while v < max_y + 0.1:
            left_axis.append(v)
            v += 0.1

    left_axis[0] = '' # no label at 0
    chart.set_axis_labels(Axis.LEFT, left_axis)

    # X axis labels
    monthlabels = [ ]
    for year in xaxis:
        for imonth in xaxis[year]:
            monthlabels.append(months[imonth])

    chart.set_axis_labels(Axis.BOTTOM, monthlabels)
    chart.set_axis_labels(Axis.BOTTOM, xaxis.keys()) # years
    
    # the axis is 100 positions long, position month labels in the centre for each month
    positions = [ ]
    p = 0
    for y in xaxis:
        datax = xaxis[y]
        for k in datax:
            w = datax[k] * 100.0 / ndatapoints
            positions.append(p + w/2)
            p += w
    chart.set_axis_positions(1, positions)
    
    # position year labels at the centre of the year
    positions = [ ]
    p = 0
    for y in xaxis:
        datax = xaxis[y]
        w = sum(datax.values()) * 100.0 / ndatapoints
        positions.append(p + w/2)
        p += w
    chart.set_axis_positions(2, positions)
    
    chart.set_legend([k[0] for k in datay.keys()])
    
    # vertical stripes for marking weeks
    #weeks = [ ]
    nsundays = 0
    daycol = genColourRange(7)
    for p in range(ndatapoints):
        d = firstweekday + p
        if (d % 7) == 0:
            assertSunday(p)
            chart.add_marker(0, p, 'V', 'FF0000', 1)
        #weeks.append(daycol[d % 7])
        #weeks.append(1./ndatapoints) # this does not work if the width is less than 0.01
        #if len(weeks)/2 == 7: # from now it's repeats
        #    break
    #chart.fill_linear_stripes(Chart.CHART, 0, *weeks)
    #chart.add_marker(0, 100, 'V', 'FF0000', 1)
    return chart

def PrintAverageCharts(dataviews):           
    # another chart that shows the deviation from the average over the week, as a bar chart
    print '<table frame="border">'
    ncols = 3
    print '<tr><td colspan="%d" align="center" style="font-family:Arial;">Averaged Pollutants per day of week</td></tr>' % ncols
    icharts = 0
    for title, view in dataviews:
        weekchart = dict([d, dict([k, []] for k in view.keys())] for d in range(7)) # for each day of the week, and for each data type an empty list
    
        # for each dataset in this view, put datapoint into the list of the week day
        for k in view:
            data = view[k]
            for iday in range(len(data)):
                weekchart[(iday + firstweekday) % 7][k].append(data[iday])
    
        # bar chart of averages per day
        datasets = [ ]    
        max_y = None
        for k in view:
            data = [0. for i in range(7)]
            for d in weekchart:
                data[d] = sum(weekchart[d][k]) / len(weekchart[d][k])
            datasets.append(data)        
            max_y = max(max_y, max(data))
                
        # bar chart
        c = GroupedVerticalBarChart(400, 250, y_range=[0, max_y])
        c.set_bar_width(20/len(datasets))
        c.set_bar_spacing(0)
        if len(datasets) > 1:
            c.set_legend([k[0] for k in view.keys()])
        
        # Set the line colours
        c.set_colours(['0000FF', 'FF0000'])
    
        for data in datasets:
            c.add_data(data)
        # y axis labels
        if max_y > 30:
            left_axis = range(0, int(max_y) + 1, 5)
        elif max_y > 10:
            left_axis = range(0, int(max_y) + 1, 1)
        elif max_y > 5:
            left_axis = [ ]
            v = 0.
            while v < max_y + 0.5:
                left_axis.append(v)
                v += 0.5
        else:
            left_axis = [ ]
            v = 0.
            while v < max_y + 0.1:
                left_axis.append(v)
                v += 0.1

        left_axis[0] = '' # no label at 0
        c.set_axis_labels(Axis.LEFT, left_axis)
        c.set_axis_labels(Axis.BOTTOM, [weekdays[d] for d in weekchart.keys()])
        if icharts % ncols == 0:
            print '%s<tr>' % (icharts > 0 and '</tr>' or '')
        print '<td><img src="%s&chtt=%s"></td>' % (c.get_url(), title)
        icharts += 1
    print '</tr></table>'  
    

def PrintTimelineCharts(dataviews):
    print '<table frame="box" style="font-family:Arial;">'
    print '<tr><td colspan="1" align="center">Pollutants per day</td></tr>'
    for title, view in dataviews:
        c = createChart('', yearsandmonths, view, firstweekday)
        print '<tr><td><img src="%s&chtt=%s"></td></tr>' % (c.get_url(), title)
    print '</table>'

  



def PrepareData(datalist):
    # get the list of entries
    dataviews = [('Particulates%20%28%c2%b5g/m3%29', {('PM10',):[], ('PM2c5', 'PM2,5'):[] }), ('Ozone%20%28%c2%b5g/m3%29', {('O3',):[]}), ('Maximum CO%20%28%c2%b5g/m3%29', {('CO max', 'CO_max'):[]}), ('Nitrogen Dioxide%20%28%c2%b5g/m3%29', {('NO2',):[]}), ('Sulphur Dioxide%20%28%c2%b5g/m3%29', {('SO2',):[]})]
    for d in datalist:
        for t, view in dataviews:
            for k in view.keys():
                for kk in k:
                    if kk in d.keys() and d[kk] != None:
                        view[k].append(float(d[kk]))
    return dataviews
                

print '''
<H1>Particulates highest in mid-week!</H1>
<p><a href="http://www.nasa.gov/vision/earth/environment/ny_air.html">Research by NASA</a> shows that particulate density in New York is highest during the week, <quote>believed to be created by the comings and goings of people working in the city</quote>.

<p>The same pattern can be observed in the Austrian capital Vienna. (In the graphs below Sundays are marked with a red vertical line). We believe the noticable increase around beginning of October coincides with the onset of colder temperatures resulting in people heating their homes and offices.'''

daysback = 200 # number of days we go back for the graph (too many days results in google charts request being too long, ca 200 seems maximum)
datalist = LoadData(scrapername)
datalist = datalist[-daysback:]
tpl = (int(datalist[0]['Date'][:4]), int(datalist[0]['Date'][4:6]), int(datalist[0]['Date'][6:8]), 0, 0, 0, 0, 0, 0)
firstweekday = int(time.strftime("%w", time.gmtime(time.mktime(tpl))))
firstday = datetime.date(*(tpl[:3]))

dataviews = PrepareData(datalist )
yearsandmonths = { }
    
for d in datalist:
    imonth = int(d['Date'][4:6]) - 1
    year = int(d['Date'][:4])
    if year not in yearsandmonths:
        yearsandmonths[year] = {}
            
    if imonth not in yearsandmonths[year].keys():
        yearsandmonths[year][imonth] = 0
            
    yearsandmonths[year][imonth] += 1 # number of datapoints for this month
    
PrintAverageCharts(dataviews)
PrintTimelineCharts(dataviews)


                                      
                    
            


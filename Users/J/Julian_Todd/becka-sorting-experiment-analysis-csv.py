# TODO:
# Zooming and scrolling (there must be a quick/standard way to do it)

import scraperwiki
import xlrd    
import urllib
import csv
import sys
import numpy
import json

verbose = False

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(url).read())
sheet = book.sheet_by_index(0)
if verbose:
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make the object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value) 
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

# collate the data on all the subjects
subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects


# check the object lists are consistent
if verbose:
    for subjectnumber, groups in subjects.items():
        objectlist = [ ]
        for objects in groups.values():
            objectlist.extend(objects)
        if len(objectlist) != len(set(objectlist)):
            print "There is a double count in subject", subjectnumber
        if len(objectlist) != 150:
            print "Subject %d has %d items" % (subjectnumber, len(objectlist))


# calculate the correlation matrix
import numpy
objectnumbers = sorted(objectlookup.keys())
corrmatrix = numpy.ones((len(objectnumbers), len(objectnumbers)))

for subjectgroups in subjects.values():
    for objects in subjectgroups.values():
        for o1 in objects:
            for o2 in objects:
                corrmatrix[objectnumbers.index(o1)][objectnumbers.index(o2)] -= 1./len(subjects)


# this is an MDS cookbook from http://code.google.com/p/pyrouette/source/browse/alg/mds.py
E = (-0.5 * corrmatrix**2)
Er = numpy.mat(numpy.mean(E,1))
Es = numpy.mat(numpy.mean(E,0))
F = numpy.array(E - numpy.transpose(Er) - Es + numpy.mean(E))
[U, S, V] = numpy.linalg.svd(F)
Y = U * numpy.sqrt(S)


data = Y[:,0:2].tolist()
for i, objectnumber in enumerate(objectnumbers):
    data[i].append(objectlookup[objectnumber])

jcode = """
window.onload = function() 
{
    var paper = Raphael("rrr", 800, 600);  
    
    var d = %s; 
    
    function h(v) { return v*600+400; }
    function r(dd)
    {
        var circle = paper.circle(h(dd[0]), h(dd[1]), 5).attr({fill:'red'}); 
        var txt = paper.text(h(dd[0])+20, h(dd[1])-20, dd[2]).attr({opacity: "0", fill: "#fff", stroke: "none", "font": '100 28px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'});
        txt.toBack();

        circle.mouseover(function() { txt.stop(); txt.toFront(); txt.attr({opacity: "1"})});
        circle.mouseout(function() { txt.animate({opacity: "0"}, 550, function() { txt.toBack() } )});
    }
   
    for (var i = 0; i < d.length; i++)
        r(d[i]); 
}""" % json.dumps(list(data))


print '<html><head><script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode

print '''
<h2>Psychology <a href="http://en.wikipedia.org/wiki/Categorization">categorization</a> experiment</h2>
<p>Each experimental subject got a pile of 150 things on cards. They were told to divide it into a number of piles 
according to things they think are similar to each other. They could use as few or as many piles as they like.</p>
<p>This is the result of the experiment, clustered using multi-dimensional scaling (MDS) and then plotted using RaphaelJS. The clusters show which objects lots of people thought belonged in the same category.</p>
<p><strong>Hover over the red dots to see which card they represent</strong></p>
'''

print '<div id="rrr" style="height:600px; width:800px; background:#333"></div></body></html>'

# TODO:
# Zooming and scrolling (there must be a quick/standard way to do it)

import scraperwiki
import xlrd    
import urllib
import csv
import sys
import numpy
import json

verbose = False

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(url).read())
sheet = book.sheet_by_index(0)
if verbose:
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make the object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value) 
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

# collate the data on all the subjects
subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects


# check the object lists are consistent
if verbose:
    for subjectnumber, groups in subjects.items():
        objectlist = [ ]
        for objects in groups.values():
            objectlist.extend(objects)
        if len(objectlist) != len(set(objectlist)):
            print "There is a double count in subject", subjectnumber
        if len(objectlist) != 150:
            print "Subject %d has %d items" % (subjectnumber, len(objectlist))


# calculate the correlation matrix
import numpy
objectnumbers = sorted(objectlookup.keys())
corrmatrix = numpy.ones((len(objectnumbers), len(objectnumbers)))

for subjectgroups in subjects.values():
    for objects in subjectgroups.values():
        for o1 in objects:
            for o2 in objects:
                corrmatrix[objectnumbers.index(o1)][objectnumbers.index(o2)] -= 1./len(subjects)


# this is an MDS cookbook from http://code.google.com/p/pyrouette/source/browse/alg/mds.py
E = (-0.5 * corrmatrix**2)
Er = numpy.mat(numpy.mean(E,1))
Es = numpy.mat(numpy.mean(E,0))
F = numpy.array(E - numpy.transpose(Er) - Es + numpy.mean(E))
[U, S, V] = numpy.linalg.svd(F)
Y = U * numpy.sqrt(S)


data = Y[:,0:2].tolist()
for i, objectnumber in enumerate(objectnumbers):
    data[i].append(objectlookup[objectnumber])

jcode = """
window.onload = function() 
{
    var paper = Raphael("rrr", 800, 600);  
    
    var d = %s; 
    
    function h(v) { return v*600+400; }
    function r(dd)
    {
        var circle = paper.circle(h(dd[0]), h(dd[1]), 5).attr({fill:'red'}); 
        var txt = paper.text(h(dd[0])+20, h(dd[1])-20, dd[2]).attr({opacity: "0", fill: "#fff", stroke: "none", "font": '100 28px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'});
        txt.toBack();

        circle.mouseover(function() { txt.stop(); txt.toFront(); txt.attr({opacity: "1"})});
        circle.mouseout(function() { txt.animate({opacity: "0"}, 550, function() { txt.toBack() } )});
    }
   
    for (var i = 0; i < d.length; i++)
        r(d[i]); 
}""" % json.dumps(list(data))


print '<html><head><script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode

print '''
<h2>Psychology <a href="http://en.wikipedia.org/wiki/Categorization">categorization</a> experiment</h2>
<p>Each experimental subject got a pile of 150 things on cards. They were told to divide it into a number of piles 
according to things they think are similar to each other. They could use as few or as many piles as they like.</p>
<p>This is the result of the experiment, clustered using multi-dimensional scaling (MDS) and then plotted using RaphaelJS. The clusters show which objects lots of people thought belonged in the same category.</p>
<p><strong>Hover over the red dots to see which card they represent</strong></p>
'''

print '<div id="rrr" style="height:600px; width:800px; background:#333"></div></body></html>'

# TODO:
# Zooming and scrolling (there must be a quick/standard way to do it)

import scraperwiki
import xlrd    
import urllib
import csv
import sys
import numpy
import json

verbose = False

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(url).read())
sheet = book.sheet_by_index(0)
if verbose:
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make the object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value) 
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

# collate the data on all the subjects
subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects


# check the object lists are consistent
if verbose:
    for subjectnumber, groups in subjects.items():
        objectlist = [ ]
        for objects in groups.values():
            objectlist.extend(objects)
        if len(objectlist) != len(set(objectlist)):
            print "There is a double count in subject", subjectnumber
        if len(objectlist) != 150:
            print "Subject %d has %d items" % (subjectnumber, len(objectlist))


# calculate the correlation matrix
import numpy
objectnumbers = sorted(objectlookup.keys())
corrmatrix = numpy.ones((len(objectnumbers), len(objectnumbers)))

for subjectgroups in subjects.values():
    for objects in subjectgroups.values():
        for o1 in objects:
            for o2 in objects:
                corrmatrix[objectnumbers.index(o1)][objectnumbers.index(o2)] -= 1./len(subjects)


# this is an MDS cookbook from http://code.google.com/p/pyrouette/source/browse/alg/mds.py
E = (-0.5 * corrmatrix**2)
Er = numpy.mat(numpy.mean(E,1))
Es = numpy.mat(numpy.mean(E,0))
F = numpy.array(E - numpy.transpose(Er) - Es + numpy.mean(E))
[U, S, V] = numpy.linalg.svd(F)
Y = U * numpy.sqrt(S)


data = Y[:,0:2].tolist()
for i, objectnumber in enumerate(objectnumbers):
    data[i].append(objectlookup[objectnumber])

jcode = """
window.onload = function() 
{
    var paper = Raphael("rrr", 800, 600);  
    
    var d = %s; 
    
    function h(v) { return v*600+400; }
    function r(dd)
    {
        var circle = paper.circle(h(dd[0]), h(dd[1]), 5).attr({fill:'red'}); 
        var txt = paper.text(h(dd[0])+20, h(dd[1])-20, dd[2]).attr({opacity: "0", fill: "#fff", stroke: "none", "font": '100 28px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'});
        txt.toBack();

        circle.mouseover(function() { txt.stop(); txt.toFront(); txt.attr({opacity: "1"})});
        circle.mouseout(function() { txt.animate({opacity: "0"}, 550, function() { txt.toBack() } )});
    }
   
    for (var i = 0; i < d.length; i++)
        r(d[i]); 
}""" % json.dumps(list(data))


print '<html><head><script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode

print '''
<h2>Psychology <a href="http://en.wikipedia.org/wiki/Categorization">categorization</a> experiment</h2>
<p>Each experimental subject got a pile of 150 things on cards. They were told to divide it into a number of piles 
according to things they think are similar to each other. They could use as few or as many piles as they like.</p>
<p>This is the result of the experiment, clustered using multi-dimensional scaling (MDS) and then plotted using RaphaelJS. The clusters show which objects lots of people thought belonged in the same category.</p>
<p><strong>Hover over the red dots to see which card they represent</strong></p>
'''

print '<div id="rrr" style="height:600px; width:800px; background:#333"></div></body></html>'

# TODO:
# Zooming and scrolling (there must be a quick/standard way to do it)

import scraperwiki
import xlrd    
import urllib
import csv
import sys
import numpy
import json

verbose = False

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(url).read())
sheet = book.sheet_by_index(0)
if verbose:
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make the object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value) 
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

# collate the data on all the subjects
subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects


# check the object lists are consistent
if verbose:
    for subjectnumber, groups in subjects.items():
        objectlist = [ ]
        for objects in groups.values():
            objectlist.extend(objects)
        if len(objectlist) != len(set(objectlist)):
            print "There is a double count in subject", subjectnumber
        if len(objectlist) != 150:
            print "Subject %d has %d items" % (subjectnumber, len(objectlist))


# calculate the correlation matrix
import numpy
objectnumbers = sorted(objectlookup.keys())
corrmatrix = numpy.ones((len(objectnumbers), len(objectnumbers)))

for subjectgroups in subjects.values():
    for objects in subjectgroups.values():
        for o1 in objects:
            for o2 in objects:
                corrmatrix[objectnumbers.index(o1)][objectnumbers.index(o2)] -= 1./len(subjects)


# this is an MDS cookbook from http://code.google.com/p/pyrouette/source/browse/alg/mds.py
E = (-0.5 * corrmatrix**2)
Er = numpy.mat(numpy.mean(E,1))
Es = numpy.mat(numpy.mean(E,0))
F = numpy.array(E - numpy.transpose(Er) - Es + numpy.mean(E))
[U, S, V] = numpy.linalg.svd(F)
Y = U * numpy.sqrt(S)


data = Y[:,0:2].tolist()
for i, objectnumber in enumerate(objectnumbers):
    data[i].append(objectlookup[objectnumber])

jcode = """
window.onload = function() 
{
    var paper = Raphael("rrr", 800, 600);  
    
    var d = %s; 
    
    function h(v) { return v*600+400; }
    function r(dd)
    {
        var circle = paper.circle(h(dd[0]), h(dd[1]), 5).attr({fill:'red'}); 
        var txt = paper.text(h(dd[0])+20, h(dd[1])-20, dd[2]).attr({opacity: "0", fill: "#fff", stroke: "none", "font": '100 28px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'});
        txt.toBack();

        circle.mouseover(function() { txt.stop(); txt.toFront(); txt.attr({opacity: "1"})});
        circle.mouseout(function() { txt.animate({opacity: "0"}, 550, function() { txt.toBack() } )});
    }
   
    for (var i = 0; i < d.length; i++)
        r(d[i]); 
}""" % json.dumps(list(data))


print '<html><head><script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode

print '''
<h2>Psychology <a href="http://en.wikipedia.org/wiki/Categorization">categorization</a> experiment</h2>
<p>Each experimental subject got a pile of 150 things on cards. They were told to divide it into a number of piles 
according to things they think are similar to each other. They could use as few or as many piles as they like.</p>
<p>This is the result of the experiment, clustered using multi-dimensional scaling (MDS) and then plotted using RaphaelJS. The clusters show which objects lots of people thought belonged in the same category.</p>
<p><strong>Hover over the red dots to see which card they represent</strong></p>
'''

print '<div id="rrr" style="height:600px; width:800px; background:#333"></div></body></html>'

# TODO:
# Zooming and scrolling (there must be a quick/standard way to do it)

import scraperwiki
import xlrd    
import urllib
import csv
import sys
import numpy
import json

verbose = False

url = 'http://seagrass.goatchurch.org.uk/~julian/Julian-SarahPowell-ALLData-4.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(url).read())
sheet = book.sheet_by_index(0)
if verbose:
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)


# make the object lookup array
objectlookup = { }
for row in range(1839, sheet.nrows): 
    i = int(sheet.cell(row, 0).value) 
    assert i == row - 1838, (i, row)
    objectlookup[i] = sheet.cell(row, 1).value
                              

# collate the data on all the subjects
subjects = { }
for r in range(3, 1839):
    if not sheet.cell(r, 0).value or r == 1658:
        continue
    subjectnumber = int(sheet.cell(r, 0).value)
    groupnumber = int(sheet.cell(r, 3).value)
    objects = [ ]
    for i in range(4, 50):
        v = sheet.cell(r, i).value
        if v:
            objects.append(int(v))
    if not objects:
        continue

    if subjectnumber not in subjects:
        subjects[subjectnumber] = { }
    subjects[subjectnumber][groupnumber] = objects


# check the object lists are consistent
if verbose:
    for subjectnumber, groups in subjects.items():
        objectlist = [ ]
        for objects in groups.values():
            objectlist.extend(objects)
        if len(objectlist) != len(set(objectlist)):
            print "There is a double count in subject", subjectnumber
        if len(objectlist) != 150:
            print "Subject %d has %d items" % (subjectnumber, len(objectlist))


# calculate the correlation matrix
import numpy
objectnumbers = sorted(objectlookup.keys())
corrmatrix = numpy.ones((len(objectnumbers), len(objectnumbers)))

for subjectgroups in subjects.values():
    for objects in subjectgroups.values():
        for o1 in objects:
            for o2 in objects:
                corrmatrix[objectnumbers.index(o1)][objectnumbers.index(o2)] -= 1./len(subjects)


# this is an MDS cookbook from http://code.google.com/p/pyrouette/source/browse/alg/mds.py
E = (-0.5 * corrmatrix**2)
Er = numpy.mat(numpy.mean(E,1))
Es = numpy.mat(numpy.mean(E,0))
F = numpy.array(E - numpy.transpose(Er) - Es + numpy.mean(E))
[U, S, V] = numpy.linalg.svd(F)
Y = U * numpy.sqrt(S)


data = Y[:,0:2].tolist()
for i, objectnumber in enumerate(objectnumbers):
    data[i].append(objectlookup[objectnumber])

jcode = """
window.onload = function() 
{
    var paper = Raphael("rrr", 800, 600);  
    
    var d = %s; 
    
    function h(v) { return v*600+400; }
    function r(dd)
    {
        var circle = paper.circle(h(dd[0]), h(dd[1]), 5).attr({fill:'red'}); 
        var txt = paper.text(h(dd[0])+20, h(dd[1])-20, dd[2]).attr({opacity: "0", fill: "#fff", stroke: "none", "font": '100 28px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'});
        txt.toBack();

        circle.mouseover(function() { txt.stop(); txt.toFront(); txt.attr({opacity: "1"})});
        circle.mouseout(function() { txt.animate({opacity: "0"}, 550, function() { txt.toBack() } )});
    }
   
    for (var i = 0; i < d.length; i++)
        r(d[i]); 
}""" % json.dumps(list(data))


print '<html><head><script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script><script>%s</script></head><body>' % jcode

print '''
<h2>Psychology <a href="http://en.wikipedia.org/wiki/Categorization">categorization</a> experiment</h2>
<p>Each experimental subject got a pile of 150 things on cards. They were told to divide it into a number of piles 
according to things they think are similar to each other. They could use as few or as many piles as they like.</p>
<p>This is the result of the experiment, clustered using multi-dimensional scaling (MDS) and then plotted using RaphaelJS. The clusters show which objects lots of people thought belonged in the same category.</p>
<p><strong>Hover over the red dots to see which card they represent</strong></p>
'''

print '<div id="rrr" style="height:600px; width:800px; background:#333"></div></body></html>'


# Blank Python
sourcescraper = ''
import freesteel.freesteelpy as kernel
import scraperwiki

# here's what I mean by very stripped down.  Should implement into a JSONP protocol 
# which can be called from one of the WebGL demos, eg:
#    http://www.nmr.mgh.harvard.edu/~rudolph/webgl/brain_viewer/brain_viewer.html

# ideal is that that one of these pages should be able to insert a call out (and a button) to this 
# service and receive the slices back -- which can then be directed to the reprap
# after further editing for stands, etc.  

# this scraperwiki app is not the production release.  It's the place where someone who is making 
# one of those javascript/WebGL front ends can easily adapt and develop the API from both ends.  
# and then we can port it into a twister unit on seagrass once it's stable and right


import cgi, os, sys
print "(The query string is:", os.getenv("QUERY_STRING"), ")<br>"
print "This is how you parse a query string", dict(cgi.parse_qsl("a=b&c=11%20333xxx")), "<br>"
print cgi.parse_qs(os.environ["QUERY_STRING"]), "<br>"
print cgi.parse_qsl(os.environ["QUERY_STRING"]), "<br>"
querystring=dict(cgi.parse_qsl(os.environ["QUERY_STRING"]))
print str(querystring), "<br>"
for key in querystring.keys():
    print key," : ", querystring[key],  "<br>"
#sys.exit(0)


# (here we should parse one of the WebGL native triangulation objects) that are often used
fssurf = kernel.FsSurf.New()
fssurf.PushTriangle(0,0,0, 0,2,0, 0.4,0.1,1)
fssurf.Build(1.0)

fshoriztoolsurf = kernel.FsHorizontalToolSurface.New()
fshoriztoolsurf.AddSurf(fssurf)
fshoriztoolsurf.AddTipShape(0.4, 0.3, 0.5)   # (corner_radius, flat_radius, z)

fsimplicitarea = kernel.FsImplicitArea.New(0)
fsimplicitarea.AddHorizToolSurf(fshoriztoolsurf)
fsimplicitarea.SetContourConditions(0.99, -1.0, 0.002, 2, -1.0, 0.9)
    # (minCNdotContour, maxZdiffContour, deltaHdiffContour, maxHdiffContour, maxCPcuspContour, minBNdotContour)

fsweave = kernel.FsWeave.New()
fsweave.SetShape(-5, 5, -5, 5, 0.17) # (xlo, xhi, ylo, yhi, approx_resolution)
fsimplicitarea.GenWeaveZProfile(fsweave)
ncontours = fsweave.GetNContours()
#print fsweave.StructureContours()
for inum in range(ncontours):
    fspath = kernel.FsPath2X.New(0.0)
    fspath.RecordContour(fsweave, False, inum, 0.002)
    print "(Testing ScraperWiki/FreeSteel)<br>"
    print "<br>"

    # G-code style output
    npts = fspath.GetNpts()
    #print "\n".join([ "G1X%.2fY%.2f<br>"  % (fspath.GetD(i, 0), fspath.GetD(i, 1))  for i in range(npts) ])

    
    for i in range(npts):
        scraperwiki.sqlite.save(['inum', 'i'], {'inum':inum, 'i': i, 'x':fspath.GetD(i, 0), 'y':fspath.GetD(i, 1)})


# Blank Python
sourcescraper = ''
import freesteel.freesteelpy as kernel
import scraperwiki

# here's what I mean by very stripped down.  Should implement into a JSONP protocol 
# which can be called from one of the WebGL demos, eg:
#    http://www.nmr.mgh.harvard.edu/~rudolph/webgl/brain_viewer/brain_viewer.html

# ideal is that that one of these pages should be able to insert a call out (and a button) to this 
# service and receive the slices back -- which can then be directed to the reprap
# after further editing for stands, etc.  

# this scraperwiki app is not the production release.  It's the place where someone who is making 
# one of those javascript/WebGL front ends can easily adapt and develop the API from both ends.  
# and then we can port it into a twister unit on seagrass once it's stable and right


import cgi, os, sys
print "(The query string is:", os.getenv("QUERY_STRING"), ")<br>"
print "This is how you parse a query string", dict(cgi.parse_qsl("a=b&c=11%20333xxx")), "<br>"
print cgi.parse_qs(os.environ["QUERY_STRING"]), "<br>"
print cgi.parse_qsl(os.environ["QUERY_STRING"]), "<br>"
querystring=dict(cgi.parse_qsl(os.environ["QUERY_STRING"]))
print str(querystring), "<br>"
for key in querystring.keys():
    print key," : ", querystring[key],  "<br>"
#sys.exit(0)


# (here we should parse one of the WebGL native triangulation objects) that are often used
fssurf = kernel.FsSurf.New()
fssurf.PushTriangle(0,0,0, 0,2,0, 0.4,0.1,1)
fssurf.Build(1.0)

fshoriztoolsurf = kernel.FsHorizontalToolSurface.New()
fshoriztoolsurf.AddSurf(fssurf)
fshoriztoolsurf.AddTipShape(0.4, 0.3, 0.5)   # (corner_radius, flat_radius, z)

fsimplicitarea = kernel.FsImplicitArea.New(0)
fsimplicitarea.AddHorizToolSurf(fshoriztoolsurf)
fsimplicitarea.SetContourConditions(0.99, -1.0, 0.002, 2, -1.0, 0.9)
    # (minCNdotContour, maxZdiffContour, deltaHdiffContour, maxHdiffContour, maxCPcuspContour, minBNdotContour)

fsweave = kernel.FsWeave.New()
fsweave.SetShape(-5, 5, -5, 5, 0.17) # (xlo, xhi, ylo, yhi, approx_resolution)
fsimplicitarea.GenWeaveZProfile(fsweave)
ncontours = fsweave.GetNContours()
#print fsweave.StructureContours()
for inum in range(ncontours):
    fspath = kernel.FsPath2X.New(0.0)
    fspath.RecordContour(fsweave, False, inum, 0.002)
    print "(Testing ScraperWiki/FreeSteel)<br>"
    print "<br>"

    # G-code style output
    npts = fspath.GetNpts()
    #print "\n".join([ "G1X%.2fY%.2f<br>"  % (fspath.GetD(i, 0), fspath.GetD(i, 1))  for i in range(npts) ])

    
    for i in range(npts):
        scraperwiki.sqlite.save(['inum', 'i'], {'inum':inum, 'i': i, 'x':fspath.GetD(i, 0), 'y':fspath.GetD(i, 1)})



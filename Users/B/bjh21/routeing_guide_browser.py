import scraperwiki
scraperwiki.sqlite.attach('atoc_routeing_guide')

import lxml.etree as etree
import lxml.html
from lxml.builder import ElementMaker
E = ElementMaker(namespace="http://www.w3.org/1999/xhtml", nsmap={None : "http://www.w3.org/1999/xhtml"})
import cgi
import os

ns={'namespaces': {'h': 'http://www.w3.org/1999/xhtml'}}

args = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

template = '''
<!DOCTYPE html
          PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head><title>Routeing Guide browser</title></head>
  <body><form action="."><table id="maintable">
    <tr><td></td>
      <td><label for="orig">Origin: </label><input name="orig" id="orig" /></td>
      <td><label for="dest"> Destination: </label><input name="dest" id="dest" /></td>
      <td><input type="submit" name="sub-stn" value="Search for stations" /></td></tr>
    <tr id="stnrow"><th>Station</th>
      <td id="orig-stnsel"></td>
      <td id="dest-stnsel"></td>
      <td><input type="submit" name="sub-rp" value="Find routeing points" /></td></tr>
    <tr id="rprow"><th>Routeing point</th>
      <td id="orig-rpsel"></td>
      <td id="dest-rpsel"></td>
      <td><input type="submit" name="sub-route" value="Find routes" /></td></tr>
    <tr id="routerow"><th>Route</th>
      <td colspan="2" id="routesel"></td>
      <td><input type="submit" name="sub-maps" value="Show maps" /></td></tr>
  </table></form>
 <div id="maps" />
 <hr />
 <p class="footer">The Routeing Guide Browser is written by <a href="http://bjh21.me.uk/">Ben Harris</a>,
   and is not endorsed by ATOC.</p>
 </body>
</html>
'''

if 'sub-stn' in args:
    args.pop('orig-stn', None)
    args.pop('dest-stn', None)
if 'sub-stn' in args or 'sub-rp' in args:
    args.pop('orig-rp', None)
    args.pop('dest-rp', None)
if 'sub-stn' in args or 'sub-rp' in args or 'sub-route' in args:
    args.pop('maps', None)

page = etree.fromstring(template)
body=page.xpath('//h:body', **ns)[0]
def byid(id):
    return page.xpath('//*[@id=$id]', id=id, **ns)[0]

idgen = 1

def radiobuttons(name, values):
    ret = []
    for v in values:
        global idgen
        global args
        b_id = "r%d"%(idgen)
        idgen += 1
        button = E.input(type='radio', name=name, value=v, id=b_id)
        if len(values) == 1:
            args[name] = v
        if args.get(name) == v:
            button.attrib['checked'] = 'checked'
        ret.extend([button, E.label(v, {'for': b_id}), E.br()])
    return ret

def london(orig, dest):
    inrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = ? AND dest = 'London Group'", (orig))
    outrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = 'London Group' AND dest = ?", (dest))
    inroutes = [r['maps'] for r in inrows]
    outroutes = [r['maps'] for r in outrows]
    routes = reduce(lambda x, y: x + y, [["%s+%s" % (i, o) for o in outroutes] for i in inroutes], [])
    routes = [r for r in routes if len(r.split('+')) == len(set(r.split('+')))]
    return routes

delstnrow = True
for k in ('orig', 'dest'):
    if k in args:
        delstnrow = False
        page.xpath('//h:input[@name=$k]', k=k, **ns)[0].attrib["value"] = args[k]
        stnrows = scraperwiki.sqlite.select("DISTINCT station FROM routeing_points WHERE station LIKE '%' || ? || '%'", (args[k]))
        stnsel = byid("%s-stnsel" % (k))
        if len(stnrows) == 0:
            stnsel.append(E.div("No matching stations"))
        else:
            stnsel.extend(radiobuttons('%s-stn'%(k), [stnrow['station'] for stnrow in stnrows]))
if delstnrow:
    byid("maintable").remove(byid("stnrow"))

rps = { }
commonrps = False
delrprow = True
for k in ('orig', 'dest'):
    if ('%s-stn' % (k)) in args:
        delrprow = False
        rprows = scraperwiki.sqlite.select("routeing_point FROM routeing_points WHERE station = ?", (args['%s-stn'%(k)]))
        rps[k] = [rprow['routeing_point'] for rprow in rprows]
        rpsel = byid("%s-rpsel" % (k))
        rpsel.extend(radiobuttons('%s-rp'%(k), rps[k]))

if delrprow:
    byid("maintable").remove(byid("rprow"))

if 'orig' in rps and 'dest' in rps:
    if set(rps['orig']).intersection(rps['dest']):
        byid("routesel").text = "Common routing point(s).  No mapped routes."
        for e in page.xpath('//*[@id="orig-rpsel" or @id="dest-rpsel"]//h:input', **ns):
            e.attrib['disabled'] = 'disabled'

if 'orig-rp' in args and len(rps['orig']) > 1:
    byid("orig-rpsel").append(E.p(u"Check fares: %s \u2192 %s \u2265 %s \u2192 %s." %
                                  (args["orig-stn"], args["dest-stn"], args["orig-rp"], args["dest-stn"])))
if 'dest-rp' in args and len(rps['dest']) > 1:
    byid("dest-rpsel").append(E.p(u"Check fares: %s \u2192 %s \u2265 %s \u2192 %s." %
                                  (args["orig-stn"], args["dest-stn"], args["orig-stn"], args["dest-rp"])))

routesel = byid("routesel")
if ('orig-rp' in args and 'dest-rp' in args):
    rrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = ? AND dest = ?",
        (args['orig-rp'], args['dest-rp']))
    routes = set([rrow['maps'] for rrow in rrows])
    if 'LONDON' in routes:
        routes.update(london(args['orig-rp'], args['dest-rp']))
        routes.remove("LONDON")
    routesel.extend(radiobuttons('maps', sorted(routes)))
else:
    byid("maintable").remove(byid("routerow"))

if args.has_key('maps'):
    maps = args['maps'].split('+')
    prevmap = None
    for map in maps:
        if prevmap:
            joins = scraperwiki.sqlite.select("""a.routeing_point FROM rp_maps a, rp_maps b
                                               WHERE a.mapname = ? AND b.mapname = ? AND a.routeing_point = b.routeing_point""",
                                              (prevmap, map))
            byid("maps").append(E.div("[%s and %s meet at %s]" % (prevmap, map, ", ".join([j['routeing_point'] for j in joins]))))
        maprows = scraperwiki.sqlite.select("pageno FROM maps WHERE mapname = ? ORDER BY mapname, pageno",
            (map))
        for maprow in maprows:
            byid("maps").append(E.div(E.img(src="/run/routeing_guide_map?pageno=%d" % (maprow['pageno']),
                                            alt="[Map %s]"%(map))))
        prevmap = map

print lxml.etree.tostring(page)
import scraperwiki
scraperwiki.sqlite.attach('atoc_routeing_guide')

import lxml.etree as etree
import lxml.html
from lxml.builder import ElementMaker
E = ElementMaker(namespace="http://www.w3.org/1999/xhtml", nsmap={None : "http://www.w3.org/1999/xhtml"})
import cgi
import os

ns={'namespaces': {'h': 'http://www.w3.org/1999/xhtml'}}

args = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

template = '''
<!DOCTYPE html
          PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head><title>Routeing Guide browser</title></head>
  <body><form action="."><table id="maintable">
    <tr><td></td>
      <td><label for="orig">Origin: </label><input name="orig" id="orig" /></td>
      <td><label for="dest"> Destination: </label><input name="dest" id="dest" /></td>
      <td><input type="submit" name="sub-stn" value="Search for stations" /></td></tr>
    <tr id="stnrow"><th>Station</th>
      <td id="orig-stnsel"></td>
      <td id="dest-stnsel"></td>
      <td><input type="submit" name="sub-rp" value="Find routeing points" /></td></tr>
    <tr id="rprow"><th>Routeing point</th>
      <td id="orig-rpsel"></td>
      <td id="dest-rpsel"></td>
      <td><input type="submit" name="sub-route" value="Find routes" /></td></tr>
    <tr id="routerow"><th>Route</th>
      <td colspan="2" id="routesel"></td>
      <td><input type="submit" name="sub-maps" value="Show maps" /></td></tr>
  </table></form>
 <div id="maps" />
 <hr />
 <p class="footer">The Routeing Guide Browser is written by <a href="http://bjh21.me.uk/">Ben Harris</a>,
   and is not endorsed by ATOC.</p>
 </body>
</html>
'''

if 'sub-stn' in args:
    args.pop('orig-stn', None)
    args.pop('dest-stn', None)
if 'sub-stn' in args or 'sub-rp' in args:
    args.pop('orig-rp', None)
    args.pop('dest-rp', None)
if 'sub-stn' in args or 'sub-rp' in args or 'sub-route' in args:
    args.pop('maps', None)

page = etree.fromstring(template)
body=page.xpath('//h:body', **ns)[0]
def byid(id):
    return page.xpath('//*[@id=$id]', id=id, **ns)[0]

idgen = 1

def radiobuttons(name, values):
    ret = []
    for v in values:
        global idgen
        global args
        b_id = "r%d"%(idgen)
        idgen += 1
        button = E.input(type='radio', name=name, value=v, id=b_id)
        if len(values) == 1:
            args[name] = v
        if args.get(name) == v:
            button.attrib['checked'] = 'checked'
        ret.extend([button, E.label(v, {'for': b_id}), E.br()])
    return ret

def london(orig, dest):
    inrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = ? AND dest = 'London Group'", (orig))
    outrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = 'London Group' AND dest = ?", (dest))
    inroutes = [r['maps'] for r in inrows]
    outroutes = [r['maps'] for r in outrows]
    routes = reduce(lambda x, y: x + y, [["%s+%s" % (i, o) for o in outroutes] for i in inroutes], [])
    routes = [r for r in routes if len(r.split('+')) == len(set(r.split('+')))]
    return routes

delstnrow = True
for k in ('orig', 'dest'):
    if k in args:
        delstnrow = False
        page.xpath('//h:input[@name=$k]', k=k, **ns)[0].attrib["value"] = args[k]
        stnrows = scraperwiki.sqlite.select("DISTINCT station FROM routeing_points WHERE station LIKE '%' || ? || '%'", (args[k]))
        stnsel = byid("%s-stnsel" % (k))
        if len(stnrows) == 0:
            stnsel.append(E.div("No matching stations"))
        else:
            stnsel.extend(radiobuttons('%s-stn'%(k), [stnrow['station'] for stnrow in stnrows]))
if delstnrow:
    byid("maintable").remove(byid("stnrow"))

rps = { }
commonrps = False
delrprow = True
for k in ('orig', 'dest'):
    if ('%s-stn' % (k)) in args:
        delrprow = False
        rprows = scraperwiki.sqlite.select("routeing_point FROM routeing_points WHERE station = ?", (args['%s-stn'%(k)]))
        rps[k] = [rprow['routeing_point'] for rprow in rprows]
        rpsel = byid("%s-rpsel" % (k))
        rpsel.extend(radiobuttons('%s-rp'%(k), rps[k]))

if delrprow:
    byid("maintable").remove(byid("rprow"))

if 'orig' in rps and 'dest' in rps:
    if set(rps['orig']).intersection(rps['dest']):
        byid("routesel").text = "Common routing point(s).  No mapped routes."
        for e in page.xpath('//*[@id="orig-rpsel" or @id="dest-rpsel"]//h:input', **ns):
            e.attrib['disabled'] = 'disabled'

if 'orig-rp' in args and len(rps['orig']) > 1:
    byid("orig-rpsel").append(E.p(u"Check fares: %s \u2192 %s \u2265 %s \u2192 %s." %
                                  (args["orig-stn"], args["dest-stn"], args["orig-rp"], args["dest-stn"])))
if 'dest-rp' in args and len(rps['dest']) > 1:
    byid("dest-rpsel").append(E.p(u"Check fares: %s \u2192 %s \u2265 %s \u2192 %s." %
                                  (args["orig-stn"], args["dest-stn"], args["orig-stn"], args["dest-rp"])))

routesel = byid("routesel")
if ('orig-rp' in args and 'dest-rp' in args):
    rrows = scraperwiki.sqlite.select("maps FROM permitted_routes WHERE orig = ? AND dest = ?",
        (args['orig-rp'], args['dest-rp']))
    routes = set([rrow['maps'] for rrow in rrows])
    if 'LONDON' in routes:
        routes.update(london(args['orig-rp'], args['dest-rp']))
        routes.remove("LONDON")
    routesel.extend(radiobuttons('maps', sorted(routes)))
else:
    byid("maintable").remove(byid("routerow"))

if args.has_key('maps'):
    maps = args['maps'].split('+')
    prevmap = None
    for map in maps:
        if prevmap:
            joins = scraperwiki.sqlite.select("""a.routeing_point FROM rp_maps a, rp_maps b
                                               WHERE a.mapname = ? AND b.mapname = ? AND a.routeing_point = b.routeing_point""",
                                              (prevmap, map))
            byid("maps").append(E.div("[%s and %s meet at %s]" % (prevmap, map, ", ".join([j['routeing_point'] for j in joins]))))
        maprows = scraperwiki.sqlite.select("pageno FROM maps WHERE mapname = ? ORDER BY mapname, pageno",
            (map))
        for maprow in maprows:
            byid("maps").append(E.div(E.img(src="/run/routeing_guide_map?pageno=%d" % (maprow['pageno']),
                                            alt="[Map %s]"%(map))))
        prevmap = map

print lxml.etree.tostring(page)

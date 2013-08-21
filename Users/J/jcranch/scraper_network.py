import scraperwiki
import cgi
import os
import cStringIO
import pydot


def main(args=None):
    if args is None:
        args = getargs()

    standard_json = [u"output_text",u"to_text",u"make_JSON"]
    standard_graphml = [u"output_text",u"JSON_to_GraphML",u"make_JSON"]
    standard_dot = [u"output_text",u"JSON_to_DOT",u"make_JSON"]
    standard_graphviz = [u"graphviz",u"JSON_to_DOT",u"make_JSON"]
    default_methods = standard_graphviz

    if u"method" not in args:
        args[u"method"] = default_methods
    elif args[u"method"] == [u"standard_JSON"]:
        args[u"method"] = standard_json
    elif args[u"method"] == [u"standard_GraphML"]:
        args[u"method"] = standard_graphml
    elif args[u"method"] == [u"standard_DOT"]:
        args[u"method"] = standard_dot
    elif args[u"method"] == [u"standard_graphviz"]:
        args[u"method"] = standard_graphviz

    first_method = args[u"method"][0]
    args[u"method"] = args[u"method"][1:]

    if first_method == u"make_JSON":
        return make_json(args)

    elif first_method == u"to_text":
        return to_text(args)

    elif first_method == u"output_text":
        return output_text(args)

    elif first_method == u"JSON_to_GraphML":
        return json_to_graphml(args)

    elif first_method == u"JSON_to_DOT":
        return json_to_dot(args)

    elif first_method == u"graphviz":
        return graphviz(args)

    else:
        print "Unrecognised method!"


def getargs():
    arguments = {}
    for (k,v) in cgi.parse_qsl(os.getenv("QUERY_STRING", "")):
        if k not in arguments:
            arguments[k] = []
        arguments[k].append(v)
    return arguments


def makeargs(url,d):
    l = []
    for (k,a) in d.iteritems():
        l.extend(a)
    return "%s?%s"%(url,"&".join("%s=%s"%(cgi.escape(k),cgi.escape(v)) for (k,v) in l))


def make_json(args):
    scraperwiki.sqlite.attach("scraperwiki_scraper_for_scraping_scrapers")
    new_nodes = set(args[u"entity"])
    old_nodes = set()
    edges = []
    while len(new_nodes) > 0:
        node = new_nodes.pop()
        old_nodes.add(node)
        for d in scraperwiki.sqlite.select('`from`,`to`,`type`,`strength` FROM scraperwiki_scraper_for_scraping_scrapers.swdata WHERE (`from` = ?)',(node,)):
            edges.append(d)
            to_node = d["to"]
            if to_node not in old_nodes and to_node not in new_nodes:
                new_nodes.add(to_node)
        for d in scraperwiki.sqlite.select('`from`,`to`,`type`,`strength` FROM scraperwiki_scraper_for_scraping_scrapers.swdata WHERE (`to` = ?)',(node,)):
            edges.append(d)
            from_node = d["from"]
            if from_node not in old_nodes and from_node not in new_nodes:
                new_nodes.add(from_node)
    return {"nodes":list(old_nodes), "edges":edges}


def to_text(args):
    return str(main(args))


class Tag():
    def __init__(self,s,tag,attribs={}):
        self.s = s
        self.tag = tag
        self.attribs = attribs
    def attriblist(self):
        return " ".join('%s="%s"'%(k,v) for (k,v) in self.attribs.iteritems())
    def __enter__(self):
        if self.attribs == {}:
            self.s.write("<%s>"%self.tag)
        else:
            self.s.write("<%s %s>"%(self.tag,self.attriblist()))
    def __exit__(self,errtype,val,trace):
        self.s.write("</%s>"%self.tag)
        return False
def tag(s,t,attribs={}):
    s.write("<%s %s/>"%(t," ".join('%s="%s"'%(k,v) for (k,v) in attribs.iteritems())))


def output_text(args):
    # doesn't generate a full html page
    s = cStringIO.StringIO()
    with Tag(s,"p"):
        s.write(cgi.escape(main(args)))
    print s.getvalue()
    s.close()


def json_to_dot(args):
    json = main(args)
    nodes = json["nodes"]
    edges = json["edges"]
    edge_colours = {"common code":"red", "mention":"green", "attachment":"dark grey"}
    directions = {"common code":"none", "mention":"forward", "attachment":"forward"}

    s = cStringIO.StringIO()
    s.write("digraph Network\n")
    s.write("{\n")

    for n in nodes:
        colour = "cyan" # want yellow for views
        s.write("node [colour=%s, shape=box]; %s;\n"%(colour,n))

    for e in edges:
        ### add links
        ### adjust "common code" thicknesses
        colour = edge_colours[e["type"]]
        direction = directions[e["type"]]
        s.write("edge [colour=%s, dirType=%s]; %s->%s;"%(colour,direction,e["from"],e["to"]))

    s.write("}\n")
    a = s.getvalue()
    s.close()
    return a


def json_to_graphml(args):
    s = cStringIO.StringIO()
    s.write('<?xml version="1.0" encoding="UTF-8"?>')
    with Tag(s,"graphml",{
        "xmlns":"http://graphml.graphdrawing.org/xmlns",
         "xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
         "xsi:schemaLocation":"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"}):
        json = main(args)
        nodes = json["nodes"]
        edges = json["edges"]
        tag(s,"key",{"id":"node_colour", "for":"node", "attr.name":"color", "attr.type":"string"})
        node_colours = {"scraper":"blue", "view":"yellow"}
        edge_colours = {"common code":"red", "mention":"green", "attachment":"dark grey"}
        tag(s,"key",{"id":"edge_colour", "for":"edge", "attr.name":"color", "attr.type":"string"})
        with Tag(s,"graph", {"id":"G"}):
            for n in nodes:
                with Tag(s,"node",{"id":n}):
                    with Tag(s,"data",{"key":"node_colour"}):
                        s.write(node_colours["scraper"]) # can't detect if something's a scraper or a view yet
            for d in edges:
                with Tag(s,"edge",{"source":(d["from"]), "target":(d["to"])}):
                    with Tag(s,"data",{"key":"edge_colour"}):
                        s.write(edge_colours[d["type"]])
    a = s.getvalue()
    s.close()
    return a


def graphviz(args):
    filename = "graphviz-output.tmp"
    format = args["graphviz-output"][0]
    args["graphviz-output"] = args["graphviz-output"][1:]
    obj = pydot.graph_from_dot_data(main(args))
    obj.write(path=filename,format=format)
    with open(filename,'w') as f:
        for l in f:
            print l

main()

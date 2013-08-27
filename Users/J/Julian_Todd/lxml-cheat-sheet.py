import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()

import os
import lxml.html
import cgi
import urllib
import re
import json
import sys


def Main():
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    if not qs.get("url"):
        print "No source URL specified, try for example: http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=http://www.lottery.culture.gov.uk/GrantDetails.aspx%3FID%3DAAE%25252f1%25252f000266127%26DBID%3DCH"
        sys.exit(0)

    url = qs.get("url")
    root = lxml.html.parse(url).getroot()

    if qs.get("csssel"):
        csssel = qs.get("csssel")[0]
        res = { "list": map(lxml.html.tostring, list(root.cssselect(csssel))) }
        res["code"] = "import lxml.html\nroot=lxml.html.parse('%s').getroot()\nnodes=root.cssselect('%s')\n" % (url, csssel)
        print json.dumps(res)
    else:
        fullpage(root, url)


def fullpage(root, url): 
    print """<html><head>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="https://media.scraperwiki.com/js/jquery.json-2.2.min.js"></script>
<style type="text/css">
    dt, dd, dl { margin-top:0; margin-bottom:0 }
    span.clas { color: green }
    span.href { color: red }
    span.id { color: blue }
    span.tail { text-decoration: underline }
    b.count-0 { color: #555 }
    div.treepane { width:90%; height:300px; overflow:scroll; border: thin black solid; margin-left:auto; margin-right:auto }
    pre#csprev { width:90%; height:300px; overflow:scroll; border: thin red solid; margin-left:auto; margin-right:auto }
    pre#cscode { width:90%; height:100px; background:#eee; overflow:scroll; border: thin red green; margin-left:auto; margin-right:auto }
    
    div#csssel { width:90%; height:5em; overflow:auto; border: thin blue solid; margin-left:auto; margin-right:auto }
    div#csssel span.taggroup { border: thin black dotted; }
    div#csssel span.tag { color:red; padding-left:3px }
    div#csssel span.clas { color:green; padding-left:3px }
    div#csssel span.id { color:blue; padding-left:3px }
    div#csssel span.choo { background:#fdd; }

    div.mrow { width:90%; margin-left:auto; margin-right:auto }
    span.matched { background:#ddf; border:thick red solid; }
</style>
</head><body>"""

    print '<h4>lxml tree selection for <a href="%s">%s</a></h4>' % (url, url)
    
    result = [ ]
    def noderecurse(result, node):
        if node.tag == 'meta':
            return
        result.append("<dl><dt>")
        if type(node) == lxml.html.HtmlComment:
            result.append('<b>COMMENT</b>')
            result.append('<span class="text">%s</span>' % re.sub("<", "&lt;", node.text))
            result.append("</dt></dl>")
            return
        result.append('<b class="count-%d">%s</b>' % (len(node), node.tag))
        vs = { "clas":node.attrib.get("class"), "id":node.attrib.get("id"), "text":node.text, "tail":node.tail, "href":node.attrib.get("href")}
        for k, v in vs.items():
            if v and v.strip():
                result.append('<span class="%s">%s</span>' % (k, re.sub("<", "&lt;", v)))
        result.append("</dt><dd>")
        for subnode in node:
            noderecurse(result, subnode)
        result.append("</dd></dl>")
    
    result = [ ]
    noderecurse(result, root)
    print '<div class="treepane">'
    print "\n".join(result)
    print '</div>'

    print '<div id="csssel"></div>'
    print '<div class="mrow"><input id="isearch" type="text"><input type="button" id="bsearch" value="Search"><input id="bselect" type="button" value="Select"></div>'
    print '<pre id="cscode"></pre>'
    print '<pre id="csprev"></pre>'

    print """
    <script>
    $(document).ready(function()
    {
        $('dd').hide();
        $('dt').click(function()
        {
            $(this).next().toggle();
            var selseq = [ ]; 
            $(this).parents("dl").each(function(index, Element) 
            { 
                var dt = $(Element).children('dt'); 
                var tag = dt.children("b").text(); 
                var clas = dt.children("span.clas").text(); 
                var id = dt.children("span.id").text();
                var res = [ ]; 
                res.push('<span class="taggroup" id="sind-'+index+'">'); 
                res.push('<span class="tag">'+tag+'</span>');
                if (id)
                    res.push('<span class="id">#'+id+'</span>'); 
                if (clas)
                    res.push('<span class="clas">.'+clas+'</span>');
                res.push('</span>');
                selseq.push(res.join(" ")); 
            }); 
            selseq.reverse(); 
            $('#csssel').html(selseq.join(" ")); 
            $('#csssel span.taggroup span').click(function() 
            { 
                if ($(this).hasClass('choo'))
                    $(this).removeClass('choo'); 
                else
                    $(this).addClass('choo'); 
            }); 
        });
    
        $('input#bsearch').click(function() 
        {
            $('span').removeClass("matched");
            var srch = $("input#isearch").val(); 
            $('dt span').each(function(index, Element) 
            { 
                if ($(Element).text().search(srch) != -1)
                {
                    $(Element).addClass("matched"); 
                    var pch = $(Element).parents("dl"); 
                    for (var i = 0; i < pch.length; i++)
                        $(pch[i]).children('dd').show(); 
                }
            })
        }); 

        $('input#bselect').click(function()
        {
            var csell = [ ]; 
            var spanup = undefined; 
            $('#csssel span.choo').each(function(index, Element)
            {
                var lspanup = $(Element).parent().attr('id'); 
                if ((spanup != lspanup) && (csell.length > 0))
                    csell.push(' ');
                csell.push($(Element).text()); 
                spanup = lspanup; 
            }); 
            $.ajax({data:{url:$('h4 a').attr('href'), "csssel":csell.join("")}, success: function(data) 
            {
                var mats = $.evalJSON(data); 
                $('#cscode').text(mats.code);
                if (mats.list.length > 0)    // needs to loop through and output a whole series of boxes here
                    $('#csprev').text(mats.list[0]);
            }}); 
        });
    })
    </script>
    </body></html>
    """

Main()


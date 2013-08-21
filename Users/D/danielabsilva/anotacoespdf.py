import scraperwiki
import urllib, urllib2
import lxml.etree, lxml.html
import re, os


def Pageblock(page, index):
    ''' 
    Print each page of the PDF in turn, outputting the contents as HTML.
    '''
    result = [ ]
    assert page.tag == 'page'
    height = int(page.attrib.get('height'))
    width = int(page.attrib.get('width'))
    number = page.attrib.get('number')
    assert page.attrib.get('position') == "absolute"

    result.append('<p>Page %s index %d height=%d width=%d</p>' % (number, index, height, width))
    result.append('<div class="page" style="height:%dpx; width:%dpx">' % (height, width))
    for v in page:
        if v.tag == 'fontspec':
            continue
        assert v.tag == 'text'
        text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
        top = int(v.attrib.get('top'))
        left = int(v.attrib.get('left'))
        width = int(v.attrib.get('width'))
        height = int(v.attrib.get('height'))
        fontid = v.attrib.get('font')
        style = 'top:%dpx; left:%dpx; height:%dpx; width:%dpx' % (top, left, height, width)
        result.append('    <div class="text fontspec-%s" style="%s">%s</div>' % (fontid, style, text))
    result.append('</div>')        
    return '\n'.join(result)


def Main(pdfurl):
    '''
    Take the URL of a PDF, and use scraperwiki.pdftoxml and lxml to output the contents
    as a styled HTML div. 
    '''
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)

    global styles
    fontspecs = { }

    # Get the PDF's internal styles: we'll use these to style the divs containing the PDF.
    for fontspec in root.xpath('page/fontspec'):
        id = fontspec.attrib.get('id')
        fontdesc = {'size':int(fontspec.attrib.get('size')), 'family':fontspec.attrib.get('family'), 'color':fontspec.attrib.get('color')}
        fontspecs[id] = fontdesc
        styles['div.fontspec-%s' % id] = 'color:%s;font-family:%s;font-size:%dpx' % (fontdesc['color'], fontdesc['family'], fontdesc['size'])

    # Output the view, with instructions for the user.
    print '<html dir="ltr" lang="en">'
    print '<head>'
    print '    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
    print '    <title>PDF to XML text positioning</title>'
    print '    <style type="text/css" media="screen">%s</style>' % "\n".join([ "%s { %s }" % (k, v)  for k, v in styles.items() ])
    print '    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>'
    print '    <script>%s</script>' % jscript
    print '</head>'

    print '<div class="info" id="info1">&lt;text block&gt;</div>'
    print '<div class="info" id="info2">&lt;position&gt;</div>'

    print '<div class="heading">'
    print '<h2>Graphical preview of scraperwiki.pdftoxml(pdfdata)</h2>'

    print '<p>Click on a text line to see its coordinates and any other text that shares the same column or row.'
    print '   Useful for discovering what coordinates to use when extracting rows from tables in a document.</p>'
    print '<p>To do: track the coordinates of the mouse and cross reference with <a href="/cropper">cropper</a> technology.</p>'

    print '<p class="href"><a href="%s">%s</a></p>'% (pdfurl, pdfurl)
    print '<form id="newpdfdoclink">'
    print '    Another PDF link:'
    print '    <input type="text" name="url" value="" title="paste in url of new document">'
    print '    <input type="submit" value="Go">'
    print '</form>'
    ttx = re.sub('<', '&lt;', pdfxml)
    ttx = re.sub('\n', '\r\n', ttx) 
    print '<textarea class="pdfprev">%s</textarea>' % ttx[:5000]
    print '</div>'

    print '<p>There are %d pages</p>' % len(root)

    # Print each page of the PDF.
    for index, page in enumerate(root):
        print Pageblock(page, index)


# Global styles for the divs containing the PDF.
styles = {
"div#info1": "position:fixed; white-space:pre; background-color:#ffd; border: thin red solid; z-index: 50; top:0px;",
"div#info2": "position:fixed; white-space:pre; background-color:#ffd; border: thin red solid; z-index: 50; top:20px;",
"div.heading": "padding-left:150px;",
"p.href":    "font-size:60%",
"div.page":  "background-color:#fff; border:thin black solid; position:relative; margin:2em;",
"div.text":  "position:absolute; white-space:pre; background-color:#eee;",
"textarea.pdfprev":"white-space:pre; height:150px; width:80%",
"div.text:hover": "background-color:#faa; cursor:pointer",
"div.linev": "background-color:#fcc;",
"div.lineh": "background-color:#fce;",
}

# Global JavaScript allowing the user to click on an area of the PDF div, and see the 
# underlying PDF source.
jscript = """
    var rfontspec = new RegExp('fontspec-(\\\\w+)');

    $(function()
    {
        $('div.text').click(function ()
        {
            var top = parseInt($(this).css('top'));
            var left = parseInt($(this).css('left'));
            var width = parseInt($(this).css('width'));
            var height = parseInt($(this).css('height'));
            var clas = $(this).attr('class');
            var lfont = rfontspec.exec(clas);
            var font = (lfont ? lfont[1] : clas);

            $('div#info1').text($(this).html());
            $('div#info2').text('top='+top + ' bottom='+(top+height)+ ' left='+left + ' right='+(left+width) + ' font='+font);
            
            $('div.text').each(function()
            {
                var lleft = parseInt($(this).css('left'));
                if (lleft == left)
                    $(this).addClass('linev');
                else
                    $(this).removeClass('linev');

                var ltop = parseInt($(this).css('top'));
                if (ltop == top)
                    $(this).addClass('lineh');
                else
                    $(this).removeClass('lineh');
            });
        });
    });
"""


    
# Check for a PDF URL entered by the user: if none, use our default URL.
urlquery = os.getenv('URLQUERY')
if urlquery:
    assert urlquery[:4] == 'url=', urlquery
    pdfurl = urllib.unquote(urlquery[4:])
else:
    pdfurl = "http://www.epa.ie/downloads/pubs/other/corporate/oee/web%20list%20of%20files%20Dublin%20oct2010.pdf"
Main(pdfurl)

#!/usr/bin/env python
#
# Copyright (c) 2010 Richard Boulton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Scrape data from the output of "pdftohtml -xml"

"""

from lxml import etree
import re

class FontSpec(object):
    """A Font specification.

    Each specification has the attributes:

     - `size`: point size of font.
     - `family`: font family (eg, "Helvetica").
     - `color`: RGB colour of font.
     - `number`: The fontspec number assigned by pdftohtml.

    The colour can be accessed as "colour", too, for users of English spelling.

    """
    __slots__ = ('family', 'size', 'color', 'number')
    def __init__(self, atts, number):
        self.family = atts['family']
        self.size = float(atts['size'])
        self.color = atts['color']
        self.number = number

    @property
    def colour(self):
        return self.color

    def __str__(self):
        return "FontSpec(%d %s %s %s)" % (self.number, self.family, self.size,
                                          self.color)

    def __repr__(self):
        return "FontSpec({'number': %d, 'family': %r, 'size': %r, " \
               "'color': %r})" % (self.number, self.family, self.size,
                                  self.color)


class DimensionedElement(object):
    def __init__(self):
        self.xoffset = 0
        self.yoffset = 0

    @property
    def top(self):
        return float(self.element.attrib['top']) + self.yoffset

    @property
    def left(self):
        return float(self.element.attrib['left']) + self.xoffset

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def right(self):
        return self.left + self.width

    @property
    def width(self):
        return float(self.element.attrib['width'])

    @property
    def height(self):
        return float(self.element.attrib['height'])


class Text(DimensionedElement):
    """A piece of text, with associated formatting information.

    """
    def __init__(self, element, page, fontspec):
        self.element = element
        self.page = page
        self.fontspec = fontspec
        self.text = etree.tostring(self.element, method="text", encoding=unicode)
        self.props = {}
        DimensionedElement.__init__(self)

    @property
    def font(self):
        return int(self.element.attrib['font'])

    def __str__(self):
        return "Text(%s, %s, %s, %s)" % (self.text, self.page.number,
                                         self.fontspec, self.props)

    def __repr__(self):
        return "<Text(%r, page=%s, fontspec=%r, props=%r)>" % \
            (etree.tostring(self.element, encoding=unicode),
             self.page.number, self.fontspec, self.props)


class Page(DimensionedElement):
    """A page.

    The element corresponding to the page is available as the `element`
    property.

    """
    def __init__(self, element):
        self.element = element
        DimensionedElement.__init__(self)

    @property
    def number(self):
        return self.element.attrib['number']

    def __str__(self):
        return "Page(%s)" % (self.number)

    def __repr__(self):
        return "<Page(%r)>" % etree.tostring(self.element, encoding=unicode)


class PdfToHTMLOutputParser(object):
    """Parse an XML document produced from pdftohtml.

    """
    def __init__(self, fd):
        self.fontspecs = {}
        self.tree = etree.parse(fd, etree.HTMLParser(encoding='utf8'))

        for event, spec in etree.iterwalk(self.tree, tag='fontspec'):
            atts = spec.attrib
            fontid = int(atts['id'])
            assert fontid not in self.fontspecs
            self.fontspecs[fontid] = FontSpec(atts, fontid)

    def fontspec(self, fontid):
        """Get the fontspec for a fontspec ID number.

        """
        return self.fontspecs[int(fontid)]

    def pages(self):
        """Iterate over the pages in the document.

        """
        for event, page in etree.iterwalk(self.tree, tag='page'):
            yield Page(page)

    def text(self, page=None, merge_verticals=False):
        """Get the text items.

        If `page` is supplied, it should be a Page (as returned by
        self.pages())

        If `merge_verticals` is supplied, the vertical offsets of items will be
        adjusted such that pages following the first appear immediately after
        the 

        """
        def text_for_page(page):
            for event, text in etree.iterwalk(page.element, tag='text'):
                fontid = text.attrib['font']
                yield Text(text, page, self.fontspec(text.attrib['font']))

        if page is None:
            if merge_verticals:
                offset = 0
                for event, page in etree.iterwalk(self.tree, tag='page'):
                    page = Page(page)
                    items = list(text_for_page(page))
                    if len(items) == 0:
                        continue
                    ymin = 9999999999999999
                    ymax = 0
                    for item in items:
                        if item.text.strip() == '':
                            continue
                        ymin = min(ymin, item.top)
                        ymax = max(ymax, item.bottom)

                    for item in items:
                        if item.text.strip() == '':
                            continue
                        item.yoffset = offset - ymin
                        yield(item)
                    offset += (ymax - ymin)
            else:
                for event, page in etree.iterwalk(self.tree, tag='page'):
                    page = Page(page)
                    for item in text_for_page(page):
                        yield(item)
        else:
            for item in text_for_page(page):
                yield(item)


def calc_lines(items):
    """Group a list of items into lines.

    Returns a list of lists of items.

    """
    # Cope with iterator inputs by forcing into a list.
    items = list(items)

    # Build a list of line centrepoints, and widths.  First we build a list of
    # the centrepoints and widths of all the items, then we iterate through
    # these and merge them together where the centrepoint of a line overlaps an
    # existing line width.

    centres = []
    for item in items:
        centres.append(((item.top + item.bottom) / 2,
                        (item.bottom - item.top) / 2))
    centres.sort()
    lines = []
    curline = centres[0]
    for line in centres:
        dist = line[0] - curline[0]
        if dist < max(line[1], curline[1]):
            curline = ((line[0] + curline[0]) / 2,
                        max(line[1], curline[1]))
        else:
            lines.append(curline)
            curline = line
    lines.append(curline)
    lines.sort()

    # Group elements into lines, by iterating through them in sorted
    # (top->bottom, left->right) order, assigning them to the first
    # relevant line.
    groups = []
    linenum = 0
    curgroup = None
    for item in sorted(items, key=lambda x: (x.top, x.left)):
        while linenum < len(lines):
            centre, wid = lines[linenum]
            if abs((item.top + item.bottom) / 2 - centre) < wid:
                # item sits on line, so add it.
                if curgroup is None:
                    curgroup = []
                    groups.append(curgroup)
                curgroup.append(item)
                break
            elif item.top < centre:
                # item is above the line, so we've somehow missed it
                # This should rarely happen, but could if we've computed a
                # centre-line too harshly.  Put the item on a line of its
                # own; not ideal, but better than losing it.
                groups.append([item])
                curgroup = None
                break
            curgroup = None
            linenum += 1
    return groups


def linear_dist((a1, a2), (b1, b2)):
    """Return the linear distance between two ranges (a1->a2) and (b1->b2).

    """
    if a1 < b1:
        dist = b1 - a2
    else:
        dist = a1 - b2
    if dist < 0:
        return 0
    return dist


class TextArea(object):
    def __init__(self, item):
        self.left = item.left
        self.right = item.right
        self.top = item.top
        self.bottom = item.bottom

        # Extra offsets to grab items to the left, right, top, bottom.
        self.grab = [0, 0, 0, 0]

        self.items = []
        self.lines = None # this is populated by self.assign_lines()
        self.props = {}
        self.add(item)

    def dist(self, item):
        """Return the distance between this area and a new item.

        """
        # Calculate the horizontal distance
        if self.left < item.left:
            # item is on the right: distance is from its left to my right
            hdist = item.left - self.right - self.grab[1]
        else:
            # item is on the left: distance is from its right to my left
            hdist = self.left - item.right - self.grab[0]
        if hdist < 0:
            hdist = 0

        # Calculate the vertical distance
        if self.top < item.top:
            # item is on the bottom: distance is from its top to my bottom
            vdist = item.top - self.bottom - self.grab[3]
        else:
            # item is on the top: distance is from its bottom to my top
            vdist = self.top - item.bottom - self.grab[2]
        if vdist < 0:
            vdist = 0

        return hdist, vdist, hdist + vdist

    def add(self, item):
        self.items.append(item)
        self.left = min(self.left, item.left)
        self.right = max(self.right, item.right)
        self.top = min(self.top, item.top)
        self.bottom = max(self.bottom, item.bottom)
        self.grab = [0, 0, 0, 0]
        for k, v in item.props.iteritems():
            if k == 'grableft':
                self.grab[0] = float(v)
            elif k == 'grabright':
                self.grab[1] = float(v)
            elif k == 'grabtop':
                self.grab[2] = float(v)
            elif k == 'grabbottom':
                self.grab[3] = float(v)
            elif k not in self.props:
                self.props[k] = v

    def assign_lines(self):
        """Group the items into lines.

        """
        self.lines = calc_lines(self.items)

    @staticmethod
    def line_text(line):
        """Get the text from a line of items, inserting space if needed.

        """
        lineitems = []
        previtem = None
        for item in line:
            if previtem and \
                linear_dist((previtem.left, previtem.right),
                            (item.left, item.right)) > item.fontspec.size:
                # Add a space when there's a gap between items
                lineitems.append(' ')
            lineitems.append(item.text)
            previtem = item
        return ''.join(lineitems).strip()

    @property
    def text(self):
        """Get the text in the area as a string, separated by newlines.

        """
        result = []
        for line in self.lines:
            result.append(self.line_text(line))
            result.append('\n')
        return ''.join(result).strip()

    @property
    def segments(self):
        """Get the segements of text in an area.

        Usually, this is just the lines, but if any items contain the
        "startitem" property, items are split on this property instead.

        """
        startitem = False
        for item in self.items:
            if item.props.get('startitem', None):
                startitem = True
                break

        result = []
        if startitem:
            segment = []

            for line in self.lines:
                linesegment = []
                for item in line:
                    if item.props.get('startitem', None):
                        line_text = self.line_text(linesegment)
                        if line_text:
                            segment.append(u'\n')
                            segment.append(line_text)
                        segment_text = ''.join(segment).strip()
                        if segment_text:
                            result.append(segment_text)
                        linesegment = [item]
                        segment = []
                    else:
                        linesegment.append(item)
                line_text = self.line_text(linesegment)
                if line_text:
                    segment.append(u'\n')
                    segment.append(line_text)
            segment_text = ''.join(segment).strip()
            if segment_text:
                result.append(segment_text)
        else:
            for line in self.lines:
                result.append(self.line_text(line))
        return result

    def __str__(self):
        return "TextArea((%.1f, %.1f), (%.1f, %.1f))" % \
            (self.left, self.right, self.top, self.bottom)


class IgnoreItem(Exception):
    """Exception raised to indicate that an item should be ignored.

    """
    pass

def act_ignore_empty():
    """Cause empty items to be ignored.

    """
    def fn(item):
        if len(item.text.strip()) == 0:
            raise IgnoreItem
    return fn

def act_bullet():
    """Check for items which start with a bullet point.

    """
    def fn(item):
        ltext = item.text.lstrip()
        if ltext[0] == u'\uf0b7' or ltext[0] == u'\uf0a7':
            item.props['startitem'] = True
            item.text = ltext[1:]
            if item.text.strip() == '':
                # There's no text after the bullet, so we should try to attach
                # to a following item.
                item.props['grabright'] = 300
    return fn

def act_weights():
    """Add properties based on font weights.

    """
    def fn(item):
        for child in item.element:
            tag = child.tag.lower()
            if tag == 'b':
                item.props['bold'] = True
            elif tag == 'i':
                item.props['italic'] = True
    return fn

def act_patterns(patterns):
    """Check for matches to known patterns.

    """
    def fn(item):
        text = item.text.strip()
        for pattern, item_type in patterns:
            if isinstance(pattern, basestring):
                if pattern.strip() == text:
                    item.props['type'] = item_type
                    break
            elif pattern.search(text):
                item.props['type'] = item_type
                break
    return fn

def act_colon_end():
    """Look for items which end with a colon, and mark them as wanting
    something to follow them on the right.

    """
    def fn(item):
        text = item.text.strip()
        if text.endswith(':'):
            item.props['grabright'] = 300
    return fn

class TextGrouper(object):
    """Code to group text objects on a page into some kind of meaningful form.

    Various heuristics are used here, and can be controlled by a set of
    special functions which are run when items come in.

    """
    def __init__(self):
        self.areas = []
        self.patterns = []

        # Some special actions.
        # These consist of a callable, which can raise StopIteration to
        # indicate that no further special actions should be performed, or
        # raise IgnoreItem to cause the item to be ignored.  It may also modify
        # the item as desired (usually by adding items to item.props).

        self.special_fns = [
            act_ignore_empty(),
            act_weights(),
            act_patterns(self.patterns),
            act_bullet(),
            act_colon_end(),
        ]

    def add_patterns(self, *titles):
        self.patterns.extend(titles)

    def merge_item(self, item):
        """Merge an existing item into the nearest text area.

        """
        if len(self.areas) == 0:
            self.areas.append(TextArea(item))
            return

        closest = None
        for num, area in enumerate(self.areas):
            if item.props.get('type', None) != None:
                if area.props.get('type', None) != item.props['type']:
                    continue
            hdist, vdist, dist = area.dist(item)
            if closest is None:
                closest = (num, dist, hdist, vdist)
                continue
            if closest[1] > dist:
                closest = (num, dist, hdist, vdist)

        if closest is None or \
           closest[2] > float(item.fontspec.size) or \
           closest[3] > item.height / 2:
            area = TextArea(item)
            self.areas.append(area)
        else:
            area = self.areas[closest[0]]
            area.add(item)

    def group(self, textitems):
        """Group the supplied list of items into TextArea objects.

        """
        # Sort the items into lines, then flatten that list to just get a list
        # in sorted order by line then x pos.
        text_in_lines = []
        for line in calc_lines(textitems):
            line.sort(key = lambda x: x.left)
            text_in_lines.extend(line)

        for item in text_in_lines:
            stext = item.text.strip()
            action = None
            # Add a space for additional properties on the item
            item.props = {}

            # Apply the special actions
            ignore = False
            try:
                for special_fn in self.special_fns:
                    special_fn(item)
            except StopIteration:
                pass
            except IgnoreItem:
                continue

            # Merge the item into the existing groups.
            self.merge_item(item)

        # Tidy up each area, putting content into lines.
        for area in self.areas:
            area.assign_lines()

    def display(self):
        for area in self.areas:
            print '{'
            for line in area.lines:
                print '  ' + str([(item.text, item.props) for item in line])
            print '}'

    def display_full(self):
        for area in self.areas:
            print area, area.props
            for line in area.lines:
                print '  ['
                for item in line:
                    print "   ", repr(item.text), item.fontspec, item.props
                print '  ]'

def iter_areas():
    import scraperwiki
    import StringIO

    pdfurl = "http://www.appc.org.uk/appc/filemanager/root/site_assets/pdfs/appc_register_entry_for_1_december_2009_to_28_february_2010.pdf"
    pdf = scraperwiki.scrape(pdfurl)
    print "Converting pdf to xml"
    xml = scraperwiki.pdftoxml(pdf)
    print "got xml"
    xmlfd = StringIO.StringIO(xml)
    doc = PdfToHTMLOutputParser(xmlfd)
    print "got doc"

    #import sys
    #doc = PdfToHTMLOutputParser(open(sys.argv[1]))

    org = {}
    grouper = TextGrouper()
    grouper.add_patterns(
        (re.compile("APPC register entry ", re.IGNORECASE), "dates"),
        ("Address(es) in UK", "address"),
        ("Address in UK", "address"),
        ("Contact", "contact"),
        ("Offices outside UK", "section"),
        (re.compile("providing PA consultancy services",
                    re.IGNORECASE), "section"),
        (re.compile("clients for whom", re.IGNORECASE), "section"),
    )
    def font_0(item):
        if item.fontspec.number == 0:
            item.props['type'] = 'name'
            item.props['grabbottom'] = 20
            print "Marked title:", repr(item.text)
    grouper.special_fns.append(font_0)
    grouper.group(doc.text(merge_verticals=True))
    #grouper.display()
    #grouper.display_full()
    for area in grouper.areas:
        yield area

def store_org(org):
    if len(org.data) == 0:
        return
    import scraperwiki, json
    data = json.dumps(org.data, indent=4)
    scraperwiki.datastore.save(unique_keys=['name'], data={'name': ''.join(org.data['name']), 'data': data})

# Map from section names to the names we want to store:
section_maps = {
    'address': 'address',
    'contact': 'contact',
    'dates': 'dates',
    'name': 'name',
    'sect_Fee-Paying Clients for whom only UK monitoring services provided this quarter': 'monitoring',
    'sect_Fee-Paying clients for whom UK PA consultancy services provided this quarter': 'consultancy',
    'sect_Offices outside UK': 'outside_offices',
    'sect_Pro-Bono Clients for whom consultancy and/or monitoring services have been provided\nthis quarter': 'probono',
    'sect_Pro-Bono Clients for whom consultancy and/or monitoring services have been provided this\nquarter': 'probono',
    'sect_Pro-Bono Clients for whom consultancy and/or monitoring services have been provided this quarter': 'probono',
    'sect_Staff (employed and sub-contracted) providing PA consultancy services this quarter': 'staff',
}

class Organisation(object):
    def __init__(self):
        self.data = {}
    def add(self, section, value):
        if isinstance(value, basestring):
            value = [value]
        section = section_maps.get(section, section)
        self.data.setdefault(section, []).extend(value)

org = Organisation()
state = {}
for area in iter_areas():
    if area.items[0].fontspec.number == 0:
        store_org(org)
        org = Organisation()
        org.add('name', area.text)
        state = {}
        continue

    itemtype = area.items[0].props.get('type', None)
    if itemtype is not None:
        if itemtype == 'dates':
            org.add('dates', area.text)
        elif itemtype == 'address':
            state['address_x'] = (area.left, area.right)
        elif itemtype == 'contact':
            state['contact_x'] = (area.left, area.right)
        elif itemtype == 'section':
            state['section'] = area.text
            state['address_x'] = None
            state['contact_x'] = None
        else:
            raise ValueError("Unhandled itemtype %r" % itemtype)
        continue

    address_x = state.get('address_x', None)
    if address_x is not None:
        dist = linear_dist(address_x, (area.left, area.right))
        if dist == 0:
            org.add('address', area.segments)
            continue

    contact_x = state.get('contact_x', None)
    if contact_x is not None:
        dist = linear_dist(contact_x, (area.left, area.right))
        if dist == 0:
            org.add('contact', area.segments)
            continue

    section = state.get('section', None)
    if section is not None:
        org.add('sect_' + section, area.segments)
        continue

    print "UNHANDLED:", state, area, repr(area.text)
store_org(org)
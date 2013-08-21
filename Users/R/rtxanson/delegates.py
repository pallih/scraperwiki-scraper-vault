import os, sys
import scraperwiki
import lxml
import lxml.html

_C = lambda node, selector: node.cssselect(selector)

def toStr(i):
    if i is not None:
        return i
    return ''

def clean(root):

    table = _C(root, "table.alldelegates")[0]
    rows = _C(table, "tr")
    header, data = rows[0], rows[1::]

    def findtext(cell):
        link = _C(cell, 'a')
        if len(link) > 0:
            return ' '.join([a.text for a in link if a.text is not None])
        return cell.text

    header_names = ["Row","Ward","Precinct","ParkDist","Seat","InOut","UpDown","Role","RoleRank","Last Name","First Name","Address","Zipcode","WalkingSubCaucus","Replaced Del","Status"]
    def make_values(rs):
        for row in rs:
            d_v = [findtext(td) for td in _C(row, 'td')]
            stat = row.attrib.get('class')
            d_s = '?'
            if stat is not None:
                if stat.strip():
                    d_s = stat
            yield d_v[:] + [d_s]

    data_values = list(make_values(data))

    return header_names, data_values[1::]


def main():

    html = scraperwiki.scrape("http://xn--x2a.net/delegates.html", user_agent="mozilla/5.0 (compatible; msie 6.0; windows nt 5.1)")
    root = lxml.html.fromstring(html)

    header, values = clean(root)


    data = [dict(zip(header, r)) for r in values]


    # output here
    for d in data:
        scraperwiki.sqlite.save(unique_keys=["Row"], data=d)

main()

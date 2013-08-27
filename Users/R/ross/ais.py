import lxml.html
import string
import urlparse
import scraperwiki


for l in string.letters:
    first_page = "http://www.marinetraffic.com/ais/datasheet.aspx?datasource=V_SHIP&alpha=%s" % l
    second_page = first_page + "&orderby=TIMESTAMP&sort_order=DESC&var_page=2"

    items = []
    for page in [first_page,second_page]:
        doc = lxml.html.fromstring( scraperwiki.scrape( page ) )
        table = doc.cssselect('#datasheet table')[0]
        for row in table[1:]: # Ignore the header row
            nm = row[1].cssselect('a.data')[0]
            name = nm.text_content()
            name_link = urlparse.urljoin( "http://www.marinetraffic.com/ais/", nm.attrib.get('href'))
            mmsi = row[2].text_content()
            flag = row[3].text_content()
            typ = row[4].text_content()
            current_pos = row[5].text_content()
            current_port = row[6].text_content()
            last_position = row[7].text_content()
            last_port = row[8].text_content()
            area = row[9].text_content()
            items.append( dict(
                name = name, url = name_link, mmsi = mmsi, flag = flag, 
                type=typ, current_position=current_pos, last_position = last_position,
                last_port = last_port, area = area
            ) )
    scraperwiki.sqlite.save(['mmsi','current_position'], items)
    


"""
<td align="left"><font class="data"><a class="data" href="shipdetails.aspx?MMSI=412751680">ZHE YU JI 651</a></font></td><td align="left"><font class="data">412751680</font></td><td align="left"><font class="data">China</font></td><td align="left"><font class="data">Cargo</font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=10&amp;mmsi=412751680&amp;centerx=121.1276&amp;centery=28.05916">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=&amp;centery=&amp;zoom=">&nbsp;</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=9&amp;olddate=lastknown&amp;oldmmsi=412751680">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=119.4765&amp;centery=25.994&amp;zoom=14">FUZHOU</a></font></td><td align="left"><font class="data">China Sea</font></td><td align="left"><font class="data"><a class="data" href="showallphotos.aspx?mmsi=412751680">0 Photos</a></font></td></tr>"""import lxml.html
import string
import urlparse
import scraperwiki


for l in string.letters:
    first_page = "http://www.marinetraffic.com/ais/datasheet.aspx?datasource=V_SHIP&alpha=%s" % l
    second_page = first_page + "&orderby=TIMESTAMP&sort_order=DESC&var_page=2"

    items = []
    for page in [first_page,second_page]:
        doc = lxml.html.fromstring( scraperwiki.scrape( page ) )
        table = doc.cssselect('#datasheet table')[0]
        for row in table[1:]: # Ignore the header row
            nm = row[1].cssselect('a.data')[0]
            name = nm.text_content()
            name_link = urlparse.urljoin( "http://www.marinetraffic.com/ais/", nm.attrib.get('href'))
            mmsi = row[2].text_content()
            flag = row[3].text_content()
            typ = row[4].text_content()
            current_pos = row[5].text_content()
            current_port = row[6].text_content()
            last_position = row[7].text_content()
            last_port = row[8].text_content()
            area = row[9].text_content()
            items.append( dict(
                name = name, url = name_link, mmsi = mmsi, flag = flag, 
                type=typ, current_position=current_pos, last_position = last_position,
                last_port = last_port, area = area
            ) )
    scraperwiki.sqlite.save(['mmsi','current_position'], items)
    


"""
<td align="left"><font class="data"><a class="data" href="shipdetails.aspx?MMSI=412751680">ZHE YU JI 651</a></font></td><td align="left"><font class="data">412751680</font></td><td align="left"><font class="data">China</font></td><td align="left"><font class="data">Cargo</font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=10&amp;mmsi=412751680&amp;centerx=121.1276&amp;centery=28.05916">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=&amp;centery=&amp;zoom=">&nbsp;</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=9&amp;olddate=lastknown&amp;oldmmsi=412751680">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=119.4765&amp;centery=25.994&amp;zoom=14">FUZHOU</a></font></td><td align="left"><font class="data">China Sea</font></td><td align="left"><font class="data"><a class="data" href="showallphotos.aspx?mmsi=412751680">0 Photos</a></font></td></tr>"""import lxml.html
import string
import urlparse
import scraperwiki


for l in string.letters:
    first_page = "http://www.marinetraffic.com/ais/datasheet.aspx?datasource=V_SHIP&alpha=%s" % l
    second_page = first_page + "&orderby=TIMESTAMP&sort_order=DESC&var_page=2"

    items = []
    for page in [first_page,second_page]:
        doc = lxml.html.fromstring( scraperwiki.scrape( page ) )
        table = doc.cssselect('#datasheet table')[0]
        for row in table[1:]: # Ignore the header row
            nm = row[1].cssselect('a.data')[0]
            name = nm.text_content()
            name_link = urlparse.urljoin( "http://www.marinetraffic.com/ais/", nm.attrib.get('href'))
            mmsi = row[2].text_content()
            flag = row[3].text_content()
            typ = row[4].text_content()
            current_pos = row[5].text_content()
            current_port = row[6].text_content()
            last_position = row[7].text_content()
            last_port = row[8].text_content()
            area = row[9].text_content()
            items.append( dict(
                name = name, url = name_link, mmsi = mmsi, flag = flag, 
                type=typ, current_position=current_pos, last_position = last_position,
                last_port = last_port, area = area
            ) )
    scraperwiki.sqlite.save(['mmsi','current_position'], items)
    


"""
<td align="left"><font class="data"><a class="data" href="shipdetails.aspx?MMSI=412751680">ZHE YU JI 651</a></font></td><td align="left"><font class="data">412751680</font></td><td align="left"><font class="data">China</font></td><td align="left"><font class="data">Cargo</font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=10&amp;mmsi=412751680&amp;centerx=121.1276&amp;centery=28.05916">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=&amp;centery=&amp;zoom=">&nbsp;</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?zoom=9&amp;olddate=lastknown&amp;oldmmsi=412751680">2012-06-08 18:05</a></font></td><td align="left"><font class="data"><a class="data" href="default.aspx?centerx=119.4765&amp;centery=25.994&amp;zoom=14">FUZHOU</a></font></td><td align="left"><font class="data">China Sea</font></td><td align="left"><font class="data"><a class="data" href="showallphotos.aspx?mmsi=412751680">0 Photos</a></font></td></tr>"""
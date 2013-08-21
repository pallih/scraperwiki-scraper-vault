import scraperwiki
import lxml.html
import lxml.etree

#here's a typical full url: http://www.hfemsd2.dphe.state.co.us/hfd2003/dtl.aspx?id=01M130&ft=hospital
#then need to drill down to: http://www.hfemsd2.dphe.state.co.us/hfd2003/dtlocc06.aspx?id=01M130&ft=hospital
#then each of http://www.hfemsd2.dphe.state.co.us/hfd2003/occreport.aspx?id=01M130&ft=hospital&occ=1101M130001

urllist = ['01M130', '010210', '010907', '01W737', '010323', '010507', '010304', '010429', '010316', '010456', '010543', '010424', '010402', '01H523', '010650', '010623', '010417', '010486', '010493', '010625', '010130', '01U328', '011119', '011020', '010435', '011145', '010444', '25017J', '01C959', '01C882', '010302', '01I529', '010440', '010430', '2511OC', '010830', '010909', '010403', '01P254', '010112', '010501', '010628', '01B953', '010232', '0104HY', '010420', '010167', '010150', '010350', '010340', '010414', '01D460', '010120', '010807', '011213', '010804', '01J169', '011165', '010704', '0104MU', '010386', '010441', '01P638', '01V196', '01U246', '01Y763', '01J544', '010626', '01O618', '01K180', '010850', '010311', '010305', '010431', '010217', '011132', '251011', '010428', '011001', '010170', '01R345', '01I962', '0104MJ', '01D972', '010221', '011206', '010433', '010720', '01I155', '011160', '010908', '010140', '010436', '010542', '01A456', '010432', '010911', '010810', '010427', '010214', '010160', '010860', '010127']

for link in urllist:
    occurrencesurl = "http://www.hfemsd2.dphe.state.co.us/hfd2003/dtlocc06.aspx?id="+link+"&ft=hospital"
    print occurrencesurl
    html = scraperwiki.scrape(occurrencesurl)
    print html
    root = lxml.html.fromstring(html)
    #<td id="OccList">
    occurrences = root.cssselect('td#OccList a')
    for occurrence in occurrences:
        print "occurrencelink", occurrence.attrib.get('href')
        occurrencelink = "http://www.hfemsd2.dphe.state.co.us/hfd2003/"+occurrence.attrib.get('href')
        print occurrence.text
        html2 = scraperwiki.scrape(occurrencelink)
        print "html2", html2
        root2 = lxml.html.fromstring(html2)
        tablecells = root2.cssselect('table tr td#occReportText')
        for cell in tablecells:
            print "FACILITY", cell.text
#Our problem is that all other data is split by <br> tags which are not closed and cannot be grabbed in the normal way
#May be worth trying Beautiful Soup to see if it handles any better
#Here's another tip: http://stackoverflow.com/questions/13122353/parsing-html-using-lxml-html
#http://stackoverflow.com/questions/8788331/how-to-split-the-tags-from-html-tree        

#for link in urllist:
 #   fullurl = "http://www.hfemsd2.dphe.state.co.us/hfd2003/dtl.aspx?id="+link+"&ft=hospital"
  #  print fullurl
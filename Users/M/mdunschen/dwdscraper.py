import urllib2
import mechanize

#hi from flo

urlbase = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=dwdwww_klima_umwelt&_nfls=false"

urlsteps = [
    "http://www.dwd.de/",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=dwdwww_klima_umwelt&_nfls=false",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&activePage=&_nfls=false",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Content%2FOeffentlichkeit%2FKU%2FKU2%2FKU21%2Fklimadaten%2Fgerman%2Fteaser2__klimadaten__deutschland.html&_state=maximized&_windowLabel=T82002&lastPageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland",    
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fhome__nkdzdaten__node.html%3F__nnn%3Dtrue",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fdaten__zeitreihen__node.html%3F__nnn%3Dtrue",
    r"http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fausgabe__monatswerte__node.html%3F__nnn%3Dtrue"
]
url = r"http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fausgabe__monatswerte__node.html%3F__nnn%3Dtrue"


def navigateToClimateData():
    br = mechanize.Browser()
    print br
    br.set_handle_robots(False)
    print br, urlsteps[1]
    br.open(urlsteps[1])
    print br
    print "xxx = ", br.viewing_html()
    for step in urlsteps[2:]:
        print step[:10]
        br.open(step)
    
    return br    


def main():
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    print br
    br.set_handle_robots(False)
    print br
    br.open(urlsteps[-1])
    print [f.name for f in br.forms()]

main()




import urllib2
import mechanize

#hi from flo

urlbase = "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=dwdwww_klima_umwelt&_nfls=false"

urlsteps = [
    "http://www.dwd.de/",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=dwdwww_klima_umwelt&_nfls=false",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&activePage=&_nfls=false",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Content%2FOeffentlichkeit%2FKU%2FKU2%2FKU21%2Fklimadaten%2Fgerman%2Fteaser2__klimadaten__deutschland.html&_state=maximized&_windowLabel=T82002&lastPageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland",    
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fhome__nkdzdaten__node.html%3F__nnn%3Dtrue",
    "http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fdaten__zeitreihen__node.html%3F__nnn%3Dtrue",
    r"http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fausgabe__monatswerte__node.html%3F__nnn%3Dtrue"
]
url = r"http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fausgabe__monatswerte__node.html%3F__nnn%3Dtrue"


def navigateToClimateData():
    br = mechanize.Browser()
    print br
    br.set_handle_robots(False)
    print br, urlsteps[1]
    br.open(urlsteps[1])
    print br
    print "xxx = ", br.viewing_html()
    for step in urlsteps[2:]:
        print step[:10]
        br.open(step)
    
    return br    


def main():
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    print br
    br.set_handle_robots(False)
    print br
    br.open(urlsteps[-1])
    print [f.name for f in br.forms()]

main()





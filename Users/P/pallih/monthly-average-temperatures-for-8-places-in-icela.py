import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import time

#All data from the Icelandic Meterological Institution (www.vedur.is) - http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/langtimatoflur.html



######## data to process:

#Average temperature for Reykjavik, Iceland 1931 - 2000
reykjavik_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Reykjavik.txt'

#Average temperature for Stykkisholmur, Iceland 1823 - 1999
stykkisholmur_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Stykkisholmur.txt'

#Average temperature for Akureyri, Iceland 1931 - 1999
akureyri_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Akureyri.txt'

#Average temperature for Grimsstadir, Iceland 1931 - 1999
grimsstadir_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Grimsstadir.txt'

#Average temperature for Raufarhofn, Iceland 1931 - 1999
raufarhofn_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Raufarhofn.txt'

#Average temperature for Teigarhorn, Iceland 1873 - 2000
teigarhorn_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Teigarhorn.txt'

#Average temperature for Haell, Iceland 1931 - 1999
haell_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Haell.txt'

#Average temperature for Storhofdi, Iceland 1931 - 1999
storhofdi_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Storhofdi.txt'

def process(url,place):

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    lines = soup.string.split("\n")
    for line in lines[2:-1]:
        data = {}
        line = str(line)
        values = line.split()
        print values
        data['place'] = place
        data['year'] = values[1]
        data['jan'] = values[2]
        data['feb'] = values[3]
        data['mar'] = values[4]
        data['apr'] = values[5]
        data['may'] = values[6]
        data['jun'] = values[7]
        data['jul'] = values[8]
        data['aug'] = values[9]
        data['sep'] = values[10]
        data['oct'] = values[11]
        data['nov'] = values[12]
        data['dec'] = values[13]
        data['year_avg'] = values[14]
        scraperwiki.datastore.save(["place","year"], data)
 
process(reykjavik_url,'reykjavik')
process(stykkisholmur_url,'stykkisholmur')
process(akureyri_url,'akureyri')
process(grimsstadir_url,'grimsstadir')
process(raufarhofn_url,'raufarhofn')
process(teigarhorn_url,'teigarhorn')
process(haell_url,'haell')
process(storhofdi_url,'storhofdi')import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import time

#All data from the Icelandic Meterological Institution (www.vedur.is) - http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/langtimatoflur.html



######## data to process:

#Average temperature for Reykjavik, Iceland 1931 - 2000
reykjavik_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Reykjavik.txt'

#Average temperature for Stykkisholmur, Iceland 1823 - 1999
stykkisholmur_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Stykkisholmur.txt'

#Average temperature for Akureyri, Iceland 1931 - 1999
akureyri_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Akureyri.txt'

#Average temperature for Grimsstadir, Iceland 1931 - 1999
grimsstadir_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Grimsstadir.txt'

#Average temperature for Raufarhofn, Iceland 1931 - 1999
raufarhofn_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Raufarhofn.txt'

#Average temperature for Teigarhorn, Iceland 1873 - 2000
teigarhorn_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Teigarhorn.txt'

#Average temperature for Haell, Iceland 1931 - 1999
haell_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Haell.txt'

#Average temperature for Storhofdi, Iceland 1931 - 1999
storhofdi_url = 'http://andvari.vedur.is/vedurfar/yfirlit/hitatoflur/Storhofdi.txt'

def process(url,place):

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    lines = soup.string.split("\n")
    for line in lines[2:-1]:
        data = {}
        line = str(line)
        values = line.split()
        print values
        data['place'] = place
        data['year'] = values[1]
        data['jan'] = values[2]
        data['feb'] = values[3]
        data['mar'] = values[4]
        data['apr'] = values[5]
        data['may'] = values[6]
        data['jun'] = values[7]
        data['jul'] = values[8]
        data['aug'] = values[9]
        data['sep'] = values[10]
        data['oct'] = values[11]
        data['nov'] = values[12]
        data['dec'] = values[13]
        data['year_avg'] = values[14]
        scraperwiki.datastore.save(["place","year"], data)
 
process(reykjavik_url,'reykjavik')
process(stykkisholmur_url,'stykkisholmur')
process(akureyri_url,'akureyri')
process(grimsstadir_url,'grimsstadir')
process(raufarhofn_url,'raufarhofn')
process(teigarhorn_url,'teigarhorn')
process(haell_url,'haell')
process(storhofdi_url,'storhofdi')
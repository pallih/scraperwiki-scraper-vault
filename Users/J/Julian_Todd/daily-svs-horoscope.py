# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)
# Scrape all the shelley horoscopes for each day

import urllib
import re
import scraperwiki
import datetime

months = ["January", "February", "March", "April", "May", "June","July","August","September","October","November","December"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sargitarius","Capricorn","Aquarius","Pisces"]

for sign in signs:
    a = "http://www.shelleyvonstrunckel.com/scripts/%s.asp" % sign

    fin = urllib.urlopen(a)
    text = fin.read()
    fin.close()

    m = re.search("(?s)<table.*?>.*?Daily stars for today.*?&nbsp;(?:<[Bb]>)?(\d.*?)</font>.*?</table>.*?size='3'>(.*?)</font>.*?</table>", text)

    mdate = re.match("(\d+)&nbsp;(\w+)&nbsp;(\d+)", m.group(1))
    print sign
    print mdate.groups()
    print m.group(2)
    imonth = months.index(mdate.group(2)) + 1
    date = datetime.date(int(mdate.group(3)), imonth, int(mdate.group(1)))
    data = { "sign":sign, "date":date, "text":m.group(2) }
    scraperwiki.datastore.save(unique_keys=["date", "sign"], data=data)

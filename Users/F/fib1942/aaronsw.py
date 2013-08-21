from BeautifulSoup import BeautifulSoup
import urllib2

resp = urllib2.urlopen('http://www.aaronsw.com/weblog/fullarchive')
links =  BeautifulSoup(resp.read()).findAll('a')



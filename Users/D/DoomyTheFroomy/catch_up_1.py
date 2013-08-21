from BeautifulSoup import BeautifulSoup
from collections import deque
import scraperwiki
import urllib
import re
import simplejson
import urllib2

# Test after @llabball, besseren Weg gefunden
#catch = "http://query.yahooapis.com/v1/public/yql?#q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D0%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3Dabc9Krz1TOUJhdqI5P2ft13176a7f187%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20limit%2010&diagnostics=true"
#
#
#xml = scraperwiki.scrape(catch)
#print xml
#soup = BeautifulSoup(xml)
#print soup
#descs = soup.findAll('div')
#print descs
#
#for elem in descs:
#    elem = BeautifulSoup(elem.prettify())
#    print elem
#    txt = elem.findAll('p')
#    print txt
#
#scraperwiki.sqlite.execute("create table address(id int, `complete` string, `postal` string, `city` string, `district` string, `street` string, `number` string)")


###########################################
### Berlin ################################
###########################################
########### Pankow ########################
########### Prenzl Berg ###################
########### Charlottenburg ################
########### Zehlendorf ####################
########### Spandau #######################
########### Mitte #########################
########### Reinickendorf #################
########### Karlshorst ####################
########### Lichtenberg ###################
########### Friedrichshain ################
########### Kreuzberg #####################
########### Hohenschönhausen ##############
########### Neukölln ######################
########### Weißensee #####################
########### Steglitz ######################
########### Wedding #######################
########### Tiergarten ####################
########### Marzahn #######################
########### Hellersdorf ###################
########### Köpenick ######################
queue_berlin = deque(["http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3Dabc9Krz1TOUJhdqI5P2ft13176a7f187%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20limit%20100&format=json&diagnostics=true"
, "http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7896%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcGrxEQ3wikJhXhwTfgt13185c3eecd%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20&format=json&diagnostics=true"
, "http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7899%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcmejjZ2iu8y-bEB_fgt13185fa1519%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7597%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131870f263f%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20limit%2010&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7935%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt1318714a434%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7920%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcmejjZ2iu8y-bEB_fgt13185ff18b2%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7889%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcmejjZ2iu8y-bEB_fgt1318601631b%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'%20&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7901%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131871f8535%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true", "http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D-1%26suchart%3D1%26objecttype%3D1%26district%3D7715%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131872d4482%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7879%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131873a6fcc%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7605%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131873c33b3%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7876%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcetFlBx1QtEaj1Pdhgt131873e5b01%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7617%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt131875858a5%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7891%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt1318759f2c1%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7931%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt131875b9c48%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7922%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt131875d4d27%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7930%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt131875ee1de%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7926%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt13187604316%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7888%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt131876239ae%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7614%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt1318763d071%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true","http://query.yahooapis.com/v1/public/yql?q=Select%20*%20from%20html%20where%20url%20in%20(select%20link%20from%20rss%20where%20url%3D%22http%3A%2F%2Fwww.immonet.de%2Fimmobiliensuche%2Frss.do%3Fsortby%3D19%26marketingtype%3D2%26suchart%3D1%26objecttype%3D1%26district%3D7877%26parentcat%3D1%26city%3D87372%26listsize%3D100%26orderby%3Dobjectpublish%26ordertype%3Dasc%26rssid%3DabcvtuCpL4b9O-WQawhgt1318765a3a9%26ext%3D.xml%22)%20and%20xpath%3D'%2F%2Fdiv%5B%40id%3D%22objektAdresse%22%5D%2Fdiv'&format=json&diagnostics=true"])
for queue_res in queue_berlin:
    catch_json = queue_res 
    try:
        results_json = simplejson.loads(scraperwiki.scrape(catch_json))
    
        query = results_json['query']
    
        results_query = query['results']
        for result_div in results_query['div']:
            try:
                result_p = result_div['p']
                result_a = result_p['content']
                print result_a
                scraperwiki.sqlite.save(unique_keys=["id"], data={ "id":result_a, "Link": catch_json })
            except:
                print 'no address'
    
    except:
        print 'no result'




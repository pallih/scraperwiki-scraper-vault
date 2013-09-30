###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import os, sys
import scraperwiki
import simplejson
import urllib2
import re



# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ('ich bin','ich fühle')]
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for (q,table) in QUERY:
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(q), RESULTS_PER_PAGE, LANGUAGE, page)
        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            print results_json
            if len(results_json['results'])==0: break
            for result in results_json['results']:
                #print type(result['text'])
                #print "*" , re.findall(unicode("Männer", 'utf-8'), result['text'], re.I)
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id'] = result['from_user_id']
                #data['to_user'] = result['to_user']
                #data['to_user_id'] = result['to_user_id']
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['source'] = result['source']
                data['profile_image_url'] = result['profile_image_url']
                data['iso_language_code'] = result['iso_language_code']
                 
                thashtags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['hashtags']=' | '.join(thashtags)
                
                tuser=re.findall("@([a-z0-9]+)", result['text'], re.I)
                data['user identified']=' | '.join(tuser)
                
                thashtags=re.findall("RT @([a-z0-9]+)", result['text'], re.I)
                data['retweets']=' | '.join(thashtags)

                thashtags=re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", result['text'], re.I)
                data['links']=' | '.join(thashtags)
                
                #thashtags=re.findall(unicode("und", 'utf-8'), result['text'], re.I)
                #data['KeyStateXXXXXXXXXX']=len(thashtags)
                
                   
                thashtags=re.findall(unicode("ich bin aufgebracht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID16']=-0.0048
   
                thashtags=re.findall(unicode("ich bin aufgeregt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID17']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich elendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID52']=-0.0048
   
                thashtags=re.findall(unicode("ich bin matt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID119']=-0.0048
   
                thashtags=re.findall(unicode("ich bin melancholisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID120']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich mies", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID122']=-0.0048
   
                thashtags=re.findall(unicode("ich bin mutlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID127']=-0.0048
   
                thashtags=re.findall(unicode("ich bin müde", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID128']=-0.0048
   
                thashtags=re.findall(unicode("ich bin panisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID133']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich scheusslich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID154']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schlapp", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID156']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schmerzerfüllt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID159']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schwerfällig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID162']=-0.0048
   
                thashtags=re.findall(unicode("ich bin stupide", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID170']=-0.0048
   
                thashtags=re.findall(unicode("ich bin wahnsinnig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID249']=-0.0048
   
                thashtags=re.findall(unicode("ich bin scheisse", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID272']=-0.0226
   
                thashtags=re.findall(unicode("ich bin genervt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID274']=-0.0237
   
                thashtags=re.findall(unicode("ich bin schrecklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID276']=-0.0242
   
                thashtags=re.findall(unicode("ich fühle mich leer", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID279']=-0.025
   
                thashtags=re.findall(unicode("ich bin beängstigend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID288']=-0.0367
   
                thashtags=re.findall(unicode("ich fühle mich grässlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID300']=-0.0395
   
                thashtags=re.findall(unicode("ich bin launisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID306']=-0.0409
   
                thashtags=re.findall(unicode("ich fühle mich schäbig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID311']=-0.0421
   
                thashtags=re.findall(unicode("ich bin besorgt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID334']=-0.0482
   
                thashtags=re.findall(unicode("ich bin verletzlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID337']=-0.0487
   
                thashtags=re.findall(unicode("ich bin leblos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID338']=-0.049
   
                thashtags=re.findall(unicode("ich fühle mich elend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID346']=-0.0519
   
                thashtags=re.findall(unicode("ich bin unruhig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID353']=-0.0551
   
                thashtags=re.findall(unicode("ich bin traurig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID356']=-0.1266
   
                thashtags=re.findall(unicode("ich bin einsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID362']=-0.1634
   
                thashtags=re.findall(unicode("ich fühle mich scheußlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID387']=-0.1834
   
                thashtags=re.findall(unicode("ich fühle mich grauenhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID392']=-0.184
   
                thashtags=re.findall(unicode("ich bin zornig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID398']=-0.1853
   
                thashtags=re.findall(unicode("ich bin verzweifelt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID409']=-0.1947
   
                thashtags=re.findall(unicode("ich bin kritisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID416']=-0.203
   
                thashtags=re.findall(unicode("ich fühle mich scheiße", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID424']=-0.2945
   
                thashtags=re.findall(unicode("ich fühle mich beschissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID425']=-0.2947
   
                thashtags=re.findall(unicode("ich bin missgelaunt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID426']=-0.297
   
                thashtags=re.findall(unicode("ich bin unglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID429']=-0.301
   
                thashtags=re.findall(unicode("ich fühle mich energielos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID430']=-0.3037
   
                thashtags=re.findall(unicode("ich fühle mich furchtbar", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID432']=-0.3042
   
                thashtags=re.findall(unicode("ich bin debil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID435']=-0.306
   
                thashtags=re.findall(unicode("ich bin gestreßt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID446']=-0.3128
   
                thashtags=re.findall(unicode("ich bin kränklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID465']=-0.3172
   
                thashtags=re.findall(unicode("ich bin wütend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID484']=-0.3233
   
                thashtags=re.findall(unicode("ich fühle mich grauenvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID485']=-0.3238
   
                thashtags=re.findall(unicode("ich bin frustriert", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID488']=-0.3244
   
                thashtags=re.findall(unicode("ich bin labil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID501']=-0.326
   
                thashtags=re.findall(unicode("ich bin grimmig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID516']=-0.3295
   
                thashtags=re.findall(unicode("ich fühle mich kraftlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID533']=-0.3338
   
                thashtags=re.findall(unicode("ich bin machtlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID536']=-0.3351
   
                thashtags=re.findall(unicode("ich bin pessimistisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID540']=-0.3359
   
                thashtags=re.findall(unicode("ich fühle mich fürchterlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID542']=-0.3363
   
                thashtags=re.findall(unicode("ich bin unzufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID543']=-0.3363
   
                thashtags=re.findall(unicode("ich bin aggressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID595']=-0.4484
   
                thashtags=re.findall(unicode("ich fühle mich gräßlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID600']=-0.4529
   
                thashtags=re.findall(unicode("ich bin gekränkt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID601']=-0.453
   
                thashtags=re.findall(unicode("ich fühle mich ungeliebt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID602']=-0.4532
   
                thashtags=re.findall(unicode("ich bin arm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID605']=-0.4546
   
                thashtags=re.findall(unicode("ich fühle mich unangenehm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID622']=-0.4691
   
                thashtags=re.findall(unicode("ich bin krank", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID624']=-0.4694
   
                thashtags=re.findall(unicode("ich bin niedergeschlagen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID627']=-0.4708
   
                thashtags=re.findall(unicode("ich bin depressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID632']=-0.4715
   
                thashtags=re.findall(unicode("ich bin ängstlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID639']=-0.4735
   
                thashtags=re.findall(unicode("ich bin angespannt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID640']=-0.4744
   
                thashtags=re.findall(unicode("ich fühle mich entsetzlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID642']=-0.477
   
                thashtags=re.findall(unicode("ich bin zerrissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID644']=-0.4776
   
                thashtags=re.findall(unicode("ich fühle mich verheerend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID645']=-0.478
   
                thashtags=re.findall(unicode("ich fühle mich erbärmlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID649']=-0.4796
   
                thashtags=re.findall(unicode("ich fühle mich hilflos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID652']=-0.4827
   
                thashtags=re.findall(unicode("ich fühle mich nutzlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID654']=-0.485
   
                thashtags=re.findall(unicode("ich fühle mich katastrophal", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID659']=-0.4917
   
                thashtags=re.findall(unicode("ich bin verletzt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID669']=-0.5202
   
                thashtags=re.findall(unicode("ich fühle mich grausam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID684']=-0.625
   
                thashtags=re.findall(unicode("ich bin wertlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID685']=-0.6264
   
                thashtags=re.findall(unicode("ich bin unsicher", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID686']=-0.6268
   
                thashtags=re.findall(unicode("ich fühle mich sinnlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID688']=-0.6331
   
                thashtags=re.findall(unicode("ich fühle mich schlecht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID702']=-0.7706
   
                thashtags=re.findall(unicode("ich bin schwach", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID706']=-0.9206
   
                thashtags=re.findall(unicode("ich bin aktiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID715']=0.0911
   
                thashtags=re.findall(unicode("ich fühle mich angenehm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID725']=0.4887
   
                thashtags=re.findall(unicode("ich fühle mich ausgewogen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID746']=0.206
   
                thashtags=re.findall(unicode("ich fühle mich ausgezeichnet", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID748']=0.3146
   
                thashtags=re.findall(unicode("ich fühle mich besser", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID789']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich blendend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID798']=0.3096
   
                thashtags=re.findall(unicode("ich bin cool", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID814']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich dufte", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID823']=0.1958
   
                thashtags=re.findall(unicode("ich bin energisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID851']=0.004
   
                thashtags=re.findall(unicode("ich bin euphorisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID883']=0.5505
   
                thashtags=re.findall(unicode("ich fühle mich exzellent", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID891']=0.4198
   
                thashtags=re.findall(unicode("ich fühle mich fabelhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID892']=0.1952
   
                thashtags=re.findall(unicode("ich fühle mich fantastisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID896']=0.3319
   
                thashtags=re.findall(unicode("ich bin freudig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID916']=0.3256
   
                thashtags=re.findall(unicode("ich bin fröhlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID923']=0.2501
   
                thashtags=re.findall(unicode("ich fühle mich fulminant", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID924']=0.004
   
                thashtags=re.findall(unicode("ich bin gelassen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID945']=0.2325
   
                thashtags=re.findall(unicode("ich bin gesund", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID970']=0.1554
   
                thashtags=re.findall(unicode("ich bin glücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID990']=0.115
   
                thashtags=re.findall(unicode("ich fühle mich grandios", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID995']=0.1843
   
                thashtags=re.findall(unicode("ich fühle mich großartig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1000']=0.4606
   
                thashtags=re.findall(unicode("ich fühle mich gut", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1007']=0.3716
   
                thashtags=re.findall(unicode("ich fühle mich göttlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1009']=0.004
   
                thashtags=re.findall(unicode("ich bin harmonisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1016']=0.3489
   
                thashtags=re.findall(unicode("ich bin heiter", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1023']=0.2013
   
                thashtags=re.findall(unicode("ich fühle mich herrlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1027']=0.4821
   
                thashtags=re.findall(unicode("ich fühle mich hervorragend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1029']=0.5891
   
                thashtags=re.findall(unicode("ich bin kraftvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1106']=0.2214
   
                thashtags=re.findall(unicode("ich bin lebendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1116']=0.0947
   
                thashtags=re.findall(unicode("ich fühle mich optimal", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1180']=0.2162
   
                thashtags=re.findall(unicode("ich bin optimistisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1181']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich reizend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1233']=0.0787
   
                thashtags=re.findall(unicode("ich fühle mich riesig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1242']=0.4554
   
                thashtags=re.findall(unicode("ich fühle mich sensationell", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1273']=0.086
   
                thashtags=re.findall(unicode("ich bin sorglos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1287']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich spitze", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1297']=0.2112
   
                thashtags=re.findall(unicode("ich bin stark", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1301']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich super", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1309']=0.5012
   
                thashtags=re.findall(unicode("ich fühle mich toll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1323']=0.5066
   
                thashtags=re.findall(unicode("ich fühle mich traumhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1329']=0.5665
   
                thashtags=re.findall(unicode("ich fühle mich umwerfend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1339']=0.1991
   
                thashtags=re.findall(unicode("ich fühle mich unbeschwert", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1348']=0.3349
   
                thashtags=re.findall(unicode("ich bin vital", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1418']=0.2122
   
                thashtags=re.findall(unicode("ich bin wachsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1428']=0.0891
   
                thashtags=re.findall(unicode("ich fühle mich wunderbar", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1460']=0.7234
   
                thashtags=re.findall(unicode("ich fühle mich wundervoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1463']=0.308
   
                thashtags=re.findall(unicode("ich bin zufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1473']=0.393
   
                thashtags=re.findall(unicode("ich fühle mich überdurchschnittlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1483']=0.09
   
                thashtags=re.findall(unicode("ich bin überglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1484']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich überragend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1489']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich überwältigend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1495']=0.3312
   
                thashtags=re.findall(unicode("ich fühle mich aufgebracht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1499']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich matt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1500']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich mutlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1501']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich müde", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1502']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich schlapp", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1503']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich schwerfällig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1504']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich stupide", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1505']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich scheisse", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1506']=-0.0226
   
                thashtags=re.findall(unicode("ich fühle mich schrecklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1507']=-0.0242
   
                thashtags=re.findall(unicode("ich fühle mich launisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1508']=-0.0409
   
                thashtags=re.findall(unicode("ich fühle mich leblos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1509']=-0.049
   
                thashtags=re.findall(unicode("ich fühle mich einsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1510']=-0.1634
   
                thashtags=re.findall(unicode("ich fühle mich unglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1511']=-0.301
   
                thashtags=re.findall(unicode("ich fühle mich debil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1512']=-0.306
   
                thashtags=re.findall(unicode("ich fühle mich gestreßt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1513']=-0.3128
   
                thashtags=re.findall(unicode("ich fühle mich kränklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1514']=-0.3172
   
                thashtags=re.findall(unicode("ich fühle mich wütend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1515']=-0.3233
   
                thashtags=re.findall(unicode("ich fühle mich labil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1516']=-0.326
   
                thashtags=re.findall(unicode("ich fühle mich machtlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1517']=-0.3351
   
                thashtags=re.findall(unicode("ich fühle mich krank", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1518']=-0.4694
   
                thashtags=re.findall(unicode("ich fühle mich niedergeschlagen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1519']=-0.4708
   
                thashtags=re.findall(unicode("ich fühle mich depressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1520']=-0.4715
   
                thashtags=re.findall(unicode("ich fühle mich ängstlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1521']=-0.4735
   
                thashtags=re.findall(unicode("ich fühle mich angespannt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1522']=-0.4744
   
                thashtags=re.findall(unicode("ich fühle mich zerissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1523']=-0.4776
   
                thashtags=re.findall(unicode("ich fühle mich verletzt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1524']=-0.5202
   
                thashtags=re.findall(unicode("ich fühle mich wertlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1525']=-0.6264
   
                thashtags=re.findall(unicode("ich fühle mich unsicher", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1526']=-0.6268
   
                thashtags=re.findall(unicode("ich fühle mich schwach", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1527']=-0.9206
   
                thashtags=re.findall(unicode("ich fühle mich cool", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1528']=-0.004
   
                thashtags=re.findall(unicode("ich fühle mich euphorisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1529']=-0.5505
   
                thashtags=re.findall(unicode("ich fühle mich fröhlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1530']=-0.2501
   
                thashtags=re.findall(unicode("ich fühle mich gesund", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1531']=-0.1554
   
                thashtags=re.findall(unicode("ich fühle mich glücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1532']=-0.115
   
                thashtags=re.findall(unicode("ich fühle mich heiter", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1533']=-0.2013
   
                thashtags=re.findall(unicode("ich fühle mich kraftvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1534']=-0.2214
   
                thashtags=re.findall(unicode("ich fühle mich lebendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1535']=-0.0947
   
                thashtags=re.findall(unicode("ich fühle mich stark", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1536']=-0.004
   
                thashtags=re.findall(unicode("ich fühle mich vital", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1537']=-0.2122
   
                thashtags=re.findall(unicode("ich fühle mich zufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1538']=-0.393
   
                thashtags=re.findall(unicode("ich fühle mich überglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1539']=-0.004


                #thashtags=re.findall(unicode("und|die", 'utf-8'), result['text'], re.I)
                #if len(thashtags) > 0:
                #    data['KeyStateXXXXXXXXXX']=0.134


                print data['from_user'], data['text'], data['iso_language_code'], data['source'], data['geo'], data['profile_image_url']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break
###################################################################################
# Twitter scraper - designed to be forked and used for more interesting things
###################################################################################

import os, sys
import scraperwiki
import simplejson
import urllib2
import re



# Change QUERY to your search term of choice.
# Examples: 'newsnight', 'from:bbcnewsnight', 'to:bbcnewsnight'
QUERY = [ ('ich bin','ich fühle')]
RESULTS_PER_PAGE = '100'
LANGUAGE = ''
NUM_PAGES = 15

for (q,table) in QUERY:
    for page in range(1, NUM_PAGES+1):
        base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&lang=%s&page=%s&result_type=recent' \
         % (urllib2.quote(q), RESULTS_PER_PAGE, LANGUAGE, page)
        try:
            results_json = simplejson.loads(scraperwiki.scrape(base_url))
            print results_json
            if len(results_json['results'])==0: break
            for result in results_json['results']:
                #print type(result['text'])
                #print "*" , re.findall(unicode("Männer", 'utf-8'), result['text'], re.I)
                data = {}
                data['id'] = result['id']
                data['text'] = result['text']
                data['from_user'] = result['from_user']
                data['from_user_id'] = result['from_user_id']
                #data['to_user'] = result['to_user']
                #data['to_user_id'] = result['to_user_id']
                data['created_at'] = result['created_at']
                data['geo'] = result['geo']
                data['source'] = result['source']
                data['profile_image_url'] = result['profile_image_url']
                data['iso_language_code'] = result['iso_language_code']
                 
                thashtags=re.findall("#([a-z0-9]+)", result['text'], re.I)
                data['hashtags']=' | '.join(thashtags)
                
                tuser=re.findall("@([a-z0-9]+)", result['text'], re.I)
                data['user identified']=' | '.join(tuser)
                
                thashtags=re.findall("RT @([a-z0-9]+)", result['text'], re.I)
                data['retweets']=' | '.join(thashtags)

                thashtags=re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", result['text'], re.I)
                data['links']=' | '.join(thashtags)
                
                #thashtags=re.findall(unicode("und", 'utf-8'), result['text'], re.I)
                #data['KeyStateXXXXXXXXXX']=len(thashtags)
                
                   
                thashtags=re.findall(unicode("ich bin aufgebracht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID16']=-0.0048
   
                thashtags=re.findall(unicode("ich bin aufgeregt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID17']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich elendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID52']=-0.0048
   
                thashtags=re.findall(unicode("ich bin matt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID119']=-0.0048
   
                thashtags=re.findall(unicode("ich bin melancholisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID120']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich mies", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID122']=-0.0048
   
                thashtags=re.findall(unicode("ich bin mutlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID127']=-0.0048
   
                thashtags=re.findall(unicode("ich bin müde", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID128']=-0.0048
   
                thashtags=re.findall(unicode("ich bin panisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID133']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich scheusslich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID154']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schlapp", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID156']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schmerzerfüllt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID159']=-0.0048
   
                thashtags=re.findall(unicode("ich bin schwerfällig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID162']=-0.0048
   
                thashtags=re.findall(unicode("ich bin stupide", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID170']=-0.0048
   
                thashtags=re.findall(unicode("ich bin wahnsinnig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID249']=-0.0048
   
                thashtags=re.findall(unicode("ich bin scheisse", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID272']=-0.0226
   
                thashtags=re.findall(unicode("ich bin genervt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID274']=-0.0237
   
                thashtags=re.findall(unicode("ich bin schrecklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID276']=-0.0242
   
                thashtags=re.findall(unicode("ich fühle mich leer", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID279']=-0.025
   
                thashtags=re.findall(unicode("ich bin beängstigend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID288']=-0.0367
   
                thashtags=re.findall(unicode("ich fühle mich grässlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID300']=-0.0395
   
                thashtags=re.findall(unicode("ich bin launisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID306']=-0.0409
   
                thashtags=re.findall(unicode("ich fühle mich schäbig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID311']=-0.0421
   
                thashtags=re.findall(unicode("ich bin besorgt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID334']=-0.0482
   
                thashtags=re.findall(unicode("ich bin verletzlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID337']=-0.0487
   
                thashtags=re.findall(unicode("ich bin leblos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID338']=-0.049
   
                thashtags=re.findall(unicode("ich fühle mich elend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID346']=-0.0519
   
                thashtags=re.findall(unicode("ich bin unruhig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID353']=-0.0551
   
                thashtags=re.findall(unicode("ich bin traurig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID356']=-0.1266
   
                thashtags=re.findall(unicode("ich bin einsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID362']=-0.1634
   
                thashtags=re.findall(unicode("ich fühle mich scheußlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID387']=-0.1834
   
                thashtags=re.findall(unicode("ich fühle mich grauenhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID392']=-0.184
   
                thashtags=re.findall(unicode("ich bin zornig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID398']=-0.1853
   
                thashtags=re.findall(unicode("ich bin verzweifelt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID409']=-0.1947
   
                thashtags=re.findall(unicode("ich bin kritisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID416']=-0.203
   
                thashtags=re.findall(unicode("ich fühle mich scheiße", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID424']=-0.2945
   
                thashtags=re.findall(unicode("ich fühle mich beschissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID425']=-0.2947
   
                thashtags=re.findall(unicode("ich bin missgelaunt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID426']=-0.297
   
                thashtags=re.findall(unicode("ich bin unglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID429']=-0.301
   
                thashtags=re.findall(unicode("ich fühle mich energielos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID430']=-0.3037
   
                thashtags=re.findall(unicode("ich fühle mich furchtbar", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID432']=-0.3042
   
                thashtags=re.findall(unicode("ich bin debil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID435']=-0.306
   
                thashtags=re.findall(unicode("ich bin gestreßt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID446']=-0.3128
   
                thashtags=re.findall(unicode("ich bin kränklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID465']=-0.3172
   
                thashtags=re.findall(unicode("ich bin wütend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID484']=-0.3233
   
                thashtags=re.findall(unicode("ich fühle mich grauenvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID485']=-0.3238
   
                thashtags=re.findall(unicode("ich bin frustriert", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID488']=-0.3244
   
                thashtags=re.findall(unicode("ich bin labil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID501']=-0.326
   
                thashtags=re.findall(unicode("ich bin grimmig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID516']=-0.3295
   
                thashtags=re.findall(unicode("ich fühle mich kraftlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID533']=-0.3338
   
                thashtags=re.findall(unicode("ich bin machtlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID536']=-0.3351
   
                thashtags=re.findall(unicode("ich bin pessimistisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID540']=-0.3359
   
                thashtags=re.findall(unicode("ich fühle mich fürchterlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID542']=-0.3363
   
                thashtags=re.findall(unicode("ich bin unzufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID543']=-0.3363
   
                thashtags=re.findall(unicode("ich bin aggressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID595']=-0.4484
   
                thashtags=re.findall(unicode("ich fühle mich gräßlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID600']=-0.4529
   
                thashtags=re.findall(unicode("ich bin gekränkt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID601']=-0.453
   
                thashtags=re.findall(unicode("ich fühle mich ungeliebt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID602']=-0.4532
   
                thashtags=re.findall(unicode("ich bin arm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID605']=-0.4546
   
                thashtags=re.findall(unicode("ich fühle mich unangenehm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID622']=-0.4691
   
                thashtags=re.findall(unicode("ich bin krank", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID624']=-0.4694
   
                thashtags=re.findall(unicode("ich bin niedergeschlagen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID627']=-0.4708
   
                thashtags=re.findall(unicode("ich bin depressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID632']=-0.4715
   
                thashtags=re.findall(unicode("ich bin ängstlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID639']=-0.4735
   
                thashtags=re.findall(unicode("ich bin angespannt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID640']=-0.4744
   
                thashtags=re.findall(unicode("ich fühle mich entsetzlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID642']=-0.477
   
                thashtags=re.findall(unicode("ich bin zerrissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID644']=-0.4776
   
                thashtags=re.findall(unicode("ich fühle mich verheerend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID645']=-0.478
   
                thashtags=re.findall(unicode("ich fühle mich erbärmlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID649']=-0.4796
   
                thashtags=re.findall(unicode("ich fühle mich hilflos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID652']=-0.4827
   
                thashtags=re.findall(unicode("ich fühle mich nutzlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID654']=-0.485
   
                thashtags=re.findall(unicode("ich fühle mich katastrophal", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID659']=-0.4917
   
                thashtags=re.findall(unicode("ich bin verletzt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID669']=-0.5202
   
                thashtags=re.findall(unicode("ich fühle mich grausam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID684']=-0.625
   
                thashtags=re.findall(unicode("ich bin wertlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID685']=-0.6264
   
                thashtags=re.findall(unicode("ich bin unsicher", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID686']=-0.6268
   
                thashtags=re.findall(unicode("ich fühle mich sinnlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID688']=-0.6331
   
                thashtags=re.findall(unicode("ich fühle mich schlecht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID702']=-0.7706
   
                thashtags=re.findall(unicode("ich bin schwach", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID706']=-0.9206
   
                thashtags=re.findall(unicode("ich bin aktiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID715']=0.0911
   
                thashtags=re.findall(unicode("ich fühle mich angenehm", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID725']=0.4887
   
                thashtags=re.findall(unicode("ich fühle mich ausgewogen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID746']=0.206
   
                thashtags=re.findall(unicode("ich fühle mich ausgezeichnet", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID748']=0.3146
   
                thashtags=re.findall(unicode("ich fühle mich besser", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID789']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich blendend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID798']=0.3096
   
                thashtags=re.findall(unicode("ich bin cool", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID814']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich dufte", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID823']=0.1958
   
                thashtags=re.findall(unicode("ich bin energisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID851']=0.004
   
                thashtags=re.findall(unicode("ich bin euphorisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID883']=0.5505
   
                thashtags=re.findall(unicode("ich fühle mich exzellent", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID891']=0.4198
   
                thashtags=re.findall(unicode("ich fühle mich fabelhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID892']=0.1952
   
                thashtags=re.findall(unicode("ich fühle mich fantastisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID896']=0.3319
   
                thashtags=re.findall(unicode("ich bin freudig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID916']=0.3256
   
                thashtags=re.findall(unicode("ich bin fröhlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID923']=0.2501
   
                thashtags=re.findall(unicode("ich fühle mich fulminant", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID924']=0.004
   
                thashtags=re.findall(unicode("ich bin gelassen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID945']=0.2325
   
                thashtags=re.findall(unicode("ich bin gesund", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID970']=0.1554
   
                thashtags=re.findall(unicode("ich bin glücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID990']=0.115
   
                thashtags=re.findall(unicode("ich fühle mich grandios", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID995']=0.1843
   
                thashtags=re.findall(unicode("ich fühle mich großartig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1000']=0.4606
   
                thashtags=re.findall(unicode("ich fühle mich gut", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1007']=0.3716
   
                thashtags=re.findall(unicode("ich fühle mich göttlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1009']=0.004
   
                thashtags=re.findall(unicode("ich bin harmonisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1016']=0.3489
   
                thashtags=re.findall(unicode("ich bin heiter", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1023']=0.2013
   
                thashtags=re.findall(unicode("ich fühle mich herrlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1027']=0.4821
   
                thashtags=re.findall(unicode("ich fühle mich hervorragend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1029']=0.5891
   
                thashtags=re.findall(unicode("ich bin kraftvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1106']=0.2214
   
                thashtags=re.findall(unicode("ich bin lebendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1116']=0.0947
   
                thashtags=re.findall(unicode("ich fühle mich optimal", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1180']=0.2162
   
                thashtags=re.findall(unicode("ich bin optimistisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1181']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich reizend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1233']=0.0787
   
                thashtags=re.findall(unicode("ich fühle mich riesig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1242']=0.4554
   
                thashtags=re.findall(unicode("ich fühle mich sensationell", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1273']=0.086
   
                thashtags=re.findall(unicode("ich bin sorglos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1287']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich spitze", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1297']=0.2112
   
                thashtags=re.findall(unicode("ich bin stark", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1301']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich super", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1309']=0.5012
   
                thashtags=re.findall(unicode("ich fühle mich toll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1323']=0.5066
   
                thashtags=re.findall(unicode("ich fühle mich traumhaft", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1329']=0.5665
   
                thashtags=re.findall(unicode("ich fühle mich umwerfend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1339']=0.1991
   
                thashtags=re.findall(unicode("ich fühle mich unbeschwert", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1348']=0.3349
   
                thashtags=re.findall(unicode("ich bin vital", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1418']=0.2122
   
                thashtags=re.findall(unicode("ich bin wachsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1428']=0.0891
   
                thashtags=re.findall(unicode("ich fühle mich wunderbar", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1460']=0.7234
   
                thashtags=re.findall(unicode("ich fühle mich wundervoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1463']=0.308
   
                thashtags=re.findall(unicode("ich bin zufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1473']=0.393
   
                thashtags=re.findall(unicode("ich fühle mich überdurchschnittlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1483']=0.09
   
                thashtags=re.findall(unicode("ich bin überglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1484']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich überragend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1489']=0.004
   
                thashtags=re.findall(unicode("ich fühle mich überwältigend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1495']=0.3312
   
                thashtags=re.findall(unicode("ich fühle mich aufgebracht", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1499']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich matt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1500']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich mutlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1501']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich müde", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1502']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich schlapp", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1503']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich schwerfällig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1504']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich stupide", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1505']=-0.0048
   
                thashtags=re.findall(unicode("ich fühle mich scheisse", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1506']=-0.0226
   
                thashtags=re.findall(unicode("ich fühle mich schrecklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1507']=-0.0242
   
                thashtags=re.findall(unicode("ich fühle mich launisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1508']=-0.0409
   
                thashtags=re.findall(unicode("ich fühle mich leblos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1509']=-0.049
   
                thashtags=re.findall(unicode("ich fühle mich einsam", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1510']=-0.1634
   
                thashtags=re.findall(unicode("ich fühle mich unglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1511']=-0.301
   
                thashtags=re.findall(unicode("ich fühle mich debil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1512']=-0.306
   
                thashtags=re.findall(unicode("ich fühle mich gestreßt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1513']=-0.3128
   
                thashtags=re.findall(unicode("ich fühle mich kränklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1514']=-0.3172
   
                thashtags=re.findall(unicode("ich fühle mich wütend", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1515']=-0.3233
   
                thashtags=re.findall(unicode("ich fühle mich labil", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1516']=-0.326
   
                thashtags=re.findall(unicode("ich fühle mich machtlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1517']=-0.3351
   
                thashtags=re.findall(unicode("ich fühle mich krank", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1518']=-0.4694
   
                thashtags=re.findall(unicode("ich fühle mich niedergeschlagen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1519']=-0.4708
   
                thashtags=re.findall(unicode("ich fühle mich depressiv", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1520']=-0.4715
   
                thashtags=re.findall(unicode("ich fühle mich ängstlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1521']=-0.4735
   
                thashtags=re.findall(unicode("ich fühle mich angespannt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1522']=-0.4744
   
                thashtags=re.findall(unicode("ich fühle mich zerissen", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1523']=-0.4776
   
                thashtags=re.findall(unicode("ich fühle mich verletzt", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1524']=-0.5202
   
                thashtags=re.findall(unicode("ich fühle mich wertlos", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1525']=-0.6264
   
                thashtags=re.findall(unicode("ich fühle mich unsicher", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1526']=-0.6268
   
                thashtags=re.findall(unicode("ich fühle mich schwach", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1527']=-0.9206
   
                thashtags=re.findall(unicode("ich fühle mich cool", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1528']=-0.004
   
                thashtags=re.findall(unicode("ich fühle mich euphorisch", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1529']=-0.5505
   
                thashtags=re.findall(unicode("ich fühle mich fröhlich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1530']=-0.2501
   
                thashtags=re.findall(unicode("ich fühle mich gesund", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1531']=-0.1554
   
                thashtags=re.findall(unicode("ich fühle mich glücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1532']=-0.115
   
                thashtags=re.findall(unicode("ich fühle mich heiter", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1533']=-0.2013
   
                thashtags=re.findall(unicode("ich fühle mich kraftvoll", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1534']=-0.2214
   
                thashtags=re.findall(unicode("ich fühle mich lebendig", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1535']=-0.0947
   
                thashtags=re.findall(unicode("ich fühle mich stark", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1536']=-0.004
   
                thashtags=re.findall(unicode("ich fühle mich vital", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1537']=-0.2122
   
                thashtags=re.findall(unicode("ich fühle mich zufrieden", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1538']=-0.393
   
                thashtags=re.findall(unicode("ich fühle mich überglücklich", 'utf-8'), result['text'], re.I)
                if len(thashtags) > 0:
                    data['MoodID1539']=-0.004


                #thashtags=re.findall(unicode("und|die", 'utf-8'), result['text'], re.I)
                #if len(thashtags) > 0:
                #    data['KeyStateXXXXXXXXXX']=0.134


                print data['from_user'], data['text'], data['iso_language_code'], data['source'], data['geo'], data['profile_image_url']
                scraperwiki.sqlite.save(table_name=table,unique_keys=["id"], data=data)
        except:
            print 'Oh dear, failed to scrape %s' % base_url
            break

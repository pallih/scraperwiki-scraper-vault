import scraperwiki
import simplejson
import re
     
# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
options = '&rpp=100&page='
     
def scrape_query(q):
    page = 1
    while 1:
        try:
            url = base_url + q + options + str(page)
            html = scraperwiki.scrape(url)
            #print html
            soup = simplejson.loads(html)
            for result in soup['results']:
                #print result['text']
                count = 0
                for m in re.finditer(r"((ext)?circo(\d+))", result['text'], re.I):
                    data = {}
                    data['id'] = result['id'] + count
                    data['text'] = result['text']
                    if m.group(1) is not None:
                        data['circo_hashtag'] = m.group(1).lower()
                        if m.group(2) is not None:
                            data['departement'] = "Français de l'Étranger"
                            data['circonscription'] = m.group(3)
                        else:
                            n = re.search(r"(\d\d)(\d\d)", m.group(3))
                            if n.group(2) is not None:
                                data['departement'] = n.group(1)
                                data['circonscription'] = n.group(2)              
                    data['from_user'] = result['from_user']
                    data['created_at'] = result['created_at']
                    data['twitter_url'] = 'https://twitter.com/'+data['from_user']+'/statuses/'+`result['id']`
                    data['photo_user'] = 'http://twitteravatar.appspot.com/users/avatar/'+data['from_user']
                    if result['geo'] is not None:
                        data['geoloc'] = result['geo']['coordinates']
                    # save records to the datastore
                    scraperwiki.sqlite.save(["id"], data)
                    count = count + 1
            page = page + 1
        except:
            print str(page) + ' pages scraped'
            break# Blank Python
scrape_query('%23legislatives+OR+%23legislatives2012')
scrape_query('Circo0101+OR+Circo0102+OR+Circo0103+OR+Circo0104+OR+Circo0105+OR+Circo0201+OR+Circo0202+OR+Circo0203+OR+Circo0204+OR+Circo0205+OR+Circo0301')
scrape_query('Circo0302+OR+Circo0303+OR+Circo0401+OR+Circo0402+OR+Circo0501+OR+Circo0502+OR+Circo0601+OR+Circo0602+OR+Circo0603+OR+Circo0604+OR+Circo0605')
scrape_query('Circo0606+OR+Circo0607+OR+Circo0608+OR+Circo0609+OR+Circo0701+OR+Circo0702+OR+Circo0703+OR+Circo0801+OR+Circo0802+OR+Circo0803+OR+Circo0901')
scrape_query('Circo0902+OR+Circo1001+OR+Circo1002+OR+Circo1003+OR+Circo1101+OR+Circo1102+OR+Circo1103+OR+Circo1201+OR+Circo1202+OR+Circo1203+OR+Circo1301')
scrape_query('Circo1302+OR+Circo1303+OR+Circo1304+OR+Circo1305+OR+Circo1306+OR+Circo1307+OR+Circo1308+OR+Circo1309+OR+Circo1310+OR+Circo1311+OR+Circo1312')
scrape_query('Circo1313+OR+Circo1314+OR+Circo1315+OR+Circo1316+OR+Circo1401+OR+Circo1402+OR+Circo1403+OR+Circo1404+OR+Circo1405+OR+Circo1406+OR+Circo1501')
scrape_query('Circo1502+OR+Circo1601+OR+Circo1602+OR+Circo1603+OR+Circo1701+OR+Circo1702+OR+Circo1703+OR+Circo1704+OR+Circo1705+OR+Circo1801+OR+Circo1802')
scrape_query('Circo1803+OR+Circo1901+OR+Circo1902+OR+Circo2A01+OR+Circo2A02+OR+Circo2B01+OR+Circo2B02+OR+Circo2101+OR+Circo2102+OR+Circo2103+OR+Circo2104')
scrape_query('Circo2105+OR+Circo2201+OR+Circo2202+OR+Circo2203+OR+Circo2204+OR+Circo2205+OR+Circo2301+OR+Circo2401+OR+Circo2402+OR+Circo2403+OR+Circo2404')
scrape_query('Circo2501+OR+Circo2502+OR+Circo2503+OR+Circo2504+OR+Circo2505+OR+Circo2601+OR+Circo2602+OR+Circo2603+OR+Circo2604+OR+Circo2701+OR+Circo2702')
scrape_query('Circo2703+OR+Circo2704+OR+Circo2705+OR+Circo2801+OR+Circo2802+OR+Circo2803+OR+Circo2804+OR+Circo2901+OR+Circo2902+OR+Circo2903+OR+Circo2904')
scrape_query('Circo2905+OR+Circo2906+OR+Circo2907+OR+Circo2908+OR+Circo3001+OR+Circo3002+OR+Circo3003+OR+Circo3004+OR+Circo3005+OR+Circo3006+OR+Circo3101')
scrape_query('Circo3102+OR+Circo3103+OR+Circo3104+OR+Circo3105+OR+Circo3106+OR+Circo3107+OR+Circo3108+OR+Circo3109+OR+Circo3110+OR+Circo3201+OR+Circo3202')
scrape_query('Circo3301+OR+Circo3302+OR+Circo3303+OR+Circo3304+OR+Circo3305+OR+Circo3306+OR+Circo3307+OR+Circo3308+OR+Circo3309+OR+Circo3310+OR+Circo3311')
scrape_query('Circo3312+OR+Circo3401+OR+Circo3402+OR+Circo3403+OR+Circo3404+OR+Circo3405+OR+Circo3406+OR+Circo3407+OR+Circo3408+OR+Circo3409+OR+Circo3501')
scrape_query('Circo3502+OR+Circo3503+OR+Circo3504+OR+Circo3505+OR+Circo3506+OR+Circo3507+OR+Circo3508+OR+Circo3601+OR+Circo3602+OR+Circo3701+OR+Circo3702')
scrape_query('Circo3703+OR+Circo3704+OR+Circo3705+OR+Circo3801+OR+Circo3802+OR+Circo3803+OR+Circo3804+OR+Circo3805+OR+Circo3806+OR+Circo3807+OR+Circo3808')
scrape_query('Circo3809+OR+Circo3810+OR+Circo3901+OR+Circo3902+OR+Circo3903+OR+Circo4001+OR+Circo4002+OR+Circo4003+OR+Circo4101+OR+Circo4102+OR+Circo4103')
scrape_query('Circo4201+OR+Circo4202+OR+Circo4203+OR+Circo4204+OR+Circo4205+OR+Circo4206+OR+Circo4301+OR+Circo4302+OR+Circo4401+OR+Circo4402+OR+Circo4403')
scrape_query('Circo4404+OR+Circo4405+OR+Circo4406+OR+Circo4407+OR+Circo4408+OR+Circo4409+OR+Circo4410+OR+Circo4501+OR+Circo4502+OR+Circo4503+OR+Circo4504')
scrape_query('Circo4505+OR+Circo4506+OR+Circo4601+OR+Circo4602+OR+Circo4701+OR+Circo4702+OR+Circo4703+OR+Circo4801+OR+Circo4901+OR+Circo4902+OR+Circo4903')
scrape_query('Circo4904+OR+Circo4905+OR+Circo4906+OR+Circo4907+OR+Circo5001+OR+Circo5002+OR+Circo5003+OR+Circo5004+OR+Circo5101+OR+Circo5102+OR+Circo5103')
scrape_query('Circo5104+OR+Circo5105+OR+Circo5201+OR+Circo5202+OR+Circo5301+OR+Circo5302+OR+Circo5303+OR+Circo5401+OR+Circo5402+OR+Circo5403+OR+Circo5404')
scrape_query('Circo5405+OR+Circo5406+OR+Circo5501+OR+Circo5502+OR+Circo5601+OR+Circo5602+OR+Circo5603+OR+Circo5604+OR+Circo5605+OR+Circo5606+OR+Circo5701')
scrape_query('Circo5702+OR+Circo5703+OR+Circo5704+OR+Circo5705+OR+Circo5706+OR+Circo5707+OR+Circo5708+OR+Circo5709+OR+Circo5801+OR+Circo5802+OR+Circo5901')
scrape_query('Circo5902+OR+Circo5903+OR+Circo5904+OR+Circo5905+OR+Circo5906+OR+Circo5907+OR+Circo5908+OR+Circo5909+OR+Circo5910+OR+Circo5911+OR+Circo5912')
scrape_query('Circo5913+OR+Circo5914+OR+Circo5915+OR+Circo5916+OR+Circo5917+OR+Circo5918+OR+Circo5919+OR+Circo5920+OR+Circo5921+OR+Circo6001+OR+Circo6002')
scrape_query('Circo6003+OR+Circo6004+OR+Circo6005+OR+Circo6006+OR+Circo6007+OR+Circo6101+OR+Circo6102+OR+Circo6103+OR+Circo6201+OR+Circo6202+OR+Circo6203')
scrape_query('Circo6204+OR+Circo6205+OR+Circo6206+OR+Circo6207+OR+Circo6208+OR+Circo6209+OR+Circo6210+OR+Circo6211+OR+Circo6212+OR+Circo6301+OR+Circo6302')
scrape_query('Circo6303+OR+Circo6304+OR+Circo6305+OR+Circo6401+OR+Circo6402+OR+Circo6403+OR+Circo6404+OR+Circo6405+OR+Circo6406+OR+Circo6501+OR+Circo6502')
scrape_query('Circo6601+OR+Circo6602+OR+Circo6603+OR+Circo6604+OR+Circo6701+OR+Circo6702+OR+Circo6703+OR+Circo6704+OR+Circo6705+OR+Circo6706+OR+Circo6707')
scrape_query('Circo6708+OR+Circo6709+OR+Circo6801+OR+Circo6802+OR+Circo6803+OR+Circo6804+OR+Circo6805+OR+Circo6806+OR+Circo6901+OR+Circo6902+OR+Circo6903')
scrape_query('Circo6904+OR+Circo6905+OR+Circo6906+OR+Circo6907+OR+Circo6908+OR+Circo6909+OR+Circo6910+OR+Circo6911+OR+Circo6912+OR+Circo6913+OR+Circo6914')
scrape_query('Circo7001+OR+Circo7002+OR+Circo7101+OR+Circo7102+OR+Circo7103+OR+Circo7104+OR+Circo7105+OR+Circo7201+OR+Circo7202+OR+Circo7203+OR+Circo7204')
scrape_query('Circo7205+OR+Circo7301+OR+Circo7302+OR+Circo7303+OR+Circo7304+OR+Circo7401+OR+Circo7402+OR+Circo7403+OR+Circo7404+OR+Circo7405+OR+Circo7406')
scrape_query('Circo7501+OR+Circo7502+OR+Circo7503+OR+Circo7504+OR+Circo7505+OR+Circo7506+OR+Circo7507+OR+Circo7508+OR+Circo7509+OR+Circo7510+OR+Circo7511')
scrape_query('Circo7512+OR+Circo7513+OR+Circo7514+OR+Circo7515+OR+Circo7516+OR+Circo7517+OR+Circo7518+OR+Circo7601+OR+Circo7602+OR+Circo7603+OR+Circo7604')
scrape_query('Circo7605+OR+Circo7606+OR+Circo7607+OR+Circo7608+OR+Circo7609+OR+Circo7610+OR+Circo7701+OR+Circo7702+OR+Circo7703+OR+Circo7704+OR+Circo7705')
scrape_query('Circo7706+OR+Circo7707+OR+Circo7708+OR+Circo7709+OR+Circo7710+OR+Circo7711+OR+Circo7801+OR+Circo7802+OR+Circo7803+OR+Circo7804+OR+Circo7805')
scrape_query('Circo7806+OR+Circo7807+OR+Circo7808+OR+Circo7809+OR+Circo7810+OR+Circo7811+OR+Circo7812+OR+Circo7901+OR+Circo7902+OR+Circo7903+OR+Circo8001')
scrape_query('Circo8002+OR+Circo8003+OR+Circo8004+OR+Circo8005+OR+Circo8101+OR+Circo8102+OR+Circo8103+OR+Circo8201+OR+Circo8202+OR+Circo8301+OR+Circo8302')
scrape_query('Circo8303+OR+Circo8304+OR+Circo8305+OR+Circo8306+OR+Circo8307+OR+Circo8308+OR+Circo8401+OR+Circo8402+OR+Circo8403+OR+Circo8404+OR+Circo8405')
scrape_query('Circo8501+OR+Circo8502+OR+Circo8503+OR+Circo8504+OR+Circo8505+OR+Circo8601+OR+Circo8602+OR+Circo8603+OR+Circo8604+OR+Circo8701+OR+Circo8702')
scrape_query('Circo8703+OR+Circo8801+OR+Circo8802+OR+Circo8803+OR+Circo8804+OR+Circo8901+OR+Circo8902+OR+Circo8903+OR+Circo9001+OR+Circo9002+OR+Circo9101')
scrape_query('Circo9102+OR+Circo9103+OR+Circo9104+OR+Circo9105+OR+Circo9106+OR+Circo9107+OR+Circo9108+OR+Circo9109+OR+Circo9110+OR+Circo9201+OR+Circo9202')
scrape_query('Circo9203+OR+Circo9204+OR+Circo9205+OR+Circo9206+OR+Circo9207+OR+Circo9208+OR+Circo9209+OR+Circo9210+OR+Circo9211+OR+Circo9212+OR+Circo9213')
scrape_query('Circo9301+OR+Circo9302+OR+Circo9303+OR+Circo9304+OR+Circo9305+OR+Circo9306+OR+Circo9307+OR+Circo9308+OR+Circo9309+OR+Circo9310+OR+Circo9311')
scrape_query('Circo9312+OR+Circo9401+OR+Circo9402+OR+Circo9403+OR+Circo9404+OR+Circo9405+OR+Circo9406+OR+Circo9407+OR+Circo9408+OR+Circo9409+OR+Circo9410')
scrape_query('Circo9411+OR+Circo9501+OR+Circo9502+OR+Circo9503+OR+Circo9504+OR+Circo9505+OR+Circo9506+OR+Circo9507+OR+Circo9508+OR+Circo9509+OR+Circo9510')
scrape_query('Circo97101+OR+Circo97102+OR+Circo97103+OR+Circo97104+OR+Circo97201+OR+Circo97202+OR+Circo97203+OR+Circo97204+OR+Circo97301+OR+Circo97302')
scrape_query('Circo97401+OR+Circo97402+OR+Circo97403+OR+Circo97404+OR+Circo97405+OR+Circo97406+OR+Circo97407+OR+Circo97501+OR+Circo97601+OR+Circo97602')
scrape_query('Circo97701+OR+Circo98601+OR+Circo98701+OR+Circo98702+OR+Circo98703+OR+Circo98801+OR+Circo98802+OR+EXTcirco01+OR+EXTcirco02+OR+EXTcirco03')
scrape_query('EXTcirco04+OR+EXTcirco05+OR+EXTcirco06+OR+EXTcirco07+OR+EXTcirco08+OR+EXTcirco09+OR+EXTcirco10+OR+EXTcirco11')
import scraperwiki
import simplejson
import re
     
# retrieve a page
base_url = 'http://search.twitter.com/search.json?q='
options = '&rpp=100&page='
     
def scrape_query(q):
    page = 1
    while 1:
        try:
            url = base_url + q + options + str(page)
            html = scraperwiki.scrape(url)
            #print html
            soup = simplejson.loads(html)
            for result in soup['results']:
                #print result['text']
                count = 0
                for m in re.finditer(r"((ext)?circo(\d+))", result['text'], re.I):
                    data = {}
                    data['id'] = result['id'] + count
                    data['text'] = result['text']
                    if m.group(1) is not None:
                        data['circo_hashtag'] = m.group(1).lower()
                        if m.group(2) is not None:
                            data['departement'] = "Français de l'Étranger"
                            data['circonscription'] = m.group(3)
                        else:
                            n = re.search(r"(\d\d)(\d\d)", m.group(3))
                            if n.group(2) is not None:
                                data['departement'] = n.group(1)
                                data['circonscription'] = n.group(2)              
                    data['from_user'] = result['from_user']
                    data['created_at'] = result['created_at']
                    data['twitter_url'] = 'https://twitter.com/'+data['from_user']+'/statuses/'+`result['id']`
                    data['photo_user'] = 'http://twitteravatar.appspot.com/users/avatar/'+data['from_user']
                    if result['geo'] is not None:
                        data['geoloc'] = result['geo']['coordinates']
                    # save records to the datastore
                    scraperwiki.sqlite.save(["id"], data)
                    count = count + 1
            page = page + 1
        except:
            print str(page) + ' pages scraped'
            break# Blank Python
scrape_query('%23legislatives+OR+%23legislatives2012')
scrape_query('Circo0101+OR+Circo0102+OR+Circo0103+OR+Circo0104+OR+Circo0105+OR+Circo0201+OR+Circo0202+OR+Circo0203+OR+Circo0204+OR+Circo0205+OR+Circo0301')
scrape_query('Circo0302+OR+Circo0303+OR+Circo0401+OR+Circo0402+OR+Circo0501+OR+Circo0502+OR+Circo0601+OR+Circo0602+OR+Circo0603+OR+Circo0604+OR+Circo0605')
scrape_query('Circo0606+OR+Circo0607+OR+Circo0608+OR+Circo0609+OR+Circo0701+OR+Circo0702+OR+Circo0703+OR+Circo0801+OR+Circo0802+OR+Circo0803+OR+Circo0901')
scrape_query('Circo0902+OR+Circo1001+OR+Circo1002+OR+Circo1003+OR+Circo1101+OR+Circo1102+OR+Circo1103+OR+Circo1201+OR+Circo1202+OR+Circo1203+OR+Circo1301')
scrape_query('Circo1302+OR+Circo1303+OR+Circo1304+OR+Circo1305+OR+Circo1306+OR+Circo1307+OR+Circo1308+OR+Circo1309+OR+Circo1310+OR+Circo1311+OR+Circo1312')
scrape_query('Circo1313+OR+Circo1314+OR+Circo1315+OR+Circo1316+OR+Circo1401+OR+Circo1402+OR+Circo1403+OR+Circo1404+OR+Circo1405+OR+Circo1406+OR+Circo1501')
scrape_query('Circo1502+OR+Circo1601+OR+Circo1602+OR+Circo1603+OR+Circo1701+OR+Circo1702+OR+Circo1703+OR+Circo1704+OR+Circo1705+OR+Circo1801+OR+Circo1802')
scrape_query('Circo1803+OR+Circo1901+OR+Circo1902+OR+Circo2A01+OR+Circo2A02+OR+Circo2B01+OR+Circo2B02+OR+Circo2101+OR+Circo2102+OR+Circo2103+OR+Circo2104')
scrape_query('Circo2105+OR+Circo2201+OR+Circo2202+OR+Circo2203+OR+Circo2204+OR+Circo2205+OR+Circo2301+OR+Circo2401+OR+Circo2402+OR+Circo2403+OR+Circo2404')
scrape_query('Circo2501+OR+Circo2502+OR+Circo2503+OR+Circo2504+OR+Circo2505+OR+Circo2601+OR+Circo2602+OR+Circo2603+OR+Circo2604+OR+Circo2701+OR+Circo2702')
scrape_query('Circo2703+OR+Circo2704+OR+Circo2705+OR+Circo2801+OR+Circo2802+OR+Circo2803+OR+Circo2804+OR+Circo2901+OR+Circo2902+OR+Circo2903+OR+Circo2904')
scrape_query('Circo2905+OR+Circo2906+OR+Circo2907+OR+Circo2908+OR+Circo3001+OR+Circo3002+OR+Circo3003+OR+Circo3004+OR+Circo3005+OR+Circo3006+OR+Circo3101')
scrape_query('Circo3102+OR+Circo3103+OR+Circo3104+OR+Circo3105+OR+Circo3106+OR+Circo3107+OR+Circo3108+OR+Circo3109+OR+Circo3110+OR+Circo3201+OR+Circo3202')
scrape_query('Circo3301+OR+Circo3302+OR+Circo3303+OR+Circo3304+OR+Circo3305+OR+Circo3306+OR+Circo3307+OR+Circo3308+OR+Circo3309+OR+Circo3310+OR+Circo3311')
scrape_query('Circo3312+OR+Circo3401+OR+Circo3402+OR+Circo3403+OR+Circo3404+OR+Circo3405+OR+Circo3406+OR+Circo3407+OR+Circo3408+OR+Circo3409+OR+Circo3501')
scrape_query('Circo3502+OR+Circo3503+OR+Circo3504+OR+Circo3505+OR+Circo3506+OR+Circo3507+OR+Circo3508+OR+Circo3601+OR+Circo3602+OR+Circo3701+OR+Circo3702')
scrape_query('Circo3703+OR+Circo3704+OR+Circo3705+OR+Circo3801+OR+Circo3802+OR+Circo3803+OR+Circo3804+OR+Circo3805+OR+Circo3806+OR+Circo3807+OR+Circo3808')
scrape_query('Circo3809+OR+Circo3810+OR+Circo3901+OR+Circo3902+OR+Circo3903+OR+Circo4001+OR+Circo4002+OR+Circo4003+OR+Circo4101+OR+Circo4102+OR+Circo4103')
scrape_query('Circo4201+OR+Circo4202+OR+Circo4203+OR+Circo4204+OR+Circo4205+OR+Circo4206+OR+Circo4301+OR+Circo4302+OR+Circo4401+OR+Circo4402+OR+Circo4403')
scrape_query('Circo4404+OR+Circo4405+OR+Circo4406+OR+Circo4407+OR+Circo4408+OR+Circo4409+OR+Circo4410+OR+Circo4501+OR+Circo4502+OR+Circo4503+OR+Circo4504')
scrape_query('Circo4505+OR+Circo4506+OR+Circo4601+OR+Circo4602+OR+Circo4701+OR+Circo4702+OR+Circo4703+OR+Circo4801+OR+Circo4901+OR+Circo4902+OR+Circo4903')
scrape_query('Circo4904+OR+Circo4905+OR+Circo4906+OR+Circo4907+OR+Circo5001+OR+Circo5002+OR+Circo5003+OR+Circo5004+OR+Circo5101+OR+Circo5102+OR+Circo5103')
scrape_query('Circo5104+OR+Circo5105+OR+Circo5201+OR+Circo5202+OR+Circo5301+OR+Circo5302+OR+Circo5303+OR+Circo5401+OR+Circo5402+OR+Circo5403+OR+Circo5404')
scrape_query('Circo5405+OR+Circo5406+OR+Circo5501+OR+Circo5502+OR+Circo5601+OR+Circo5602+OR+Circo5603+OR+Circo5604+OR+Circo5605+OR+Circo5606+OR+Circo5701')
scrape_query('Circo5702+OR+Circo5703+OR+Circo5704+OR+Circo5705+OR+Circo5706+OR+Circo5707+OR+Circo5708+OR+Circo5709+OR+Circo5801+OR+Circo5802+OR+Circo5901')
scrape_query('Circo5902+OR+Circo5903+OR+Circo5904+OR+Circo5905+OR+Circo5906+OR+Circo5907+OR+Circo5908+OR+Circo5909+OR+Circo5910+OR+Circo5911+OR+Circo5912')
scrape_query('Circo5913+OR+Circo5914+OR+Circo5915+OR+Circo5916+OR+Circo5917+OR+Circo5918+OR+Circo5919+OR+Circo5920+OR+Circo5921+OR+Circo6001+OR+Circo6002')
scrape_query('Circo6003+OR+Circo6004+OR+Circo6005+OR+Circo6006+OR+Circo6007+OR+Circo6101+OR+Circo6102+OR+Circo6103+OR+Circo6201+OR+Circo6202+OR+Circo6203')
scrape_query('Circo6204+OR+Circo6205+OR+Circo6206+OR+Circo6207+OR+Circo6208+OR+Circo6209+OR+Circo6210+OR+Circo6211+OR+Circo6212+OR+Circo6301+OR+Circo6302')
scrape_query('Circo6303+OR+Circo6304+OR+Circo6305+OR+Circo6401+OR+Circo6402+OR+Circo6403+OR+Circo6404+OR+Circo6405+OR+Circo6406+OR+Circo6501+OR+Circo6502')
scrape_query('Circo6601+OR+Circo6602+OR+Circo6603+OR+Circo6604+OR+Circo6701+OR+Circo6702+OR+Circo6703+OR+Circo6704+OR+Circo6705+OR+Circo6706+OR+Circo6707')
scrape_query('Circo6708+OR+Circo6709+OR+Circo6801+OR+Circo6802+OR+Circo6803+OR+Circo6804+OR+Circo6805+OR+Circo6806+OR+Circo6901+OR+Circo6902+OR+Circo6903')
scrape_query('Circo6904+OR+Circo6905+OR+Circo6906+OR+Circo6907+OR+Circo6908+OR+Circo6909+OR+Circo6910+OR+Circo6911+OR+Circo6912+OR+Circo6913+OR+Circo6914')
scrape_query('Circo7001+OR+Circo7002+OR+Circo7101+OR+Circo7102+OR+Circo7103+OR+Circo7104+OR+Circo7105+OR+Circo7201+OR+Circo7202+OR+Circo7203+OR+Circo7204')
scrape_query('Circo7205+OR+Circo7301+OR+Circo7302+OR+Circo7303+OR+Circo7304+OR+Circo7401+OR+Circo7402+OR+Circo7403+OR+Circo7404+OR+Circo7405+OR+Circo7406')
scrape_query('Circo7501+OR+Circo7502+OR+Circo7503+OR+Circo7504+OR+Circo7505+OR+Circo7506+OR+Circo7507+OR+Circo7508+OR+Circo7509+OR+Circo7510+OR+Circo7511')
scrape_query('Circo7512+OR+Circo7513+OR+Circo7514+OR+Circo7515+OR+Circo7516+OR+Circo7517+OR+Circo7518+OR+Circo7601+OR+Circo7602+OR+Circo7603+OR+Circo7604')
scrape_query('Circo7605+OR+Circo7606+OR+Circo7607+OR+Circo7608+OR+Circo7609+OR+Circo7610+OR+Circo7701+OR+Circo7702+OR+Circo7703+OR+Circo7704+OR+Circo7705')
scrape_query('Circo7706+OR+Circo7707+OR+Circo7708+OR+Circo7709+OR+Circo7710+OR+Circo7711+OR+Circo7801+OR+Circo7802+OR+Circo7803+OR+Circo7804+OR+Circo7805')
scrape_query('Circo7806+OR+Circo7807+OR+Circo7808+OR+Circo7809+OR+Circo7810+OR+Circo7811+OR+Circo7812+OR+Circo7901+OR+Circo7902+OR+Circo7903+OR+Circo8001')
scrape_query('Circo8002+OR+Circo8003+OR+Circo8004+OR+Circo8005+OR+Circo8101+OR+Circo8102+OR+Circo8103+OR+Circo8201+OR+Circo8202+OR+Circo8301+OR+Circo8302')
scrape_query('Circo8303+OR+Circo8304+OR+Circo8305+OR+Circo8306+OR+Circo8307+OR+Circo8308+OR+Circo8401+OR+Circo8402+OR+Circo8403+OR+Circo8404+OR+Circo8405')
scrape_query('Circo8501+OR+Circo8502+OR+Circo8503+OR+Circo8504+OR+Circo8505+OR+Circo8601+OR+Circo8602+OR+Circo8603+OR+Circo8604+OR+Circo8701+OR+Circo8702')
scrape_query('Circo8703+OR+Circo8801+OR+Circo8802+OR+Circo8803+OR+Circo8804+OR+Circo8901+OR+Circo8902+OR+Circo8903+OR+Circo9001+OR+Circo9002+OR+Circo9101')
scrape_query('Circo9102+OR+Circo9103+OR+Circo9104+OR+Circo9105+OR+Circo9106+OR+Circo9107+OR+Circo9108+OR+Circo9109+OR+Circo9110+OR+Circo9201+OR+Circo9202')
scrape_query('Circo9203+OR+Circo9204+OR+Circo9205+OR+Circo9206+OR+Circo9207+OR+Circo9208+OR+Circo9209+OR+Circo9210+OR+Circo9211+OR+Circo9212+OR+Circo9213')
scrape_query('Circo9301+OR+Circo9302+OR+Circo9303+OR+Circo9304+OR+Circo9305+OR+Circo9306+OR+Circo9307+OR+Circo9308+OR+Circo9309+OR+Circo9310+OR+Circo9311')
scrape_query('Circo9312+OR+Circo9401+OR+Circo9402+OR+Circo9403+OR+Circo9404+OR+Circo9405+OR+Circo9406+OR+Circo9407+OR+Circo9408+OR+Circo9409+OR+Circo9410')
scrape_query('Circo9411+OR+Circo9501+OR+Circo9502+OR+Circo9503+OR+Circo9504+OR+Circo9505+OR+Circo9506+OR+Circo9507+OR+Circo9508+OR+Circo9509+OR+Circo9510')
scrape_query('Circo97101+OR+Circo97102+OR+Circo97103+OR+Circo97104+OR+Circo97201+OR+Circo97202+OR+Circo97203+OR+Circo97204+OR+Circo97301+OR+Circo97302')
scrape_query('Circo97401+OR+Circo97402+OR+Circo97403+OR+Circo97404+OR+Circo97405+OR+Circo97406+OR+Circo97407+OR+Circo97501+OR+Circo97601+OR+Circo97602')
scrape_query('Circo97701+OR+Circo98601+OR+Circo98701+OR+Circo98702+OR+Circo98703+OR+Circo98801+OR+Circo98802+OR+EXTcirco01+OR+EXTcirco02+OR+EXTcirco03')
scrape_query('EXTcirco04+OR+EXTcirco05+OR+EXTcirco06+OR+EXTcirco07+OR+EXTcirco08+OR+EXTcirco09+OR+EXTcirco10+OR+EXTcirco11')

import urllib
try: import json
except: import simplejson as json

import scraperwiki
from dateutil.parser import *
from datetime import *
import commands
import re


# json container From comune di venezia API
url = 'http://portale.comune.venezia.it/sites/all/modules/yui_venis/determine.php?tipo=JSON&giorni=10'

delibereJson = urllib.urlopen(url).read()
print delibereJson 

now = parse(commands.getoutput("date"))
today = now.date()
NOW = datetime.now()

delibereObj =  json.loads(delibereJson) 
for key, value in delibereObj.iteritems():
    items = value
    for delibera in items:
        print delibera['numero']

        # estrae importo
        importoStr = ""
        importo = 0
        matchObj = re.match( r'.*EURO ([0-9\.,]*).*', delibera['oggetto'], re.M|re.I)
        if matchObj:
            print "matchObj.group(1) : ", matchObj.group(1)
            importoStr =  matchObj.group(1)
            if importoStr .endswith('.') or importoStr .endswith(',') :
                importoStr = importoStr [:len(importoStr )-1]
            # trasfoma in numero
            if len(importoStr) > 2:
                importoStr = importoStr .replace(".","")
                importoStr = importoStr .replace(",",".")
                try:
                    importo = float(importoStr)
                except:
                    importo = 0
        else:
             print "No match!!"

        # formatta data
        dataStr =  delibera['data']
        anno = dataStr[6:]
        dataStr =  delibera['data']
        mese = dataStr[3:]
        mese = mese[:2]
        dataStr =  delibera['data']
        giorno = dataStr[:2]
        print(delibera['data'])
        print(anno)
        print(mese)
        print(giorno)
        dataDelibera = datetime.strptime(anno + "-" + mese + "-" + giorno, '%Y-%m-%d')   

        data = {
                  'num' : delibera['numero'],
                  'codice' : delibera['numero'],
                  'importo' : importo ,
                  'anno' : delibera['anno'],
                  'descrizione' : delibera['oggetto'],
                  'DataSalvataggio' : dataDelibera.date(),
                  'DataUltimoUpdate' : NOW,
                  'url' : ''
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

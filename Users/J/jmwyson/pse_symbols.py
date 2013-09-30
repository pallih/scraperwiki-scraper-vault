import scraperwiki
import requests
import demjson

symbolsURL = 'http://pse.com.ph/stockMarket/companyInfoSecurityProfile.html?method=getListedRecords&common=no&ajax=true'

symbolsRequest = requests.get( symbolsURL )
symbolsArray = symbolsRequest.json()

scraperwiki.sqlite.save(unique_keys=['securitySymbol'], data=symbolsArray['records'] )
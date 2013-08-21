import scraperwiki
from datetime import datetime
import requests

AQUSH = 'https://www.aqush.jp/lend/getOpenFundData'

r = requests.get(AQUSH, verify=False)
funds = r.json()
now = datetime.now()
for fund in funds:
    fund['retrieved'] = now
    scraperwiki.sqlite.save(unique_keys=['retrieved', 'fundId'], data=fund)
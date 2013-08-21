import scraperwiki
import pprint
from scrapemark import scrape  

scrape_result = scrape("""
<h1 itemprop="name">{{ name }}</h1>
<span >Rs. {{ price }}</span>
<div id="fk-stock-info-id">{{ stock_status }}.</div>
<div class="fk-product-page-offers"> <td>Free<b>{{ addons }}</b></td></div>
<ul class="feature_bullet">
{*
<li><span>{{ [features] }}</span></li>
*}
</ul>
""",

url='http://www.flipkart.com/mobiles/blackberry/itmd23frghh6hmgz?pid=mobd23fkhszytvgb&_l=qoFUjXIr2LQVya6shU4AfQ--&_r=bEBqlyY_c_N5rSwQbbPafg--&ref=06d31bde-df96-4d6b-9a2f-e3963b983155')

pprint.pprint(scrape_result, depth=3)



scraperwiki.sqlite.save(['name'], data=scrape_result)


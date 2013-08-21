# Blank Python
sourcescraper = 'desura_games'
import scraperwiki
scraperwiki.sqlite.attach(sourcescraper)
scraperwiki.sqlite.attach('exchange_rates')

def get_rate(pair):
    res = scraperwiki.sqlite.select('current from exchange_rates.swdata where pair=?', pair.upper())
    return float(res[0]['current'])

eurusd = get_rate('EURUSD')
gbpusd = get_rate('GBPUSD')

data = scraperwiki.sqlite.select('''
    count(*) as count,
    avg(price_usd) as avg_usd,
    avg(price_eur) as avg_eur,
    avg(price_gbp) as avg_gbp
    from game where price_eur>0 and price_gbp>0 and price_usd>0'''
)[0]

data.update({
    'eurusd': eurusd,
    'gbpusd': gbpusd,
    'eur_to_usd': data['avg_eur'] * eurusd,
    'gbp_to_usd': data['avg_gbp'] * gbpusd,
})

data.update(scraperwiki.sqlite.select('''
    count(case when price_usd > price_eur*? then 1 end) as eur_cheaper_count,
    count(case when price_usd < price_eur*? then 1 end) as eur_expensive_count,
    count(case when price_usd > price_gbp*? then 1 end) as gbp_cheaper_count,
    count(case when price_usd < price_gbp*? then 1 end) as gbp_expensive_count
    from game where price_eur>0 and price_gbp>0 and price_usd>0'''
    , (eurusd, eurusd, gbpusd, gbpusd)
)[0])

print '''
<style type="text/css">
td {
  padding: 1px 6px;
}
.num {
  text-align: right;
}
.green {
  color: green;
}
.red {
  color: red;
}
</style>

<h1>Summary</h1>
<p>%(count)d games considered</p>
<table style="border-collapse: collapse" border=1>
<tr><th>Currency</th><th>Avg price</th><th>Exchange rate</th><th>USD-equivalent</th><th>Nr cheaper than USD</th><th>Nr more expensive than USD</th></tr>
<tr><th>USD</th>
    <td class="num">%(avg_usd).2f</td><td class="num">1</td><td class="num">%(avg_usd).2f</td></tr>
<tr><th>EUR</th>
    <td class="num">%(avg_eur).2f</td><td class="num">%(eurusd).2f</td><td class="num">%(eur_to_usd).2f</td>
    <td>%(eur_cheaper_count)d</td><td>%(eur_expensive_count)d</td></tr>
<tr><th>GBP</th>
    <td class="num">%(avg_gbp).2f</td><td class="num">%(gbpusd).2f</td><td class="num">%(gbp_to_usd).2f</td>
    <td>%(gbp_cheaper_count)d</td><td>%(gbp_expensive_count)d</td></tr>
</table>

<h1>Games</h1>
<table style="border-collapse: collapse" border=1>
<tr><th>Title</th><th>USD</th><th></th><th>EUR</th><th>equiv.</th><th>%%</th><th></th><th>GBP</th><th>equiv.</th><th>%%</th></tr>
''' % data

rows = scraperwiki.sqlite.select('''
title, slug, price_usd * 1 as price_usd,
price_eur, price_eur * ? as eur_to_usd,
price_gbp, price_gbp * ? as gbp_to_usd
from game where price_eur>0 and price_gbp>0 and price_usd>0
order by title'''
, (eurusd, gbpusd)
)

for row in rows:
    row['eur_percent'] = row['eur_to_usd']*100/row['price_usd']
    row['eur_color'] = 'green' if (row['eur_percent'] <= 100) else 'red'
    row['gbp_percent'] = row['gbp_to_usd']*100/row['price_usd']
    row['gbp_color'] = 'green' if (row['gbp_percent'] <= 100) else 'red'

    print '''<tr><td><a href="http://www.desura.com/games/%(slug)s">%(title)s</td>
    <td class="num">%(price_usd).2f</td>
    <td></td>
    <td class="num">%(price_eur).2f</td>
    <td class="num %(eur_color)s">%(eur_to_usd).2f</td>
    <td class="num %(eur_color)s">%(eur_percent).0f</td>
    <td></td>
    <td class="num">%(price_gbp).2f</td>
    <td class="num %(gbp_color)s">%(gbp_to_usd).2f</td>
    <td class="num %(gbp_color)s">%(gbp_percent).0f</td>
    </tr>
    ''' % row

print '</table>'


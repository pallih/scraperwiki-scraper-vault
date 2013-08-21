import scraperwiki
from pygooglechart import PieChart3D

sourcescraper = 'intrade_total_trading_volume'


scraperwiki.sqlite.attach(sourcescraper, 't')

volume = scraperwiki.sqlite.select('* FROM contract_volume')
latest_date = max([v['date'] for v in volume])

contracts = scraperwiki.sqlite.select('''
contract_info.event_class, SUM(volume)
FROM contract_info INNER JOIN contract_volume 
ON contract_info.id = contract_volume.id
WHERE contract_volume.date = ?
GROUP BY event_class
''', latest_date)

volumes = dict([(d['event_class'], d['SUM(volume)']) for d in contracts])
print '<h2>Contract Volume by Category</h2>'
print '<table>'
for k,v in sorted(volumes.items(), key=lambda v:v[1], reverse=True):
    print '<tr><td>{}</td><td>{:,}</td></tr>'.format(k,v)
print '</table>'

chart = PieChart3D(300,300)
chart.add_data(volumes.values())
chart.set_pie_labels(volumes.keys())
chart_url = chart.get_url()

print '<img src = "{}">'.format(chart_url)

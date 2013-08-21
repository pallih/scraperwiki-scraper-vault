import datetime
import scraperwiki

# Serve this as an RSS feed
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")

sourcescraper = 'gsxr600segundamanoes'

rss = """
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
 <title>GSX R600</title>
 <description>Anuncios de GSX R600</description>
 <lastBuildDate>{date}</lastBuildDate>
 <pubDate>{date}</pubDate>
 {items}
</channel>
</rss>
"""

rss_item_template = """
<item>
  <title>{title}</title>
  <description>{description}</description>
  <link>{url}</link>
  <guid>{url}</guid>
  <pubDate>{date}</pubDate>
</item>
"""

items = []
scraperwiki.sqlite.attach(sourcescraper)
for data in scraperwiki.sqlite.select("* from motos"):
    for key, value in data.items():
        data[key] = value.strip().encode('utf-8')
    data['date'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data['description'] = """<img src="{img}"><br>
            {title}<br>
            {price}<br>
            {location}
    """.format(**data)
    items.append(rss_item_template.format(**data))

print rss.format(
    items='\n'.join(items), 
    date=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
)

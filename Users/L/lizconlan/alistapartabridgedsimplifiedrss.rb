require 'time'

ScraperWiki.attach("alistapart_rss")
data = ScraperWiki.select("* from `swdata` limit 25;")

feed = []

feed << '<?xml version="1.0" encoding="utf-8"?>'
feed << '<rss version="2.0">'
feed << '  <channel>'
feed << '    <title>A List Apart: The Abridged Feed</title>'
feed << '    <link>http://alistapart.com</link>'
feed << '    <description>This feed delivers ALA articles, weekly columns, and other general messages.</description>'
feed << '    <copyright>Copyright 2013, A List Apart</copyright>'
feed << '    <image>'
feed << '      <title>A List Apart</title>'
feed << '      <url>http://profile.ak.fbcdn.net/hprofile-ak-prn1/c18.18.221.221/s160x160/148338_10151216757058038_249037877_n.png</url>'
feed << '      <link>http://alistapart.com</link>'
feed << '    </image>'


data.each do |item|
  feed << "    <item>"
  feed << "        <title><![CDATA[#{item["title"]}]]></title>"
  feed << "        <link>#{item["link"]}</link>"
  feed << %|        <guid isPermaLink="false"><![CDATA[#{item["guid"]}]]></guid>|
  feed << "        <pubDate>#{Time.parse(item["published"]).strftime("%a, %d %b %Y %H:%M:%S %Z")}</pubDate>"
  feed << "    </item>"
end

feed << "  </channel>"
feed << "</rss>"

print feed.join("\n")








require 'time'

ScraperWiki.attach("alistapart_rss")
data = ScraperWiki.select("* from `swdata` limit 25;")

feed = []

feed << '<?xml version="1.0" encoding="utf-8"?>'
feed << '<rss version="2.0">'
feed << '  <channel>'
feed << '    <title>A List Apart: The Abridged Feed</title>'
feed << '    <link>http://alistapart.com</link>'
feed << '    <description>This feed delivers ALA articles, weekly columns, and other general messages.</description>'
feed << '    <copyright>Copyright 2013, A List Apart</copyright>'
feed << '    <image>'
feed << '      <title>A List Apart</title>'
feed << '      <url>http://profile.ak.fbcdn.net/hprofile-ak-prn1/c18.18.221.221/s160x160/148338_10151216757058038_249037877_n.png</url>'
feed << '      <link>http://alistapart.com</link>'
feed << '    </image>'


data.each do |item|
  feed << "    <item>"
  feed << "        <title><![CDATA[#{item["title"]}]]></title>"
  feed << "        <link>#{item["link"]}</link>"
  feed << %|        <guid isPermaLink="false"><![CDATA[#{item["guid"]}]]></guid>|
  feed << "        <pubDate>#{Time.parse(item["published"]).strftime("%a, %d %b %Y %H:%M:%S %Z")}</pubDate>"
  feed << "    </item>"
end

feed << "  </channel>"
feed << "</rss>"

print feed.join("\n")









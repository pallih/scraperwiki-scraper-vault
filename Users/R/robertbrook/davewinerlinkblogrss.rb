require 'time'

ScraperWiki.attach("davewinerlinkblogsimplerss")
data = ScraperWiki.select("* from `swdata` limit 25;")

feed = []

feed << '<?xml version="1.0" encoding="utf-8"?>'
feed << '<rss version="2.0">'
feed << '  <channel>'
feed << '    <title>Dave Winer&apos;s linkblog feed</title>'
feed << '    <link>http://static.scripting.com/myReallySimple/linkblog.html</link>'
feed << '    <description>Dave Winer&apos;s linkblog. It&apos;s my personal contribution to the World Wide River.</description>'


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

<?php
scraperwiki::httpresponseheader('Content-Type', 'application/atom+xml');
scraperwiki::attach("exfm");
$data = scraperwiki::select("* from exfm.swdata" );

?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">

<channel>
<title>TuMusika Evolution Podcast</title>
<link>http://www.tumusika.net/</link>
<language>es-es</language>
<itunes:owner>
<itunes:name>TuMusika Evolution</itunes:name>
<itunes:email>darkgiank@darkgiank.com</itunes:email>
</itunes:owner>

<?php

// .. CREACION DEL ARRAY
 foreach ($data as $item){
    echo "        <item>\n";
    echo "            <title>".$item['artist']." - ".$item['title']."</title>\n";    
    echo "            <enclosure url=\"".$item['url']."\" type=\"audio/mpeg\" />\n";
    echo "            <guid>".$item['loved_count']."</guid>\n";
    echo "        </item>\n";
}
 
?>
</channel>
</rss>
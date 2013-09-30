<?php
$noobServer = "178.159.0.60"; #redirect server
$tmdbPosterSizeUrl = "http://cf2.imgobject.com/t/p/w342";
$tmdbFanartSizeUrl = "http://cf2.imgobject.com/t/p/w1280";

scraperwiki::attach("xbmc_noobroom");

$data = scraperwiki::select(           
    "* from xbmc_noobroom.swdata"
);

print "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n";           
print "<items>\n\n";
foreach($data as $d){
if ($d["movietitle"]==null)
  {
    echo "\n";
  }
else{
  print "<item>\n";
  print "<title><![CDATA[".$d["movietitle"]."]]></title>\n";
  print "<link><![CDATA[http://noobroom5.com/14/7304dfc91298a5f79cc648ea/".$d["noobid"].".mp4]]></link>\n";
  print "<thumbnail>".$tmdbPosterSizeUrl.$d["movieposter"]."</thumbnail>\n";
  print "<genre><![CDATA[".$d["moviegenre"]."]]></genre>\n";
  print "<info><![CDATA[".$d["movieplot"]."]]></info>\n";
  print "<date>".$d["movierelease"]."</date>\n";
  print "<fanart>".$tmdbFanartSizeUrl.$d["moviefanart"]."</fanart>\n";
  print "</item>\n\n";
  }
}
print "</items>";

?>
<?php
$noobServer = "178.159.0.60"; #redirect server
$tmdbPosterSizeUrl = "http://cf2.imgobject.com/t/p/w342";
$tmdbFanartSizeUrl = "http://cf2.imgobject.com/t/p/w1280";

scraperwiki::attach("xbmc_noobroom");

$data = scraperwiki::select(           
    "* from xbmc_noobroom.swdata"
);

print "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n";           
print "<items>\n\n";
foreach($data as $d){
if ($d["movietitle"]==null)
  {
    echo "\n";
  }
else{
  print "<item>\n";
  print "<title><![CDATA[".$d["movietitle"]."]]></title>\n";
  print "<link><![CDATA[http://noobroom5.com/14/7304dfc91298a5f79cc648ea/".$d["noobid"].".mp4]]></link>\n";
  print "<thumbnail>".$tmdbPosterSizeUrl.$d["movieposter"]."</thumbnail>\n";
  print "<genre><![CDATA[".$d["moviegenre"]."]]></genre>\n";
  print "<info><![CDATA[".$d["movieplot"]."]]></info>\n";
  print "<date>".$d["movierelease"]."</date>\n";
  print "<fanart>".$tmdbFanartSizeUrl.$d["moviefanart"]."</fanart>\n";
  print "</item>\n\n";
  }
}
print "</items>";

?>

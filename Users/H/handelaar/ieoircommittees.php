<?php
require  'scraperwiki/simple_html_dom.php';
# Based on second ScraperWiki PHP tutorial

# This script outputs the URI of all the raw data XML files at oireachtas.ie
# from which the excrably-dismal official website is generated. If you want
# to import this stuff into KildareStreet, you need this data first.
#
# And then clean the shit out of it.

$html = scraperwiki::scrape("http://debates.oireachtas.ie/Committees.aspx?Dail=30");
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr[bgcolor='Gainsboro'] a,tr[bgcolor='WhiteSmoke'] a") as $data)
{
    $ctteehtml = scraperwiki::scrape("http://debates.oireachtas.ie/" . $data->href);
    $committee = new simple_html_dom();
    $committee->load($ctteehtml);
    #echo $data->href . "\n"; 
    foreach($committee->find("table[id='DebatesTable'] tr[bgcolor='Gainsboro'] a,table[id='DebatesTable'] tr[bgcolor='WhiteSmoke'] a") as $hearing) {
        $uri = "http://debates.oireachtas.ie/Xml/30/" . str_replace("DDebate.aspx?F=","",str_replace("&Ex=All&Page=1","",$hearing->href));
        scraperwiki::save(array('data'), array('data' => $uri));
        }
}

?>
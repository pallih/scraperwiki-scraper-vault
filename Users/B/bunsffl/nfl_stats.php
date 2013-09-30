<?php

$html = scraperWiki::scrape("http://sports.yahoo.com/nfl/stats/byposition?pos=QB&conference=NFL&year=season_2012&timeframe=Week1&qualified=1&sort=49&old_category=QB");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('tr[class=ysprow1]') as $data){

        $record = array(
            'qbname' => $data->children[0]->plaintext,
            'pyards' => $data->children[7]->plaintext
        );

        $record = str_replace("&nbsp;", "", $record);
        
        scraperwiki::save(array('qbname'), $record);
}
 
?>
<?php

$html = scraperWiki::scrape("http://sports.yahoo.com/nfl/stats/byposition?pos=QB&conference=NFL&year=season_2012&timeframe=Week1&qualified=1&sort=49&old_category=QB");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('tr[class=ysprow1]') as $data){

        $record = array(
            'qbname' => $data->children[0]->plaintext,
            'pyards' => $data->children[7]->plaintext
        );

        $record = str_replace("&nbsp;", "", $record);
        
        scraperwiki::save(array('qbname'), $record);
}
 
?>

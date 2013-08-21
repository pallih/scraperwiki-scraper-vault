...
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.dpp.cz/meteocidla/");
$html = scraperwiki::scrape("");

preg_match_all("|<div class=\"box-parkoviste\">(.*)</div>|Uis",$html,$match);
preg_match_all("|<class=\"\">(.*)</div>|Uis",$html,$match);

$csv = array();
$i = 0;
$sloupce = array(0=>"Datum",1=>"Silnice",2=>"Vítr");
foreach($match[0] as $m)
{
...
    $items = array();
    preg_match("|<h2>(.*)</h2>|U",$m,$h2);
    $items["nazev"] = utf8_decode($h2[1]);
    
    preg_match_all("|<li>(.*)</li>|",$m,$li);
    preg_match_all("|<li>(.*)</li>|U",$m,$li);
    
    $j = 0;...
   
       
       $items[$j] = isset($strong[1])?$strong[1]:"";
       $items[$sloupce[$j]] = isset($strong[1])?$strong[1]:"";
       ++$j;
    }
    
    ++$id;

    $items["id"] = $i;
    scraperwiki::save(array('id'), $items);
    ++$i;
}

...
?>
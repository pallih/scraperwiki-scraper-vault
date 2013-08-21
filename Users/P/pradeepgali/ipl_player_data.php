<?php
require 'scraperwiki/simple_html_dom.php';
$iplSeries="2012";
//$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league/".$iplSeries."/");
$html_content= scraperWiki::scrape("http://www.thatscricket.com/indian-premier-league"); 
$dom = str_get_html($html_content);
$i=0;

foreach ($dom->find("#eventsquads option") as $el){
//print $el;
print $el->plaintext." ".$el->value."\n"; 
$player_list=scraperWiki::scrape("http://www.thatscricket.com/src/ajaxcall.php?action=searchsquads&squad=".urlencode($el->value));
$player_dom=str_get_html($player_list);

foreach($player_dom->find(".item_title") as $ael)
        {
        //print $ael->plaintext;
        $record = array(            
            'IPL'=>$iplSeries,
            'player_url' =>  $ael->href, 
            'Name' =>  $ael->plaintext,
            'Team'=>$el->plaintext
        );
        scraperwiki::save(array('IPL','player_url','Team'), $record);
        }
$player_dom->__destruct();
}


?>

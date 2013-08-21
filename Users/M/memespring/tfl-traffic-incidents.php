<?php
    
$url = "http://trafficalerts.tfl.gov.uk/microsite/tn2007-text.php?type=0&when=1&searchtext=&zoom=%25%25zoom&easting=%25%25easting&northing=%25%25northing";


$html = scraperwiki::scrape($url);


$html = str_replace("\r\n","", $html);

$item_regex = "/<h3>.*?<\/h3><p>.*?<\/p>/";

preg_match_all($item_regex, $html, $item_matches, PREG_PATTERN_ORDER);

//Strip out the items
foreach ($item_matches[0] as $item_match){

    //title
    $title_regex = "/<h3><a href=\"#\">(.*?)\[/U";
    preg_match_all($title_regex, $item_match, $title_matches, PREG_PATTERN_ORDER);
    $title = str_replace('<h3><a href="#">', "", $title_matches[0][0]);
    $title = str_replace(' [', "", $title);
    $title = trim(str_replace('</a>', "", $title));
    $title = str_replace('(', "", $title);                    
    $title = str_replace(')', "", $title);                                        
    $title = "Traffic incident: " . $title;

           
    //link
    $link_regex = "/ \[<a href=\"([^\"]*)\"/U";
    preg_match_all($link_regex, $item_match, $link_matches, PREG_PATTERN_ORDER);
    $link = $link_matches[1][0];
    $link = trim(str_replace('[ <a href="', "", $link));                
    $link = "http://trafficalerts.tfl.gov.uk/microsite/" . $link;

    //detail
    $detail_regex = "/<p>.*?<\/p>/";        
    preg_match_all($detail_regex, $item_match, $detail_matches, PREG_PATTERN_ORDER);
    $detail =  strip_tags($detail_matches[0][0]);

    //location
    $easting_regex = "/easting=([0-9]*)&/U";
    preg_match_all($easting_regex, $link, $easting_matches, PREG_PATTERN_ORDER);        
    $easting = $easting_matches[1][0];

    $northing_regex = "/northing=([0-9]*)/";        
    preg_match_all($northing_regex, $link, $northing_matches, PREG_PATTERN_ORDER);        
    $northing = $northing_matches[1][0];

    scraperwiki::save(array('link'), array('link'=>$link, 'title'=>$title, 'detail'=> $detail, 'easting'=>$easting, 'northing'=>$northing));

    //add details
    //$this->add_spot($link, $this->source_id, $link, $lat_long->lng, 
    //    $lat_long->lat,  $title, $detail, null, null, true, null, null, null, null);


}
?>
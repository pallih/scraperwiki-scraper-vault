<?php
function print_date($when) {           
    print $when->format(DATE_ISO8601) . "\n"; 
}

function extract_data($value)
{
$htmlvalue = str_get_html($value);
//print $htmlvalue;
$link=$htmlvalue->find('li[class="first last"] a', 0);
$title=$htmlvalue->find('li[class="first last"] a', 0);
$description=$htmlvalue->find('li[class="first last"] a', 0);
$date=$htmlvalue->find('span[class="date-display-single"]', 0);
$processdate=substr($date->plaintext,-10);
//print $link->href. "\n";
//print $title->plaintext. "\n";
//print $description->plaintext. "\n";
$when = date_create_from_format('d/m/Y', $processdate); print_date($when); 
$data = array( 
    'link' => $link->href, 
   'title' => $title->plaintext,
    'description' => $description->plaintext,
    'date' => $when
);

scraperwiki::save(array('title'), $data); 
}

$html = scraperWiki::scrape("http://www.aagbi.org/education/educational-resources/tutorial-week/my-events/tutorial");           
require 'scraperwiki/simple_html_dom.php';         
$dom = new simple_html_dom();
$dom->load($html);
$dom1 = new simple_html_dom();
$dom1->load($html);
$newurl="1";
while ($newurl<>""):
$newurl="";
foreach($dom->find('li[class="pager-next"] a') as $data){
    $newurl="http://www.aagbi.org" . $data->href;
    }
$html_el = $dom->find(".view-content", 0); 
foreach ($html_el->children() as $child1) {
    //need to add code to extract and process the individual div strings  
    if (preg_match("/www.aagbi.org/i", $child1)) {
  extract_data($child1);

} else {
}
}
$html = scraperWiki::scrape($newurl);
$dom->load($html);
endwhile;

?>

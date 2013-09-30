<?php
require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape('http://www.bbmp.gov.in/index.php?option=com_content&view=article&id=401&Itemid=205');
$dom = new simple_html_dom();
$dom->load($html);
$out = array();
$index=0;
foreach($dom->find("html body div.Main div.Sheet div.Sheet-body div.contentLayout div.content div.Post div.Post-body div.Post-inner div.PostContent div.article table tbody tr td table tbody tr td div a" ) as $data){
    $href = $data->href;
    $out[$index] = urlencode('http://www.bbmp.gov.in'.$href);
    
    $index++;

}

print_r($out);
?>
<?php
require 'scraperwiki/simple_html_dom.php';
$html = scraperWiki::scrape('http://www.bbmp.gov.in/index.php?option=com_content&view=article&id=401&Itemid=205');
$dom = new simple_html_dom();
$dom->load($html);
$out = array();
$index=0;
foreach($dom->find("html body div.Main div.Sheet div.Sheet-body div.contentLayout div.content div.Post div.Post-body div.Post-inner div.PostContent div.article table tbody tr td table tbody tr td div a" ) as $data){
    $href = $data->href;
    $out[$index] = urlencode('http://www.bbmp.gov.in'.$href);
    
    $index++;

}

print_r($out);
?>

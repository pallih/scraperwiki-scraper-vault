<?php


require 'scraperwiki/simple_html_dom.php';

// Sample: http://www.osha.gov/pls/imis/establishment.inspection_detail?id=316455856

$html = scraperWiki::scrape("http://www.osha.gov/pls/imis/establishment.inspection_detail?id=316455856");
$dom = new simple_html_dom();
$dom->load($html);
$inspection_table = $dom->find('table', 1);
$info = $inspection_table->find('tr', 1);
scraperwiki::save_sqlite(array("inspection"),array("inspection"=> $info->plaintext));     
echo $info->plaintext;


$general_info_table = $dom->find('table', 4);
echo "\ngeneral info table:\n";
print_r($general_info_table->plaintext);


$wont_exist = $dom->find('table', 1999);
echo "\nwont exist:\n";
if( empty($wont_exist) ){
    echo "there was no violations table";
}
print_r($wont_exist);
// $dom->find('


//$generic_info = $dom->find('table', 2);
//$generic_info_row = $generic_info->find('tr td table tr');

//echo $generic_info_row->plaintext;
//$nr = $generic_info->find('td',0)->plaintext;
//echo "nr: {$nr}";
//nr:  NR59372


 
//           print_r($dom); 
   
?>

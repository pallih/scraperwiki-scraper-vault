<?php
require 'scraperwiki/simple_html_dom.php';  

for($i=1; $i<8;$i++){
$url = 'http://www.blacksheepwools.com/knitting-yarn.html?limit=48&p=' .$i;
$content = file_get_contents($url);

preg_match_all("/title=\".*\" class=\"product-image\">/", $content, $titles);
preg_match_all("/<p class=\"msrp\">RRP: <span class=\"price\">.*<\/span>/", $content, $rrpprices);
preg_match_all("/<p class=\"saving\">SAVE: <span class=\"price\">.*<\/span>/", $content, $savings);
$allTitles = array();
$allRRP = array();
$allSavings = array();

foreach ($titles[0] as $title)
{
    $title =  str_replace("title=\"", "", $title); 
    $title =  str_replace("\" class=\"product-image\">", "", $title);
    $allTitles[]=$title;
}

foreach ($rrpprices[0] as $rrp){
    $rrp =  str_replace("<p class=\"msrp\">RRP: <span class=\"price\">", "", $rrp); 
    $rrp =  str_replace("</span>", "", $rrp); 
    $rrp =  str_replace("£", "", $rrp);
    $allRRP[]=$rrp;
}

foreach ($savings[0] as $saved){
    $saved =  str_replace("<p class=\"saving\">SAVE: <span class=\"price\">", "", $saved); 
    $saved =  str_replace("</span>", "", $saved); 
    //$saved =  str_replace("£", "", $saved);
   
    $allSavings[]=$saved;
}


for($j=0;$j<(count($allTitles)-1);$j++)
{
$record = array(
'product' => $allTitles[$j],
'price' => "£".($allRRP[$j]-$allSavings[$j]));
scraperwiki::save(array('product','price'), $record);
//echo $allTitles[$j].", ".$allRRP[$j]." ,".$allSavings[$j]."\n");
}
   

}




?>

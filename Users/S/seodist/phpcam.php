<?php
// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
//include json;
$i = 0;
while($i<=2)
{
$html = scraperwiki::scrape('http://www.flipkart.com/cameras/all-digital-cameras?response-type=json&inf-start=%d'.$i);
//$html = scraperwiki::scrape('http://www.flipkart.com/cameras/all-digital-cameras#scrollTo=0;pageno='.$i);
//print $html;
print "\n\nEND OF HTML\n\n"; 
//$dom = new simple_html_dom();
//$dom->load($html);
//$html=json_decode($html,TRUE);
print($html);
$dom = new DOMDocument(); 
@$dom->loadHtml($html);
$xpath = new DOMXPath($dom);
$articleList = $xpath->query("//div[@class='fk-product-thumb fkp-medium']"); 
foreach ($articleList as $item)
{
    echo $item->nodeValue;
}
$i=$i+1;
}
?>

<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
$result = array();
$x=1;
$i=0;
do
  {
$i++;
$html = scraperwiki::scrape("http://www.postcode-info.co.uk/find-a-postcode.html?countyid=0&areaname=___&submitted=1&page=".$i."&order=postcode");

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 

foreach ($dom->find('td') as $td)
{
    array_push($arr, $td->plaintext);
}

$arr=array_slice($arr, 10, -6);

$max = sizeof($arr);
for ($a=0;$a<$max;$a=$a+3)
{
scraperwiki::save_sqlite(array("a"),array("a"=>$x, "b"=>$arr[$a], "c"=>$arr[$a+1], "d"=>$arr[$a+2], "e"=>$a));
$x++;
}

}
while ($i<545);


?><?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
$result = array();
$x=1;
$i=0;
do
  {
$i++;
$html = scraperwiki::scrape("http://www.postcode-info.co.uk/find-a-postcode.html?countyid=0&areaname=___&submitted=1&page=".$i."&order=postcode");

$dom = new simple_html_dom();
$dom->load($html);

$arr = array(); 

foreach ($dom->find('td') as $td)
{
    array_push($arr, $td->plaintext);
}

$arr=array_slice($arr, 10, -6);

$max = sizeof($arr);
for ($a=0;$a<$max;$a=$a+3)
{
scraperwiki::save_sqlite(array("a"),array("a"=>$x, "b"=>$arr[$a], "c"=>$arr[$a+1], "d"=>$arr[$a+2], "e"=>$a));
$x++;
}

}
while ($i<545);


?>
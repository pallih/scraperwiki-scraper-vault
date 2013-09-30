<?php
// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.gw2db.com/recipes/leatherworker");
print $html;
print "\n\nEND OF HTML\n\n"; 
$dom = new simple_html_dom();
$dom->load($html);
$arr = array(); 
foreach ($dom->find('tr') as $td)
    array_push($arr, $td->plaintext);
print_r($arr);

print json_encode($arr) . "\n";
?>

<?php
// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.gw2db.com/recipes/leatherworker");
print $html;
print "\n\nEND OF HTML\n\n"; 
$dom = new simple_html_dom();
$dom->load($html);
$arr = array(); 
foreach ($dom->find('tr') as $td)
    array_push($arr, $td->plaintext);
print_r($arr);

print json_encode($arr) . "\n";
?>


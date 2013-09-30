<?php

require 'scraperwiki/simple_html_dom.php';


$html_content = scraperwiki::scrape("http://www.epart.it/Network");


$html = str_get_html($html_content);
$items = $html->find("span[class=orange bold]");

print $items;

$num=0;
foreach ($items as $item) {
print str_replace(")","",str_replace("(","",$item->innertext));
$num=$num+str_replace(")","",str_replace("(","",$item->innertext));
}
print "\nnum:".$num;
?>
<?php

require 'scraperwiki/simple_html_dom.php';


$html_content = scraperwiki::scrape("http://www.epart.it/Network");


$html = str_get_html($html_content);
$items = $html->find("span[class=orange bold]");

print $items;

$num=0;
foreach ($items as $item) {
print str_replace(")","",str_replace("(","",$item->innertext));
$num=$num+str_replace(")","",str_replace("(","",$item->innertext));
}
print "\nnum:".$num;
?>

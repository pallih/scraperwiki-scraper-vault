<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://eventful.com/events?geo=region_id:984");
$html = str_get_html($html_content);

// Fetch page
$file = fopen($url, "r"); 

$data = '';
while (!feof($file)) {
// Extract the data from the file / url
$data .= fgets($file, 1024);
}

$doc = new DOMDocument();

$doc->loadHtml($data);

// XPath lets you search DOM documents easily
$xpath = new DOMXPath($doc);
$nodelist = $xpath->query('//table[class=mytable]');

?>
<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://eventful.com/events?geo=region_id:984");
$html = str_get_html($html_content);

// Fetch page
$file = fopen($url, "r"); 

$data = '';
while (!feof($file)) {
// Extract the data from the file / url
$data .= fgets($file, 1024);
}

$doc = new DOMDocument();

$doc->loadHtml($data);

// XPath lets you search DOM documents easily
$xpath = new DOMXPath($doc);
$nodelist = $xpath->query('//table[class=mytable]');

?>

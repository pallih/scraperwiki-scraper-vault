<?php

$html = scraperwiki::scrape('http://uk.php.net/manual/en/tokens.php');
$doc = new DOMDocument;
libxml_use_internal_errors(true);
$doc->loadHTML($html);
libxml_use_internal_errors(false);

$xpath = new DOMXPath($doc);

$rows = $xpath->query('(//div[@id="tokens"]//table)[1]//tbody/tr');

$data = array();
foreach ($rows as $row) {
    $cells  = $row->getElementsByTagName('td');
    $token  = $cells->item(0)->textContent;
    $syntax = $cells->item(1)->textContent;
    $ref    = '';
    foreach ($cells->item(2)->childNodes as $c) {
        $ref .= $doc->saveXML($c);
    }
    $data[] = array('token' => $token, 'syntax' => $syntax, 'ref' => $ref);
}

scraperwiki::save_sqlite(array('token'), $data, 'tokens');
<?php

$html = scraperwiki::scrape('http://uk.php.net/manual/en/tokens.php');
$doc = new DOMDocument;
libxml_use_internal_errors(true);
$doc->loadHTML($html);
libxml_use_internal_errors(false);

$xpath = new DOMXPath($doc);

$rows = $xpath->query('(//div[@id="tokens"]//table)[1]//tbody/tr');

$data = array();
foreach ($rows as $row) {
    $cells  = $row->getElementsByTagName('td');
    $token  = $cells->item(0)->textContent;
    $syntax = $cells->item(1)->textContent;
    $ref    = '';
    foreach ($cells->item(2)->childNodes as $c) {
        $ref .= $doc->saveXML($c);
    }
    $data[] = array('token' => $token, 'syntax' => $syntax, 'ref' => $ref);
}

scraperwiki::save_sqlite(array('token'), $data, 'tokens');

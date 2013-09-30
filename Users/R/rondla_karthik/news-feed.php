<?php
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.rediff.com/news");
print $html;
$dom = new simple_html_dom();
$dom->load($html);

    print "Rediff News";


foreach($dom->find('b') as $data) {
foreach($dom->find('div') as $data) {

    # Store data in the datastore
     print $data->plaintext . "\n";

scraperwiki::save(array('headline'), array('headline' => $data->plaintext));
scraperwiki::save(array('intro'), array('intro' => $data->plaintext));

}    }       
?>
<?php
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.rediff.com/news");
print $html;
$dom = new simple_html_dom();
$dom->load($html);

    print "Rediff News";


foreach($dom->find('b') as $data) {
foreach($dom->find('div') as $data) {

    # Store data in the datastore
     print $data->plaintext . "\n";

scraperwiki::save(array('headline'), array('headline' => $data->plaintext));
scraperwiki::save(array('intro'), array('intro' => $data->plaintext));

}    }       
?>

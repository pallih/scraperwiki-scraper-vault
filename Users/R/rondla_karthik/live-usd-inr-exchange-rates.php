<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.xe.com/ucc/convert.cgi?Amount=1&From=USD&To=INR&image.x=33&image.y=11&image=Submit");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
?><?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.xe.com/ucc/convert.cgi?Amount=1&From=USD&To=INR&image.x=33&image.y=11&image=Submit");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('td') as $data)
{
    # Store data in the datastore
    print $data->plaintext . "\n";
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
?>
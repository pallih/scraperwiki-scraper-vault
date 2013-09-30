<?php
######################################
# PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://ec.europa.eu/eures/main.jsp?acro=job&lang=en&catId=482&parentCategory=482");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('select[name=isco2] option') as $data)
{
    print $data->plaintext . "\n";
    print $data->value . "\n";
    //scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?><?php
######################################
# PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://ec.europa.eu/eures/main.jsp?acro=job&lang=en&catId=482&parentCategory=482");
print $html;

$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('select[name=isco2] option') as $data)
{
    print $data->plaintext . "\n";
    print $data->value . "\n";
    //scraperwiki::save(array('data'), array('data' => $data->plaintext));
}

?>
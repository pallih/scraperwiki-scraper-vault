<?php
require 'scraperwiki/simple_html_dom.php';

$res = scraperWiki::scrape("http://www.onewaytextlink.com/links.php?type=free&pagenum=1");
$html = str_get_html($res);

$id = 0;
foreach($html->find("a") as $data)
{
    $record = array(
        'id' => $id,
        'url' => $data->href
    );
    scraperWiki::save(array('id'), $record);
    $id++;
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

$res = scraperWiki::scrape("http://www.onewaytextlink.com/links.php?type=free&pagenum=1");
$html = str_get_html($res);

$id = 0;
foreach($html->find("a") as $data)
{
    $record = array(
        'id' => $id,
        'url' => $data->href
    );
    scraperWiki::save(array('id'), $record);
    $id++;
}

?>

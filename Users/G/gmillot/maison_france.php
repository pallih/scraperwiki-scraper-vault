<?php

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.leboncoin.fr/ventes_immobilieres/offres/aquitaine/occasions/?f=a&th=1&ret=1");
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('#hl td[nowrap] a') as $data)
{
    $entry = array();
    $entry['url'] = $data->getAttribute('href');
    $entry['titre'] = html_entity_decode($data->plaintext);

    print "scraping ".$entry['titre'].' ( '.$entry['url'].' )'.chr(10);
    $page = scraperwiki::scrape($entry['url']);
    $domPage = new simple_html_dom();
    $domPage->load($page);

    foreach($domPage->find('.lbcAdParams .ad_details') as $detail){
        $name = $detail->find('label', 0)->plaintext;
        $val = $detail->find('strong', 0)->plaintext;
        $entry[html_entity_decode($name)] = html_entity_decode($val);
    }

    $entry['description'] = html_entity_decode($domPage->find('table.AdviewContent span.lbcAd_text', 0)->plaintext);
    # Store data in the datastore
    scraperwiki::save(array('url'), $entry);
}

?>

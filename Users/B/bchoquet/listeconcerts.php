<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$pg = 0;
$dept = 69;
$baseUrl = 'http://www.infoconcert.com';

do{
    $html = scraperwiki::scrape($baseUrl."/concerts/concerts-par-departement".($pg > 0 ? '-'.$pg : '').".html?departement_id=".$dept);
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    $nodes = $dom->find('div.lst_concert_1l');

    foreach($nodes as $node)
    {
        print $node->find('a', 0)->plaintext . "\n";
        $salle = $node->next_sibling()->find('a', 1);
        $ville = $node->next_sibling()->find('a', 0);
        $dates = $node->next_sibling()->find('strong');
        $data = array(
            'artist' => $node->find('a', 0)->plaintext,
            'artist_url' => $baseUrl.$node->find('a', 0)->href,
            'salle' => $salle->plaintext,
            'salle_url' => $baseUrl.$salle->href,
            'ville' => $ville->plaintext,
            'ville_url' => $baseUrl.$ville->href,
            'dte_debut' => count($dates) > 0 ? utf8_decode($dates[0]->plaintext) : '',
            'dte_fin' => count($dates) > 1 ? utf8_decode($dates[1]->plaintext) : ''
        );

        # Store data in the datastore
        scraperwiki::save(array_keys($data), $data);
    }
    
    $pg++;

} while (count($nodes) > 0);
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';
$pg = 0;
$dept = 69;
$baseUrl = 'http://www.infoconcert.com';

do{
    $html = scraperwiki::scrape($baseUrl."/concerts/concerts-par-departement".($pg > 0 ? '-'.$pg : '').".html?departement_id=".$dept);
    
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
    $nodes = $dom->find('div.lst_concert_1l');

    foreach($nodes as $node)
    {
        print $node->find('a', 0)->plaintext . "\n";
        $salle = $node->next_sibling()->find('a', 1);
        $ville = $node->next_sibling()->find('a', 0);
        $dates = $node->next_sibling()->find('strong');
        $data = array(
            'artist' => $node->find('a', 0)->plaintext,
            'artist_url' => $baseUrl.$node->find('a', 0)->href,
            'salle' => $salle->plaintext,
            'salle_url' => $baseUrl.$salle->href,
            'ville' => $ville->plaintext,
            'ville_url' => $baseUrl.$ville->href,
            'dte_debut' => count($dates) > 0 ? utf8_decode($dates[0]->plaintext) : '',
            'dte_fin' => count($dates) > 1 ? utf8_decode($dates[1]->plaintext) : ''
        );

        # Store data in the datastore
        scraperwiki::save(array_keys($data), $data);
    }
    
    $pg++;

} while (count($nodes) > 0);
?>
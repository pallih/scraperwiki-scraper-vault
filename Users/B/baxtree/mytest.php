<?php
    print "Hello World!";
    $html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm"); 
    print $html . "\n";
    require 'scraperwiki/simple_html_dom.php'; 
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    foreach($dom->find("table[@align='left'] tr.tcont") as $data)
    { $tds = $data->find("td"); 
      $record = array( 'country' => $tds[1-10]->plaintext, 'years_in_school' => intval($tds[4]->plaintext) ); 
      print_r($record); }
scraperwiki::save(array('country'), $record); 
?>
<?php
    print "Hello World!";
    $html = scraperWiki::scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm"); 
    print $html . "\n";
    require 'scraperwiki/simple_html_dom.php'; 
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    foreach($dom->find("table[@align='left'] tr.tcont") as $data)
    { $tds = $data->find("td"); 
      $record = array( 'country' => $tds[1-10]->plaintext, 'years_in_school' => intval($tds[4]->plaintext) ); 
      print_r($record); }
scraperwiki::save(array('country'), $record); 
?>

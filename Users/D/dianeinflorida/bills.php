<?php

# Blank PHP
$html = scraperWiki::scrape("http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find(".membername") as $data){
    $tds = $data->find("a");
   {
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
      scraperwiki::save(array('country'), $record);   
    }
}


?>
<?php

# Blank PHP
$html = scraperWiki::scrape("http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx");

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find(".membername") as $data){
    $tds = $data->find("a");
   {
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
      scraperwiki::save(array('country'), $record);   
    }
}


?>

<?php

$recCount = 18718;
$offsetCount = 0;

require 'scraperwiki/simple_html_dom.php';           
        
while ($offsetCount < $recCount) {
        
        $html = scraperWiki::scrape("http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us");
        
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find("il") as $trs ){
          $tds = $trs->find("il");
        
            if (intval($tds[0]->plaintext) > 0) {

                $district = $tds[2]->plaintext;
                if ($district == '&nbsp;') { $district = ''; };

                $record = array(
                    'id' => $tds[0]->plaintext, 
                    'name' => $tds[1]->plaintext,
                    'district' => $district,
                    'state' => $tds[3]->plaintext
                );
                scraperwiki::save(array('id'), $record);
            }
        }
        
        $offsetCount += 50;
}
?>
<?php

$recCount = 18718;
$offsetCount = 0;

require 'scraperwiki/simple_html_dom.php';           
        
while ($offsetCount < $recCount) {
        
        $html = scraperWiki::scrape("http://www.linkedin.com/jsearch?keywords=marketing&searchLocationType=I&countryCode=us");
        
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find("il") as $trs ){
          $tds = $trs->find("il");
        
            if (intval($tds[0]->plaintext) > 0) {

                $district = $tds[2]->plaintext;
                if ($district == '&nbsp;') { $district = ''; };

                $record = array(
                    'id' => $tds[0]->plaintext, 
                    'name' => $tds[1]->plaintext,
                    'district' => $district,
                    'state' => $tds[3]->plaintext
                );
                scraperwiki::save(array('id'), $record);
            }
        }
        
        $offsetCount += 50;
}
?>

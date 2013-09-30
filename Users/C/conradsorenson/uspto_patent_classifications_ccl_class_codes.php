<?php

/* USPTO Patent Classification Index */
/* written 2012-07-18 by Conrad Sorenson */


/* This scraper pulls the classification numbers and titles from the USPTO index - a follow-up to obtain subclassifications and titles is planned */

$html = scraperwiki::scrape("http://www.uspto.gov/web/patents/classification/selectnumwithtitle.htm");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$class_index = 1;
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    
    if(count($tds)==4){
        $test = strlen(trim($tds[2]->plaintext));
        if($test>0){
            $record = array(
                'class_index' => $class_index,
                'class_num' => $tds[2]->plaintext, 
                'class_title' => $tds[3]->plaintext
            );
            scraperwiki::save(array('class_num'), $record);
            $class_index++;
        }
        
    }
    
}


?>
<?php

/* USPTO Patent Classification Index */
/* written 2012-07-18 by Conrad Sorenson */


/* This scraper pulls the classification numbers and titles from the USPTO index - a follow-up to obtain subclassifications and titles is planned */

$html = scraperwiki::scrape("http://www.uspto.gov/web/patents/classification/selectnumwithtitle.htm");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$class_index = 1;
foreach($dom->find("div[@align='left'] tr") as $data){
    $tds = $data->find("td");
    
    if(count($tds)==4){
        $test = strlen(trim($tds[2]->plaintext));
        if($test>0){
            $record = array(
                'class_index' => $class_index,
                'class_num' => $tds[2]->plaintext, 
                'class_title' => $tds[3]->plaintext
            );
            scraperwiki::save(array('class_num'), $record);
            $class_index++;
        }
        
    }
    
}


?>

<?php
$html = scraperWiki::scrape("http://coursetalk.org/courses/computer-science");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

foreach ($dom->find("table.course_list tr") as $el)
{
    foreach ($dom->find("tr") as $tr){
    $supplier = $tr->first_child()->children(0)->href;
        if ($supplier == "/codecademy"  || $supplier == "/coursera" || $supplier == "/udacity" || $supplier == "/edx") { 
             $supplier = substr($supplier, 1);  
             $record = array( 'course' => $supplier );

            print $tr->children(1)->children(0)->href;

         }

    scraperwiki::save(array('course'), $record);     
    }
}

/*
foreach($dom->find("div[@align='left' table") as $data){
    $tds = $data->find("td");
    if(count($tds)==12){
        $record = array(
            'country' => $tds[0]->plaintext, 
            'years_in_school' => intval($tds[4]->plaintext)
        );
        print json_encode($record) . "\n";
    }
}
*/

?>

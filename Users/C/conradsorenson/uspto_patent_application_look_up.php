<?php

/* USPTO Patent Patent Application Look Up */
/* written 2012-07-19 by Conrad Sorenson */


// This scraper downloads patent search information
// NEXT STEPS = Support multiple pages


$html = scraperwiki::scrape("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&p=1&f=S&l=50&Query=%22H.sub.2Se%22+AND+CCL%2F438%2F%24&d=PG01");

//http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=0&f=S&l=50&d=PG01&OS=%22H.sub.2Se%22+AND+CCL%2F438%2F%24&RS=%28%22H.sub.2Se%22+AND+CCL%2F438%2F%24%29&TD=304&Srch1=%28%2522H.sub.2Se%2522+AND+438%252F%24.CCLS.%29&StartAt=Jump+To&StartNum=51&Query=%22H.sub.2Se%22+AND+CCL%2F438%2F%24

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);
$count = 1;
foreach($dom->find("tr[] tr") as $data){
    $tds = $data->find("td");
    

    if(count($tds)>1){

        $record = array (
            'index' => $count,
            'AppNo' => $tds[1]->plaintext, 
            'title' => $tds[2]->plaintext
        );
        scraperwiki::save(array('index'), $record);


        $count++; 

    }

}


?>

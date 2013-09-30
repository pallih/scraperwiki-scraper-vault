<?php

/* USPTO Patent Application Information Extraction */
/* written 2012-07-19 by Conrad Sorenson */


// This scraper extracts information from patent applications

//  THIS IS A WORK IN PROGRESS


$html = scraperwiki::scrape("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%2220120180870%22.PGNR.&OS=DN/20120180870&RS=DN/20120180870");
//$html = scraperwiki::scrape("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%2220120180860%22.PGNR.&OS=DN/20120180860&RS=DN/20120180860");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

//echo $dom;

$count = 1;




foreach($dom->find("table[] table") as $data){
    $tables = $data->find("td");


    $loopcount = 0;

    $tc = count($tables);

    if ($loopcount==0){
        echo "There are " . $tc . " elements.\n";
    }




    while ($tc>$loopcount){
        
        //echo "<td> item " . $loopcount . "\n";
        $temp = $tables[$loopcount]->plaintext;

        $temp = str_replace("&nbsp;", " ", $temp);
        $temp = trim($temp);
        echo "\"" . $temp . "\"\n";


/*      Locate desired information:

            Application Number
            Application Title
            Publication Date
            Abstract
            Application Number Series
            File Date
            Agent
            Inventors...................DONE
            Assignees
            CCLs
            Kind Code

*/


//      Inventors
        $pos = strpos($temp,"Inventor");
    
        if($pos !== false) {
            $inventors = $temp;
            echo "INVENTORS\n";
        }



        //echo $tables[$loopcount] . "\n\n";

        $loopcount++;

    }

    echo "\n";

    $count++;

}
    

/*    if(count($tds)>1){

        $record = array (
            'index' => $count,
            'AppNo' => $tds[1]->plaintext, 
            'title' => $tds[2]->plaintext
        );
        scraperwiki::save(array('index'), $record);


        $count++; 

    }

}
*/

?>
<?php

/* USPTO Patent Application Information Extraction */
/* written 2012-07-19 by Conrad Sorenson */


// This scraper extracts information from patent applications

//  THIS IS A WORK IN PROGRESS


$html = scraperwiki::scrape("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%2220120180870%22.PGNR.&OS=DN/20120180870&RS=DN/20120180870");
//$html = scraperwiki::scrape("http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PG01&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.html&r=1&f=G&l=50&s1=%2220120180860%22.PGNR.&OS=DN/20120180860&RS=DN/20120180860");

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

//echo $dom;

$count = 1;




foreach($dom->find("table[] table") as $data){
    $tables = $data->find("td");


    $loopcount = 0;

    $tc = count($tables);

    if ($loopcount==0){
        echo "There are " . $tc . " elements.\n";
    }




    while ($tc>$loopcount){
        
        //echo "<td> item " . $loopcount . "\n";
        $temp = $tables[$loopcount]->plaintext;

        $temp = str_replace("&nbsp;", " ", $temp);
        $temp = trim($temp);
        echo "\"" . $temp . "\"\n";


/*      Locate desired information:

            Application Number
            Application Title
            Publication Date
            Abstract
            Application Number Series
            File Date
            Agent
            Inventors...................DONE
            Assignees
            CCLs
            Kind Code

*/


//      Inventors
        $pos = strpos($temp,"Inventor");
    
        if($pos !== false) {
            $inventors = $temp;
            echo "INVENTORS\n";
        }



        //echo $tables[$loopcount] . "\n\n";

        $loopcount++;

    }

    echo "\n";

    $count++;

}
    

/*    if(count($tds)>1){

        $record = array (
            'index' => $count,
            'AppNo' => $tds[1]->plaintext, 
            'title' => $tds[2]->plaintext
        );
        scraperwiki::save(array('index'), $record);


        $count++; 

    }

}
*/

?>

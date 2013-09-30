<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

    $dom = new simple_html_dom();
    
    $letters = array ('s');
    
    foreach($letters as $alph){

    $html = scraperWiki::scrape("www.bsog.in/members1.php?name1=".$alph."&submit=submit");
                   
    $dom->load($html);
    //print ($id);
    foreach($dom->find("table[border=1]") as $table)
    {
        $counter = 1;
        //print("table restarting\n");
        foreach($table->find("td[width=224]") as $tds)
        {
            //print($counter."::".$tds->plaintext);
            $record[$counter]=$tds->plaintext; //inserting into the record array
            $counter++;
            if($counter > 11){
                //$counter = 1;
                break;
             }         
        }

        foreach($table->find("td[colspan=2]") as $tds)
        {
            //print($counter."::".$tds->plaintext);
            $record[$counter]=$tds->plaintext; //inserting into the record array
            $counter++;
            if($counter > 19){
                $counter = 1;
                break;
             }      
        }
            print_r($record);
            print ("\n");
            scraperwiki::save_sqlite(array("1","2"),$record,"BSOGS");
        //}
    }
    
}
    $dom->__destruct();
    
?>
<?php

//scrapping html
require 'scraperwiki/simple_html_dom.php';           

    $dom = new simple_html_dom();
    
    $letters = array ('s');
    
    foreach($letters as $alph){

    $html = scraperWiki::scrape("www.bsog.in/members1.php?name1=".$alph."&submit=submit");
                   
    $dom->load($html);
    //print ($id);
    foreach($dom->find("table[border=1]") as $table)
    {
        $counter = 1;
        //print("table restarting\n");
        foreach($table->find("td[width=224]") as $tds)
        {
            //print($counter."::".$tds->plaintext);
            $record[$counter]=$tds->plaintext; //inserting into the record array
            $counter++;
            if($counter > 11){
                //$counter = 1;
                break;
             }         
        }

        foreach($table->find("td[colspan=2]") as $tds)
        {
            //print($counter."::".$tds->plaintext);
            $record[$counter]=$tds->plaintext; //inserting into the record array
            $counter++;
            if($counter > 19){
                $counter = 1;
                break;
             }      
        }
            print_r($record);
            print ("\n");
            scraperwiki::save_sqlite(array("1","2"),$record,"BSOGS");
        //}
    }
    
}
    $dom->__destruct();
    
?>

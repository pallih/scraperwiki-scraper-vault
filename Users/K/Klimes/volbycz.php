<?php
# Blank PHP
//scraperwiki::sqliteexecute("create table Volby ('kraj' string, 'okres' string, 'obec' string, 'kandidatka' string, `kandidat` string, 'vek' int, 'navrhujici' string, 'prislusnost' string, 'hlasy' int, 'poradi' int)");
$html = scraperWiki::scrape("http://www.volby.cz/pls/kv2010/kv22?xjazyk=CZ&xid=0&xv=23");           
//print $html . "\n";
 $html = iconv('ISO-8859-2', 'utf-8', $html);   
        
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

$tables = $dom->find("div[@class='tabulka1']");

// Tabulky kraju
print "Tabulky kraju\n";
//foreach($tables[0]->find("table") as $data1){ 
    $tmp = $tables[0]->find("table");
    $data1=$tmp[0];
    $kraj=str_replace("Jmenné seznamy - část ","",$data1->children(0)->plaintext);
   // print "|".$kraj."|\n";     

// Odkazy v tabulce kraju
print "Odkazy v tabulce kraju\n";
//foreach($data1->find("tr") as $data2){  
    
    $tmp = $data1->find("tr");
    $data2 = $tmp[2];
    
    //if($data2->children(0)->tag!="td")continue;
    $okres = $data2->children(1)->plaintext;
    $href = get_link($data2->children(2)->first_child ()->href);
    print "Stahuji: " . $href . "\n";
    $html = scraperWiki::scrape($href); 
    $html = iconv('ISO-8859-2', 'utf-8', $html);
    
    $dom->load($html);
    $tables = $dom->find("div[@class='tabulka1']");
    // Tabulka obci
    print "Tabulka obci\n";
    print "Tables[0] " . $tables[0]->innertext . "\n";
    print "Tables[0]->find " . $tables[0]->find("td[class='cislo']")->innertext ."\n";
    //foreach($tables[0]->find("td[class='cislo']") as $data3){  
        $tmp = $tables[0]->find("td[class='cislo']");
       
       // for ($i=4;$i<33;$i++){
        $data3 = $tmp[18];
        print "data3: ". $data3->innertext . "\n";   
        $href=get_link($data3->children(0)->href); 
        print "Stahuji: " . $href . "\n";
        $html = scraperWiki::scrape($href); 
        $html = iconv('ISO-8859-2', 'utf-8', $html);        
        $dom->load($html);

        $tables = $dom->find("div[@class='tabulka1']");
        $tmp = $tables[0]->find("a");
        $data = $tmp[0];
        
        
        $html = scraperWiki::scrape(get_link($data->href)); 
        $html = iconv('ISO-8859-2', 'utf-8', $html);
        $dom->load($html);
        $obec=null;
        foreach($dom->find("h3") as $data){
            if(strstr($data->plaintext,"Obec:")!=null){
            $obec=substr($data->plaintext,7);
            $obec=trim($obec);
            print "|".$obec."|\n";  
            break;
            }
        }
        if($obec==null) print "Error. Cannot find Obec\n";
        $tables = $dom->find("div[@class='tabulka1']");
        
        foreach($tables[0]->find("tr") as $data){
            if($data->children(0)->tag!="td")continue;
            
            if($data->children(0)->headers=="sa1")$i=1;
            else $i=0;
            //print "I: ". $i. "\n";
            $row[0]=$kraj;
            $row[1]=$okres;
            $row[2]=$obec;
            $row[3]=$data->children(1+$i)->plaintext;
            $row[4]=$data->children(3+$i)->plaintext;
            $row[5]=$data->children(4+$i)->plaintext;
            $row[6]=$data->children(5+$i)->plaintext;
            $row[7]=$data->children(6+$i)->plaintext;
            $row[8]=str_replace("&nbsp;","",$data->children(7+$i)->plaintext);
            $row[9]=$data->children(9+$i)->plaintext;
            /*foreach($row as $a){
                print _convert($a) . " ";
            }
            print "\n";*/
            scraperwiki::sqliteexecute("insert into Volby values (?,?,?,?,?,?,?,?,?,?)", $row);
        }
        scraperwiki::sqlitecommit(); 
 //  }
//}
//}
//  } 
//print $html . "\n";

function get_link($str)
{
    return str_replace("&amp;","&","http://www.volby.cz/pls/kv2010/".$str);
}    


?>
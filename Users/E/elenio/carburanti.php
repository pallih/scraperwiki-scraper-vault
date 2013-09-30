<?php

# Blank PHP
setlocale(LC_ALL, "it_IT");
$url = "http://carburanti.regione.fvg.it/PagUnica_Carburanti.asp";
$ch = curl_init();
// set the target url
curl_setopt($ch, CURLOPT_URL,$url);  
// howmany parameter to post 
curl_setopt($ch, CURLOPT_POST, 1);  
$http_post_fields="txgiornata=20/09/2012&txprovincia=&txcomune=&txcompagnia=&txtipo_vend=&txcarburante=GASOLIO&txPrimaRigaTabella=<tr><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>PROV.</b></font><br></td><td valign=top align=center width=110 rowspan=2><font face=Verdana size=1 color=black><b>COMUNE</b></font><br></td><td valign=top align=center width=200 rowspan=2><font face=Verdana size=1 color=black><b>UBICAZIONE<br>IMPIANTO</b></font><br></td><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>MARCHIO</b></font><br></td><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>TIPO / SERV.</b></font><br></td><td valign=top colspan=2 align=center bgcolor='#808080'><font face=Verdana size=1 color=white><b>GASOLIO</b></font></td></tr><tr><td valign=top align=center width=60><font face=Verdana size=1 color=black><b>MAX</b></font></td><td valign=top align=center width=60><font face=Verdana size=1 color=black><b>MIN</b></font></td></tr>";
curl_setopt($ch, CURLOPT_POSTFIELDS,$http_post_fields);   
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$html= curl_exec ($ch); 
curl_close ($ch); 
require 'scraperwiki/simple_html_dom.php';       
$dom = new simple_html_dom(); 
$dom->load($html);
$table= $dom->find("table",2);
//print(count($table)."a");
//print($html);
$i=1;
// initialize empty array to store the data array from each row
$theData = array();

foreach($table->find("tr") as $row) {

if ($i>=3) {
    // initialize array to store the cell data from each row
    $rowData = array();

    foreach($row->find('td') as $cell) {
        // push the cell's text to the array
        $rowData[] = $cell->plaintext;
    }
    // push the row's data array to the 'big' array
    $theData[] = $rowData;
$tds=$row->find('td');
$record = array('PROGR' => $i, 'PROVINCIA' => trim($tds[0]->plaintext), 'COMUNE' => trim($tds[1]->plaintext), 'INDIRIZZO' => trim($tds[2]->plaintext), 'INDIRIZZO_COMPLETO' => trim($tds[1]->plaintext)." (".trim($tds[0]->plaintext)."), ".trim($tds[2]->plaintext),'MARCHIO' => trim($tds[3]->find('img', 0)->getAttribute('alt')),'TIPO' => trim($tds[4]->plaintext), 'PMAX' => floatval(str_replace(",",".",$tds[5]->plaintext)), 'PMIN' => floatval(str_replace(",",".",$tds[6]->plaintext))); 

scraperwiki::save_sqlite(array('COMUNE','INDIRIZZO'), $record); 
}
$i++;
}

//print_r($theData);
//print json_encode($record) . "\n";
print $i-1;
//print_r(scraperwiki::show_tables());
/*
foreach($dom->find("tr") as $data){     Back to scraper overview
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
print "\n* * *"; 
?>
<?php

# Blank PHP
setlocale(LC_ALL, "it_IT");
$url = "http://carburanti.regione.fvg.it/PagUnica_Carburanti.asp";
$ch = curl_init();
// set the target url
curl_setopt($ch, CURLOPT_URL,$url);  
// howmany parameter to post 
curl_setopt($ch, CURLOPT_POST, 1);  
$http_post_fields="txgiornata=20/09/2012&txprovincia=&txcomune=&txcompagnia=&txtipo_vend=&txcarburante=GASOLIO&txPrimaRigaTabella=<tr><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>PROV.</b></font><br></td><td valign=top align=center width=110 rowspan=2><font face=Verdana size=1 color=black><b>COMUNE</b></font><br></td><td valign=top align=center width=200 rowspan=2><font face=Verdana size=1 color=black><b>UBICAZIONE<br>IMPIANTO</b></font><br></td><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>MARCHIO</b></font><br></td><td valign=top align=center width=40 rowspan=2><font face=Verdana size=1 color=black><b>TIPO / SERV.</b></font><br></td><td valign=top colspan=2 align=center bgcolor='#808080'><font face=Verdana size=1 color=white><b>GASOLIO</b></font></td></tr><tr><td valign=top align=center width=60><font face=Verdana size=1 color=black><b>MAX</b></font></td><td valign=top align=center width=60><font face=Verdana size=1 color=black><b>MIN</b></font></td></tr>";
curl_setopt($ch, CURLOPT_POSTFIELDS,$http_post_fields);   
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$html= curl_exec ($ch); 
curl_close ($ch); 
require 'scraperwiki/simple_html_dom.php';       
$dom = new simple_html_dom(); 
$dom->load($html);
$table= $dom->find("table",2);
//print(count($table)."a");
//print($html);
$i=1;
// initialize empty array to store the data array from each row
$theData = array();

foreach($table->find("tr") as $row) {

if ($i>=3) {
    // initialize array to store the cell data from each row
    $rowData = array();

    foreach($row->find('td') as $cell) {
        // push the cell's text to the array
        $rowData[] = $cell->plaintext;
    }
    // push the row's data array to the 'big' array
    $theData[] = $rowData;
$tds=$row->find('td');
$record = array('PROGR' => $i, 'PROVINCIA' => trim($tds[0]->plaintext), 'COMUNE' => trim($tds[1]->plaintext), 'INDIRIZZO' => trim($tds[2]->plaintext), 'INDIRIZZO_COMPLETO' => trim($tds[1]->plaintext)." (".trim($tds[0]->plaintext)."), ".trim($tds[2]->plaintext),'MARCHIO' => trim($tds[3]->find('img', 0)->getAttribute('alt')),'TIPO' => trim($tds[4]->plaintext), 'PMAX' => floatval(str_replace(",",".",$tds[5]->plaintext)), 'PMIN' => floatval(str_replace(",",".",$tds[6]->plaintext))); 

scraperwiki::save_sqlite(array('COMUNE','INDIRIZZO'), $record); 
}
$i++;
}

//print_r($theData);
//print json_encode($record) . "\n";
print $i-1;
//print_r(scraperwiki::show_tables());
/*
foreach($dom->find("tr") as $data){     Back to scraper overview
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
print "\n* * *"; 
?>

<?php
print "Hello, coding in the cloud!";

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 8; $pn < 9; $pn++) 
{
//$url = "http://www.imdb.com/title/tt".$pn."/";
$url = "http://en.600024.com/actor/rajini-movies-list/page/".$pn."/";
$url = "http://en.600024.com/actor/rajini-movies-list/";
$html = scraperwiki::scrape($url);
//print $html;
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td[class="moviegrid"]') as $data)
{
    $divs = $data->find("div");
    $mname = $divs[0]->plaintext; 
    //print $divs[2]->plaintext;  
   // print "\n"; 
    $dname = $divs[1]->plaintext;
    $mdname = $divs[2]->plaintext;  
    $record = array('MovieName'=>$mname,'MusicDirName'=>$mdname,'DirName'=>$dname); 
    scraperwiki::save_sqlite(array("MovieName","MusicDirName","DirName"),$record,"RajiniDB");
}
}
   // $m_data[$i]= $m_name->plaintext;  
   
   // $i++;
   //$record = array('murl'=>$url,'mname'=>$m_data[0],'minfo'=>$m_data[1],'mrating'=>$m_data[2],'mdirector'=>$m_data[3],'mstar'=>$m_data[4]);
            //print_r($record);
//$m_data = "";
// scraperwiki::save_sqlite(array("murl","mname","minfo","mrating","mdirector","mstar"),$record,"movdb");
    //print $data->plaintext . "\n";

?>



<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';

$i = 0;

//page 1-100
for ($p =1; $p <=100; $p++){
$dataurl = "http://wwwdb.tesri.gov.tw/tree/old_tree/tree_advsearch.asp?pn=".$p."&treecity=1&treekind=1&treeold=1&treetall=1&treepie=1&treewidth=1&treeadd=";

$html_content = scraperwiki::scrape($dataurl);
$html = str_get_html($html_content);


$raw =$html->find("table table table", 11);

//convert all big5 encoding to unicode
$data = mb_convert_encoding($raw, "UTF-8", "Big5");

//clean up the dom to make html code more readable
$data = str_replace("class='m_out' onmouseover=this.className='m_over' onmouseout=this.className='m_out'", "", $data);
$data = str_replace("bgcolor='#fefff0'", "", $data);
$data = str_replace("bgcolor='#fefff0' width='15%'", "", $data);
$data = str_replace("bgcolor='#fefff0' width='10%'", "", $data);
$data = str_replace("bgcolor='#fefff0' width='30%'", "", $data);
$data = str_replace("bgcolor='#fefff0' width='30%'", "", $data);
$data = str_replace("width='10%'", "", $data);
$data = str_replace("width='8%'", "", $data);
$data = str_replace("width='30%'", "", $data);
$data = str_replace("width='15%'", "", $data);

$data = str_replace("<tr bgcolor='#eeeeee' align=center>", "<tr>", $data);

//trip down extra tags, only keep table, tr, td, th tags
$data = strip_tags($data, '<table><tr><td><th>');

$data = str_replace("<tr><td >縣市</td><td >樹種</td><td >預測樹齡</td><td >樹高(m)</td><td >胸徑(m)</td><td >冠幅(m 2)</td><td >座落位置</td><td >擁有者</td></tr>", "<tr><th>縣市</th><th>樹種</th><th>預測樹齡</th><th>樹高(m)</th><th>胸徑(m)</th><th>冠幅(m2)</th><th>座落位置</th><th>擁有者</th></tr>", $data);


//html tidy
$tidy = tidy_parse_string($data, array('output-html' => true, 'show-body-only'=> true), 'utf8');
$tidy->cleanRepair();

$data = $tidy;

$data = preg_replace('/\s+/', ' ', $data);
$data = str_get_html($data);



foreach ($data->find("tr") as $tr){
    
     $tds = $tr->find("td");
     
    if(count($tds)==8){

    
      $record = array(
            'index' => $i, 
            '縣市' => $tds[0]->innertext, 
            '樹種' => $tds[1]->innertext, 
            '預測樹齡' => $tds[2]->innertext, 
            '樹高' => $tds[3]->innertext, 
            '胸徑' => $tds[4]->innertext, 
            '冠幅' => $tds[5]->innertext, 
            '座落位置' => $tds[6]->innertext, 
            '擁有者' => $tds[7]->innertext, 
         );

      //   print $i. "\n";

        
        scraperwiki::save_sqlite(array("index"),$record);


        $i++;
         
     }
    
    }

}

?>


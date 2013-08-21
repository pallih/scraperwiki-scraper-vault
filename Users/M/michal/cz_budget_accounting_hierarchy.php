<?php

//source: http://www.mfcr.cz/cps/rde/xchg/mfcr/xsl/vyhlasky_32273.html

require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.mfcr.cz/cps/rde/xchg/mfcr/xsl/vyhlasky_32273.html';
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);

$tables = array(
'0' => 'entry',
'1' => 'paragraph'
);

foreach ($tables as $key => $table) {

    //table
    $trs = $dom->find('div[class=tabulka2]',$key)->find('tr');
    $header = array_shift($trs);
    $ths = $header->find('th');
    foreach ($ths as $th) {
      $header_text[] = $th->plaintext;
    }
    //scraperwiki::save_sqlite(array(),$header_text, $table.'_info');

    $last = array('0'=>'','1'=>'','2'=>'','3'=>'');
    
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      if (count($tds) == 0) continue; //empty row, should not be there
    
      if (count($tds) > 1) {
        for ($j = 0; $j <= 3; $j++) {
          if(str_replace('&nbsp;','',$tds[$j]->plaintext) != '') {
    //echo $tds[$j]->outertext;
            $last[$j] = trim(str_replace('&nbsp;','',$tds[$j]->plaintext));
            for ($k = $j+1; $k <=3; $k++) $last[$k] = ''; //erase old values
            $out = array('n1'=>$last[0],'n2'=>$last[1],'n3'=>$last[2],'n4'=>$last[3]);
            $out['name'] = $tds[4]->plaintext;
   // print_r($out);
            scraperwiki::save_sqlite(array('n1','n2','n3','n4'),$out,$table);
          }
        }
      } else {
        $out['description'] = $tds[0]->plaintext;
        scraperwiki::save_sqlite(array('n1','n2','n3','n4'),$out,$table);
      }
    }

}

?>

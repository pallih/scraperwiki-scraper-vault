<?php

require 'scraperwiki/simple_html_dom.php';

$ArrRange = array('2'=>array('L'=>'1','H'=>'19'),
                    '3'=>array('L'=>'250','H'=>'699'),
                    '4'=>array('L'=>'7500','H'=>'8499'),
                    '5'=>array('L'=>'86000','H'=>'89999'),
                    '6'=>array('L'=>'900000','H'=>'949999'),
                    '7'=>array('L'=>'9900000','H'=>'9989999'));




foreach($ArrRange as $Range){
    for($I=$Range['L']; $I<= $Range['H']; $I++){
        $Isbn = sprintf('%02d',$I);
        //$SelectIsbn($Isbn);
        echo $Isbn . "\r\n";
        //$PubData = ParseHtml($Isbn);

    }
}


exit;


function ParseHtml($Isbn){
    $html = GetIsbnHtml($Isbn);

    $dom = new simple_html_dom();
    $dom->load($html);

    $domTable = new simple_html_dom();
    echo $dom->find('div.article04',0)->innertext;
    //$domTable=load($dom->find('div.article04',1)->innertext);

    foreach($domTable->find('tr') as $row){
        //echo $row->innertext . "\r\n";
    }
}

function GetIsbnHtml($Value){

    $url = 'http://www.isbn-center.jp/cgi-bin/isbndb/isbn.cgi';

    $curl=curl_init();
    curl_setopt($curl,CURLOPT_URL,$url);
    curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true) ;


    $data = array( 'sub'=>'search',
                    'id'=>'',
                    'pass'=>'',
                    'isbn'=>$Value,
                    'comp'=>'',
                    'yomi'=>'');

    curl_setopt($curl,CURLOPT_POST,true);
    curl_setopt($curl,CURLOPT_POSTFIELDS,$data);

    $res = curl_exec($curl) ;
    curl_close($curl) ;
    return mb_convert_encoding($res,'UTF-8','EUC-JP');
}


?>

<?php

require 'scraperwiki/simple_html_dom.php';

define('BASE_URL','http://www.e-gov.go.jp/link/');
define('DOMAIN_GOJP','.go.jp');
define('SELECT_LIMIT',100);
define('MAX_LOOP',10);

$GoJpLinks = array('gov'=>'index.html',
                    'ministryA'=>'ministry/a.html',
                    'ministryK'=>'ministry/k.html',
                    'ministryS'=>'ministry/s.html',
                    'ministryT'=>'ministry/t.html',
                    'ministryN'=>'ministry/n.html',
                    'ministryH'=>'ministry/h.html',
                    'ministryM'=>'ministry/m.html',
                    'ministryY'=>'ministry/y.html',
                    'ministryR'=>'ministry/w.html',
                    'ministryW'=>'ministry/r.html');

scraperwiki::save_sqlite(array("url"),array("url"=>"","date"=>date("YmdHis")));

foreach($GoJpLinks as $link){
    unset($ArrDoamins);
    $ArrDoamins = GetGoJpLinks(BASE_URL.$link);
    //var_dump($ArrDoamins);
    SaveDomains($ArrDoamins, TRUE);
}

for($Loop=0;$Loop<MAX_LOOP;$Loop++){
    $SelectDoamins = SelectDomain();
    foreach($SelectDoamins as $Domain){
        unset($ArrDoamins);
        $ArrDoamins = GetGoJpLinks($Domain['url']);
        //var_dump($ArrDoamins);
        SaveDomains($ArrDoamins);
    
        $Domain['date'] = date("YmdHis");
        scraperwiki::save_sqlite(array("url"),$Domain);
    }
    unset($SelectDoamins);
}

exit;

function SelectDomain(){

    $result= scraperwiki::select("* from swdata where date = '' limit " . SELECT_LIMIT);
    //var_dump($result);
    return $result;
}

function SaveDomains($ArrDoamins){

    foreach($ArrDoamins as $url=>$domain){
        $arrSaveValue=array();

        $result= scraperwiki::select("* from swdata where url = '". $url. "'");
        if(count($result)<>0){ 
            //echo "skip ". $url ."\r\n";
            continue;
        }

        $arrSaveValue['url'] = $url;
        $arrSaveValue['scheme'] = $domain['scheme'];
        $arrSaveValue['host'] = $domain['host'];
        
        $hosts = explode('.',substr($domain['host'],0,-6));
        for($i=0; $i<count($hosts)-1;$i++){
            $arrSaveValue['domain_sub'] = $arrSaveValue['domain_sub'] . $hosts[$i]. ".";
        }
        if(array_key_exists('domain_sub',$arrSaveValue)){
            $arrSaveValue['domain_sub']= substr($arrSaveValue['domain_sub'],0,-1);
        }
        $arrSaveValue['domain_main'] = end($hosts).DOMAIN_GOJP;

        $arrSaveValue['title'] = $domain['title'];
        $arrSaveValue['date'] = '';

        scraperwiki::save_sqlite(array("url"),$arrSaveValue);
        echo "save ". $url ."\r\n";
    }

}

function GetGoJpLinks($Url){

    //echo "Get " . $Url . "\r\n";

    $html = scraperWiki::scrape( $Url );

    $dom = new simple_html_dom();
    $dom->load($html);

    $arrDoamins = array();
    foreach($dom->find('a') as $el){
        //echo "$el->href\r\n";
        if(strpos($el->href,DOMAIN_GOJP)<>FALSE){
            $host = parse_url($el->href);
            if($host<>FALSE){
                if($host['scheme']<>"" && strpos($host['host'],DOMAIN_GOJP)<>FALSE){
                    $url = $host['scheme'].'://'.$host['host'];
                    $arrDoamins[$url] = $host;
                    $arrDoamins[$url]['title'] =  $el->plaintext;
                }
            }
        }
    }
    return $arrDoamins;
}

?>

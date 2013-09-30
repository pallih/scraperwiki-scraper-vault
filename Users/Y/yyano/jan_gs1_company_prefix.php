<?php
require 'scraperwiki/simple_html_dom.php';

define("URL_GS1_BASE", "http://www.gepir.jp/GEPIRJapanWebSite/ResponseForm.aspx");
define("URL_GS1_PARAM","?VAL=%VAL%&LANG=JA&TYPE=1");

$iStart = scraperwiki::get_var('49');
scraperwiki::save_var('49old', $iStart );

for($i = $iStart; $i < 100000; $i++){
    //echo "$i\r\n";
    unset($Prefixes);
    unset($ArrGs1Data);
    if(SelectCountGs1Data('49', $i)<>1){
        //echo "Get $i.\r\n";
        $ArrGs1Data = GetGs1Data('49', $i, $Prefixes);
        //var_dump($ArrGs1Data);
        //var_dump($Prefixes);
        SaveGs1Data($Prefixes, $ArrGs1Data);
    } else {
        echo "skip $i.\r\n";
    }
    scraperwiki::save_var('49', $i );
}
exit;

function SelectCountGs1Data($ContryCd, $Gs1Cd){

    $sql = "COUNT(PartyCode) from swdata " .
                    "where JanType = '".$ContryCd."'" . 
                    "   and PartyCode = '". sprintf("%05d",$Gs1Cd)."'";
    //echo $sql . "\r\n";
    $value = scraperwiki::select($sql);
    //var_dump($value);
    return $value[0]['COUNT(PartyCode)'];
}

function SaveGs1Data($Prefixes, $ArrGs1Data){

    $ArrGs1Data['CodeCount'] = count($Prefixes);

    foreach($Prefixes as $Prefix){
        $ArrGs1Data['JanType'] = substr($Prefix,0,2);
        $ArrGs1Data['JanLength'] = strlen($Prefix);
        $ArrGs1Data['PartyCode'] = substr($Prefix,2);
        scraperwiki::save_sqlite(array("JanType","JanLength","PartyCode"),$ArrGs1Data);
    }
}
function GetGs1Data($ContryCd, $Gs1Cd, &$Prefixes){

    $JAN = $ContryCd . sprintf("%05d", $Gs1Cd );
    $url = URL_GS1_BASE. str_replace("%VAL%", $JAN, URL_GS1_PARAM);

    //echo "$url\r\n";
    $html = scraperWiki::scrape( $url );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $Prefixes = array();

    //error check
    $arrGs1Data['ErrMsg'] = trim($dom->find('span#DataList1_ctl00_dataRETURNMESSAGE',0)->plaintext);
    if($arrGs1Data['ErrMsg']=='unknown error code'){
        echo $JAN ." / ". $arrGs1Data['ErrMsg'] . "\r\n";
        exit;
    }
    if( $dom->find('span#DataList1_ctl00_dataNumberOfHits',0)->plaintext <> 1 ){
        echo $JAN ." / ". $arrGs1Data['ErrMsg'] . "\r\n";
        $Prefixes[] = $JAN;
        return $arrGs1Data;
    }

    foreach($dom->find('table#DataList2 span') as $el){
        $elText = trim($el->plaintext);
        switch($el->id){
            case 'DataList2_ctl00_dataGLN':
                $dom_Prefixes = new simple_html_dom();
                $dom_Prefixes ->load($el->innertext);
                foreach($dom_Prefixes ->find('td') as $el_prefix){
                    if(strlen($el_prefix->plaintext)>0){
                        $Prefixes[] = trim(substr($el_prefix->plaintext, 0, strpos($el_prefix->plaintext,"X")));
                    }
                }
                break;
            case 'DataList2_ctl00_dataPARTYNAME_JP_KN': //Party Name Kana
                $arrGs1Data['ParyNameKana'] = $elText;
                break;
            case 'DataList2_ctl00_dataPARTYNAME_JP_KJ': //Party Name Kanji
                $arrGs1Data['ParyNameKanji'] = $elText;
                break;
            case 'DataList2_ctl00_dataADDRESS_JP': //address
                $arrGs1Data['Address'] = $elText;
                break;
            case 'DataList2_ctl00_dataPOSTCODE': //postcode
                $arrGs1Data['PostCode'] = $elText;
                break;
            case 'DataList2_ctl00_dataCOUNTRYCODE': //Country Code
                $arrGs1Data['ContryCode'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPOINT_JP': //Contact Point
                $arrGs1Data['ConstctPoint'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_JP_KN': //Contact Person Kana
                $arrGs1Data['ConstctPersonKana'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_JP_KJ': //Contact Person Kanji
                $arrGs1Data['ConstctPersonKanji'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_EN': //Contact Person English
                $arrGs1Data['ConstctPersonEn'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPHONE': //Phone
                $arrGs1Data['Phone'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTFAX': //FAX
                $arrGs1Data['Fax'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTEMAIL': //e-mail
                $arrGs1Data['Mail'] = $elText;
                break;
            case 'DataList2_ctl00_dataWEBSITE': //web url
                $arrGs1Data['Web'] = $elText;
                break;
            case 'DataList2_ctl00_dataUSE': //use
                $arrGs1Data['USE'] = $elText;
                break;
            default:
                //echo $el->id . "\r\n";
        }

    }
    echo $JAN ." / ". $arrGs1Data['ParyNameKanji'] . "\r\n";

    return $arrGs1Data;
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';

define("URL_GS1_BASE", "http://www.gepir.jp/GEPIRJapanWebSite/ResponseForm.aspx");
define("URL_GS1_PARAM","?VAL=%VAL%&LANG=JA&TYPE=1");

$iStart = scraperwiki::get_var('49');
scraperwiki::save_var('49old', $iStart );

for($i = $iStart; $i < 100000; $i++){
    //echo "$i\r\n";
    unset($Prefixes);
    unset($ArrGs1Data);
    if(SelectCountGs1Data('49', $i)<>1){
        //echo "Get $i.\r\n";
        $ArrGs1Data = GetGs1Data('49', $i, $Prefixes);
        //var_dump($ArrGs1Data);
        //var_dump($Prefixes);
        SaveGs1Data($Prefixes, $ArrGs1Data);
    } else {
        echo "skip $i.\r\n";
    }
    scraperwiki::save_var('49', $i );
}
exit;

function SelectCountGs1Data($ContryCd, $Gs1Cd){

    $sql = "COUNT(PartyCode) from swdata " .
                    "where JanType = '".$ContryCd."'" . 
                    "   and PartyCode = '". sprintf("%05d",$Gs1Cd)."'";
    //echo $sql . "\r\n";
    $value = scraperwiki::select($sql);
    //var_dump($value);
    return $value[0]['COUNT(PartyCode)'];
}

function SaveGs1Data($Prefixes, $ArrGs1Data){

    $ArrGs1Data['CodeCount'] = count($Prefixes);

    foreach($Prefixes as $Prefix){
        $ArrGs1Data['JanType'] = substr($Prefix,0,2);
        $ArrGs1Data['JanLength'] = strlen($Prefix);
        $ArrGs1Data['PartyCode'] = substr($Prefix,2);
        scraperwiki::save_sqlite(array("JanType","JanLength","PartyCode"),$ArrGs1Data);
    }
}
function GetGs1Data($ContryCd, $Gs1Cd, &$Prefixes){

    $JAN = $ContryCd . sprintf("%05d", $Gs1Cd );
    $url = URL_GS1_BASE. str_replace("%VAL%", $JAN, URL_GS1_PARAM);

    //echo "$url\r\n";
    $html = scraperWiki::scrape( $url );
    
    $dom = new simple_html_dom();
    $dom->load($html);

    $Prefixes = array();

    //error check
    $arrGs1Data['ErrMsg'] = trim($dom->find('span#DataList1_ctl00_dataRETURNMESSAGE',0)->plaintext);
    if($arrGs1Data['ErrMsg']=='unknown error code'){
        echo $JAN ." / ". $arrGs1Data['ErrMsg'] . "\r\n";
        exit;
    }
    if( $dom->find('span#DataList1_ctl00_dataNumberOfHits',0)->plaintext <> 1 ){
        echo $JAN ." / ". $arrGs1Data['ErrMsg'] . "\r\n";
        $Prefixes[] = $JAN;
        return $arrGs1Data;
    }

    foreach($dom->find('table#DataList2 span') as $el){
        $elText = trim($el->plaintext);
        switch($el->id){
            case 'DataList2_ctl00_dataGLN':
                $dom_Prefixes = new simple_html_dom();
                $dom_Prefixes ->load($el->innertext);
                foreach($dom_Prefixes ->find('td') as $el_prefix){
                    if(strlen($el_prefix->plaintext)>0){
                        $Prefixes[] = trim(substr($el_prefix->plaintext, 0, strpos($el_prefix->plaintext,"X")));
                    }
                }
                break;
            case 'DataList2_ctl00_dataPARTYNAME_JP_KN': //Party Name Kana
                $arrGs1Data['ParyNameKana'] = $elText;
                break;
            case 'DataList2_ctl00_dataPARTYNAME_JP_KJ': //Party Name Kanji
                $arrGs1Data['ParyNameKanji'] = $elText;
                break;
            case 'DataList2_ctl00_dataADDRESS_JP': //address
                $arrGs1Data['Address'] = $elText;
                break;
            case 'DataList2_ctl00_dataPOSTCODE': //postcode
                $arrGs1Data['PostCode'] = $elText;
                break;
            case 'DataList2_ctl00_dataCOUNTRYCODE': //Country Code
                $arrGs1Data['ContryCode'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPOINT_JP': //Contact Point
                $arrGs1Data['ConstctPoint'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_JP_KN': //Contact Person Kana
                $arrGs1Data['ConstctPersonKana'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_JP_KJ': //Contact Person Kanji
                $arrGs1Data['ConstctPersonKanji'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPERSON_EN': //Contact Person English
                $arrGs1Data['ConstctPersonEn'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTPHONE': //Phone
                $arrGs1Data['Phone'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTFAX': //FAX
                $arrGs1Data['Fax'] = $elText;
                break;
            case 'DataList2_ctl00_dataCONTACTEMAIL': //e-mail
                $arrGs1Data['Mail'] = $elText;
                break;
            case 'DataList2_ctl00_dataWEBSITE': //web url
                $arrGs1Data['Web'] = $elText;
                break;
            case 'DataList2_ctl00_dataUSE': //use
                $arrGs1Data['USE'] = $elText;
                break;
            default:
                //echo $el->id . "\r\n";
        }

    }
    echo $JAN ." / ". $arrGs1Data['ParyNameKanji'] . "\r\n";

    return $arrGs1Data;
}


?>

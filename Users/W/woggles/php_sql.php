<?php

require 'scraperwiki/simple_html_dom.php';  
if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
$data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz");
file_put_contents("simpletest.tar.gz", $data);
exec('tar -xzvf simpletest.tar.gz');
}
require_once('simpletest/browser.php');
$browser = new SimpleBrowser();
$browser->useCookies();
$browser->get('https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx');


$viewstate = $browser->getField('__VIEWSTATE');

// $browser->setField('__VIEWSTATE', $viewstate);

$browser->setField('txtSetor', '003');
$browser->setField('txtQuadra', '006');
$browser->setField('txtLote', '0001');
$browser->setField('txtDigito', '1');
$browser->clickSubmitByName('_BtnAvancarDasii');

//$results = $browser->getField("txtNome");
$results = $browser->getContent();


$dom = new simple_html_dom();
$dom->load($results);

$arrName = array();
foreach ($dom->find('input') as $input)
    array_push($arrName, $input->name);


$arrValue = array();
foreach ($dom->find('input') as $input)
    array_push($arrValue, $input->value);

$arr = array(
        $arrName[5] => $arrValue[5],
        $arrName[6] => $arrValue[6],
        $arrName[7] => $arrValue[7],
        $arrName[8] => $arrValue[8],
        $arrName[9] => $arrValue[9],
        $arrName[11] => $arrValue[11]);
print_r($arr);
scraperwiki::save(array('txtNumIPTU'),$arr);



//    $pageurl = "https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx";
//    $html = scraperWiki::scrape($pageurl);                    
//    $dom = new simple_html_dom();
//    $dom->load($html);
//$viewstate = "dDwxMTI2NTQ5NjQ3O3Q8O2w8aTwyPjs+O2w8dDw7bDxpPDM+O2k8NT47aTw3PjtpPDk+O2k8MTE+O2k8MTM+O2k8MTc+O2k8MTk+O2k8MjM+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDAwMzs+PjtwPGw8b25LZXlVcDs+O2w8amF2YXNjcmlwdDpBdXRvX1RhYih0aGlzLCB3aW5kb3cuZG9jdW1lbnQuZnJtQ2FkYXN0cm8udHh0UXVhZHJhKVw7Oz4+Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDAwNjs+PjtwPGw8b25LZXlVcDs+O2w8amF2YXNjcmlwdDpBdXRvX1RhYih0aGlzLCB3aW5kb3cuZG9jdW1lbnQuZnJtQ2FkYXN0cm8udHh0TG90ZSlcOzs+Pj47Oz47dDxwPHA8bDxUZXh0Oz47bDwwMDAzOz4+O3A8bDxvbktleVVwOz47bDxqYXZhc2NyaXB0OkF1dG9fVGFiKHRoaXMsIHdpbmRvdy5kb2N1bWVudC5mcm1DYWRhc3Ryby50eHREaWdpdG8pXDs7Pj4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8ODs+Pjs+Ozs+O3Q8cDw7cDxsPG9uY2xpY2s7PjtsPGphdmFzY3JpcHQ6cmV0dXJuIEhlbHAoMSlcOzs+Pj47Oz47dDxwPHA8bDxUZXh0Oz47bDxOw7ptZXJvIGRlIENvbnRyaWJ1aW50ZSBDYW5jZWxhZG8uIE7Do28gw6kgcG9zc8OtdmVsIGZhemVyIGF0dWFsaXphw6fDo28gY2FkYXN0cmFsLlw8YnIvXD5WZXJpZmlxdWUgbyBuw7ptZXJvIGRlIGNvbnRyaWJ1aW50ZSBhdHVhbCBwYXJhIHByZWVuY2hpbWVudG8gZGEgYXR1YWxpemHDp8Ojby47Pj47Pjs7Pjt0PHA8cDxsPFdlYkJvdGFvQ29uZmlybWFjYW9fVmFsaWRhRm9ybXVsYXJpbzs+O2w8bzxmPjs+Pjs+Ozs+O3Q8cDxwPGw8V2ViQm90YW9Db25maXJtYWNhb19WYWxpZGFGb3JtdWxhcmlvOz47bDxvPGY+Oz4+Oz47Oz47dDxwPDtwPGw8b25DbGljazs+O2w8amF2YXNjcmlwdDpyZXR1cm4gdmVyaWZpY2FEYWMoKVw7Oz4+Pjs7Pjs+Pjs+PjtsPGhwU3FsOz4+jNVaSJ63bAz02PnxodL2mDypaAE=";

 //       $ch = curl_init($pageurl);

//        $postdata = "__VIEWSTATE=". urlencode($viewstate)  ."&txtSetor=003&txtQuadra=006&txtLote=0001&txtDigito=1";
//        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//        curl_setopt($ch, CURLOPT_HEADER, 0);
//        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//        curl_setopt($ch, CURLOPT_POST, 1);
//        curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);

//      $html = curl_exec($ch);

//      curl_close($ch);
                
//        $dom = new simple_html_dom();
//        $dom->load($html);


function verificaDac()
            {
                //VERIFICAR DAC11


                $strVerif = "00300600031";
                $i = 0 ;
                $chr = 0 ;
                $wsoma = 0 ;
                $wresto = 0;
                $ind = 0 ;
                $posfinal = 0;
                $dac = 0;

                $ind = 2;
                $wsoma = 0;
                $posfinal = strlen($strVerif) - 2;
                                
                for ($i = $posfinal; $i >= 0; $i--)
                    {
                    $chr = substr($strVerif, $i, 1);                
                    $wsoma = $wsoma + ($chr * $ind);
                    $ind = $ind + 1;
                    if ($ind == 11)
                        { $ind = 1; }
                    }                        
                $wresto = 11 - ($wsoma % 11);
                if ($wresto == 10)
                    { $dac = "1";
                  }
                else
                    if ($wresto == 11)
                        { $dac = "0"; }
                    else
                        { $dac = $wresto; }
                           
                if (substr($strVerif,10,1) != $dac) {
                }                

            }
verificaDac();
?><?php

require 'scraperwiki/simple_html_dom.php';  
if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
$data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz");
file_put_contents("simpletest.tar.gz", $data);
exec('tar -xzvf simpletest.tar.gz');
}
require_once('simpletest/browser.php');
$browser = new SimpleBrowser();
$browser->useCookies();
$browser->get('https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx');


$viewstate = $browser->getField('__VIEWSTATE');

// $browser->setField('__VIEWSTATE', $viewstate);

$browser->setField('txtSetor', '003');
$browser->setField('txtQuadra', '006');
$browser->setField('txtLote', '0001');
$browser->setField('txtDigito', '1');
$browser->clickSubmitByName('_BtnAvancarDasii');

//$results = $browser->getField("txtNome");
$results = $browser->getContent();


$dom = new simple_html_dom();
$dom->load($results);

$arrName = array();
foreach ($dom->find('input') as $input)
    array_push($arrName, $input->name);


$arrValue = array();
foreach ($dom->find('input') as $input)
    array_push($arrValue, $input->value);

$arr = array(
        $arrName[5] => $arrValue[5],
        $arrName[6] => $arrValue[6],
        $arrName[7] => $arrValue[7],
        $arrName[8] => $arrValue[8],
        $arrName[9] => $arrValue[9],
        $arrName[11] => $arrValue[11]);
print_r($arr);
scraperwiki::save(array('txtNumIPTU'),$arr);



//    $pageurl = "https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx";
//    $html = scraperWiki::scrape($pageurl);                    
//    $dom = new simple_html_dom();
//    $dom->load($html);
//$viewstate = "dDwxMTI2NTQ5NjQ3O3Q8O2w8aTwyPjs+O2w8dDw7bDxpPDM+O2k8NT47aTw3PjtpPDk+O2k8MTE+O2k8MTM+O2k8MTc+O2k8MTk+O2k8MjM+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDAwMzs+PjtwPGw8b25LZXlVcDs+O2w8amF2YXNjcmlwdDpBdXRvX1RhYih0aGlzLCB3aW5kb3cuZG9jdW1lbnQuZnJtQ2FkYXN0cm8udHh0UXVhZHJhKVw7Oz4+Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDAwNjs+PjtwPGw8b25LZXlVcDs+O2w8amF2YXNjcmlwdDpBdXRvX1RhYih0aGlzLCB3aW5kb3cuZG9jdW1lbnQuZnJtQ2FkYXN0cm8udHh0TG90ZSlcOzs+Pj47Oz47dDxwPHA8bDxUZXh0Oz47bDwwMDAzOz4+O3A8bDxvbktleVVwOz47bDxqYXZhc2NyaXB0OkF1dG9fVGFiKHRoaXMsIHdpbmRvdy5kb2N1bWVudC5mcm1DYWRhc3Ryby50eHREaWdpdG8pXDs7Pj4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8ODs+Pjs+Ozs+O3Q8cDw7cDxsPG9uY2xpY2s7PjtsPGphdmFzY3JpcHQ6cmV0dXJuIEhlbHAoMSlcOzs+Pj47Oz47dDxwPHA8bDxUZXh0Oz47bDxOw7ptZXJvIGRlIENvbnRyaWJ1aW50ZSBDYW5jZWxhZG8uIE7Do28gw6kgcG9zc8OtdmVsIGZhemVyIGF0dWFsaXphw6fDo28gY2FkYXN0cmFsLlw8YnIvXD5WZXJpZmlxdWUgbyBuw7ptZXJvIGRlIGNvbnRyaWJ1aW50ZSBhdHVhbCBwYXJhIHByZWVuY2hpbWVudG8gZGEgYXR1YWxpemHDp8Ojby47Pj47Pjs7Pjt0PHA8cDxsPFdlYkJvdGFvQ29uZmlybWFjYW9fVmFsaWRhRm9ybXVsYXJpbzs+O2w8bzxmPjs+Pjs+Ozs+O3Q8cDxwPGw8V2ViQm90YW9Db25maXJtYWNhb19WYWxpZGFGb3JtdWxhcmlvOz47bDxvPGY+Oz4+Oz47Oz47dDxwPDtwPGw8b25DbGljazs+O2w8amF2YXNjcmlwdDpyZXR1cm4gdmVyaWZpY2FEYWMoKVw7Oz4+Pjs7Pjs+Pjs+PjtsPGhwU3FsOz4+jNVaSJ63bAz02PnxodL2mDypaAE=";

 //       $ch = curl_init($pageurl);

//        $postdata = "__VIEWSTATE=". urlencode($viewstate)  ."&txtSetor=003&txtQuadra=006&txtLote=0001&txtDigito=1";
//        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//        curl_setopt($ch, CURLOPT_HEADER, 0);
//        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//        curl_setopt($ch, CURLOPT_POST, 1);
//        curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);

//      $html = curl_exec($ch);

//      curl_close($ch);
                
//        $dom = new simple_html_dom();
//        $dom->load($html);


function verificaDac()
            {
                //VERIFICAR DAC11


                $strVerif = "00300600031";
                $i = 0 ;
                $chr = 0 ;
                $wsoma = 0 ;
                $wresto = 0;
                $ind = 0 ;
                $posfinal = 0;
                $dac = 0;

                $ind = 2;
                $wsoma = 0;
                $posfinal = strlen($strVerif) - 2;
                                
                for ($i = $posfinal; $i >= 0; $i--)
                    {
                    $chr = substr($strVerif, $i, 1);                
                    $wsoma = $wsoma + ($chr * $ind);
                    $ind = $ind + 1;
                    if ($ind == 11)
                        { $ind = 1; }
                    }                        
                $wresto = 11 - ($wsoma % 11);
                if ($wresto == 10)
                    { $dac = "1";
                  }
                else
                    if ($wresto == 11)
                        { $dac = "0"; }
                    else
                        { $dac = $wresto; }
                           
                if (substr($strVerif,10,1) != $dac) {
                }                

            }
verificaDac();
?>
<?php

require 'scraperwiki/simple_html_dom.php';  
if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
$data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz");
file_put_contents("simpletest.tar.gz", $data);
exec('tar -xzvf simpletest.tar.gz');
}


function leading_zeros($value, $places){
// Function written by Marcus L. Griswold (vujsa)
// Can be found at http://www.handyphp.com
// Do not remove this header!
    $leading = "";
    if(is_numeric($value)){
        for($x = 1; $x <= $places; $x++){
            $ceiling = pow(10, $x);
            if($value < $ceiling){
                $zeros = $places - $x;
                for($y = 1; $y <= $zeros; $y++){
                    $leading .= "0";
                }
            $x = $places + 1;
            }
        }
        $output = $leading . $value;
    }
    else{
        $output = $value;
    }
    return $output;
}

        function verificaDac($setorA,$quadraA,$loteA)
            {
                //VERIFICAR DAC11

                $strVerif = $setorA.$quadraA.$loteA."1";
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
                return $dac;
            }


function getPage($s,$q,$lmin,$lmax) {        
        require_once('simpletest/browser.php');
        $browser = new SimpleBrowser();        
        $browser->useCookies();        

for ($r = $lmin; $r <= $lmax; $r++) { 


        $browser->get('https://www3.prefeitura.sp.gov.br/sf8663/formsinternet/Principal.aspx');


        $viewstate = $browser->getField('__VIEWSTATE');

        $setor = $s;
        $quadra = $q;
        $lote = leading_zeros(number_format($r,0,'',''),4);
       // $lote = leading_zeros(number_format($r),4);



$browser->setField('txtSetor', $setor);
$browser->setField('txtQuadra', $quadra);
$browser->setField('txtLote', $lote);
$browser->setField('txtDigito', verificaDac($setor,$quadra,$lote));
$browser->clickSubmitByName('_BtnAvancarDasii');


$results = $browser->getContent();


$dom = new simple_html_dom();
$dom->load($results);




$arrName = array();
foreach ($dom->find('input') as $input)
    array_push($arrName, $input->name);


$arrValue = array();
foreach ($dom->find('input') as $input)
    array_push($arrValue, $input->value);

if (empty($arrValue)) {
} else if ($arrValue[6] == "") {
 var_dump($lote);

} else {

     $arr = array(
        $arrName[5] => $arrValue[5],
        $arrName[6] => $arrValue[6],
        $arrName[7] => $arrValue[7],
        $arrName[8] => $arrValue[8],
        $arrName[9] => $arrValue[9],
        $arrName[11] => $arrValue[11]);

     scraperwiki::save(array('txtNumIPTU'),$arr);

    }
}

}

getPage("005","078",485,999);
?>
<?php

//loop for variables
    //for loop
    //$page = //get page - iterate 1-100 or before it 404's?
    
        function alphabetCombos($length,$prefix = '') {
            for($j = 97; $j < 123; $j++) {
                if ($length > 1) {
                    alphabetCombos($length-1,$prefix . chr($j));
                } else {
                    //echo $prefix . chr($j) . ' ';
                    return $prefix . chr($j);
                }
            }
        }

        //alphabetCombos(2);

$name = alphabetCombos(2); //'ab';  //name var
echo $name;
echo 'alphacombo='. " " . alphabetCombos(2);

foreach (range('1', '25') as $i)
$page =  $i; //page var

$url = '&last='. "" . alphabetCombos(2) . "" .  '&page=' . "" . $page;
//Concact
$fullurl = array('https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH',$url);

//$var = implode('', $fullurl);

//scrape $var
//echo 'var='. " " . $var;
echo $url;
?>

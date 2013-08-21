<?php
  
        function buildUrl($length,$prefix = '') {
            for($j = 97; $j < 123; $j++) {
                if ($length > 1) {
                    buildUrl($length-1,$prefix . chr($j));
                } else {                   
                    //echo $prefix . chr($j) . ' ';
                    $last = $prefix . chr($j) . '';
                    //echo $last. chr(13) . chr(10);                    
                    
                    for ($i = 0; $i < 26; $i = ++$i){
                        $page .= '' . $i .'';
                    $page = '&page='. $i;              
                          
                    //echo $page. chr(13) . chr(10);
                    
                    $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                    echo $fullUrl ;
 }
                    //return $alpha;
                }
            }
        }

buildUrl(2);

//getPage();

//alphabetCombos(2). "". getPage();
       

                    //foreach (range('1', '25') as $i);
                    //    $page = '&page=' . $i;
                    //echo "https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=" . "" . $last . "" . $page;
                    //echo "   Return var ";

?>
<?php
  
        function buildUrl($length,$prefix = '') {
            for($j = 97; $j < 123; $j++) {
                if ($length > 1) {
                    buildUrl($length-1,$prefix . chr($j));
                } else {                   
                    //echo $prefix . chr($j) . ' ';
                    $last = $prefix . chr($j) . '';
                    //echo $last. chr(13) . chr(10);                    
                    
                    for ($i = 0; $i < 26; $i = ++$i){
                        $page .= '' . $i .'';
                    $page = '&page='. $i;              
                          
                    //echo $page. chr(13) . chr(10);
                    
                    $fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
                    echo $fullUrl ;
 }
                    //return $alpha;
                }
            }
        }

buildUrl(2);

//getPage();

//alphabetCombos(2). "". getPage();
       

                    //foreach (range('1', '25') as $i);
                    //    $page = '&page=' . $i;
                    //echo "https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=" . "" . $last . "" . $page;
                    //echo "   Return var ";

?>

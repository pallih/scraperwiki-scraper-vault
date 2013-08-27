<?php
function buildUrl($length,$prefix = '') {
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
        buildUrl($length-1,$prefix . chr($j));
    } else {
        $last = $prefix . chr($j) . '';
        for ($i = 1; $i < 26; $i = ++$i){
            $page = '&page='. $i;              
            //$fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
            $fullUrl = '"https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . '",';
            echo $fullUrl ;
            }
        }
    }
}

buildUrl(2);

?>
<?php
function buildUrl($length,$prefix = '') {
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
        buildUrl($length-1,$prefix . chr($j));
    } else {
        $last = $prefix . chr($j) . '';
        for ($i = 1; $i < 26; $i = ++$i){
            $page = '&page='. $i;              
            //$fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
            $fullUrl = '"https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . '",';
            echo $fullUrl ;
            }
        }
    }
}

buildUrl(2);

?>
<?php
function buildUrl($length,$prefix = '') {
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
        buildUrl($length-1,$prefix . chr($j));
    } else {
        $last = $prefix . chr($j) . '';
        for ($i = 1; $i < 26; $i = ++$i){
            $page = '&page='. $i;              
            //$fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
            $fullUrl = '"https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . '",';
            echo $fullUrl ;
            }
        }
    }
}

buildUrl(2);

?>

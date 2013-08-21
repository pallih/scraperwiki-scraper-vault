<?php
    function get_url_contents($url){
        $crl = curl_init();
        $timeout = 5;
        curl_setopt ($crl, CURLOPT_URL,$url);
        curl_setopt ($crl, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt ($crl, CURLOPT_CONNECTTIMEOUT, $timeout);
        $ret = curl_exec($crl);
        curl_close($crl);
        return $ret;
    }

    $url = "https://twitter.com/search?q=%23happy%20near%3A%22Stockholm%22%20within%3A15mi&src=typd";
    $str = file_get_contents($url);

    echo $str;
?>

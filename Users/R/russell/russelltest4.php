<?php
ini_set('display_errors',1); 
error_reporting(E_ALL ^ E_NOTICE);

echo "Starting Scraper";
$ch=login();
$html=downloadUrl('https://scraperwiki.com/profiles/edit/', $ch);
echo $html;



function downloadUrl($Url, $ch){
    curl_setopt($ch, CURLOPT_URL, $Url);
    curl_setopt($ch, CURLOPT_POST, 0);
    curl_setopt($ch, CURLOPT_REFERER, "https://scraperwiki.com/login/");
    curl_setopt($ch, CURLOPT_USERAGENT, "MozillaXYZ/1.0");
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    $output = curl_exec($ch);
    echo "Executing download of page...";
    echo "<br>login-Ch:";
    echo $ch;
    var_dump($ch);
    return $output;
}

function login(){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://scraperwiki.com/login/'); //login URL
    curl_setopt ($ch, CURLOPT_POST, 1);
    $postData='
    user_or_email=a&password=a&csrfmiddlewaretoken=a';
    curl_setopt ($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt ($ch, CURLOPT_COOKIEJAR, 'cookie.txt');
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    $store = curl_exec ($ch);
    echo "Executing Login...";
    echo "<br>login-Store:";
    echo $store;
    echo "<br>login-Ch:";
    echo $ch;
    var_dump($ch);
    return $ch;
}
?>
<?php
ini_set('display_errors',1); 
error_reporting(E_ALL ^ E_NOTICE);

echo "Starting Scraper";
$ch=login();
$html=downloadUrl('https://scraperwiki.com/profiles/edit/', $ch);
echo $html;



function downloadUrl($Url, $ch){
    curl_setopt($ch, CURLOPT_URL, $Url);
    curl_setopt($ch, CURLOPT_POST, 0);
    curl_setopt($ch, CURLOPT_REFERER, "https://scraperwiki.com/login/");
    curl_setopt($ch, CURLOPT_USERAGENT, "MozillaXYZ/1.0");
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    $output = curl_exec($ch);
    echo "Executing download of page...";
    echo "<br>login-Ch:";
    echo $ch;
    var_dump($ch);
    return $output;
}

function login(){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://scraperwiki.com/login/'); //login URL
    curl_setopt ($ch, CURLOPT_POST, 1);
    $postData='
    user_or_email=a&password=a&csrfmiddlewaretoken=a';
    curl_setopt ($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt ($ch, CURLOPT_COOKIEJAR, 'cookie.txt');
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    $store = curl_exec ($ch);
    echo "Executing Login...";
    echo "<br>login-Store:";
    echo $store;
    echo "<br>login-Ch:";
    echo $ch;
    var_dump($ch);
    return $ch;
}
?>

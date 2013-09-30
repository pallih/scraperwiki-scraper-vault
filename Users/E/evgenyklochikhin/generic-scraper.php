<?php
// This is a generic scraper to get the site map
// and dig in from the root

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://ruseffect.com");
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_COOKIESESSION, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt ($ch, CURLOPT_FAILONERROR, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
$filetime = curl_getinfo($ch, CURLINFO_FILETIME);
$url_root = curl_exec($ch);
curl_close($ch);

//Random number for the data keys
$random .= md5(microtime(true).mt_rand(10000,90000));

//Array of URLs and Filetimes
$data = array(
            "Key"=>$random,
            "URL"=>$url, 
            "Date"=>$filetime);            

//Save SQLite
scraperwiki::save(array("Key"), $data);      

?>
<?php
// This is a generic scraper to get the site map
// and dig in from the root

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://ruseffect.com");
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_COOKIESESSION, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt ($ch, CURLOPT_FAILONERROR, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
$filetime = curl_getinfo($ch, CURLINFO_FILETIME);
$url_root = curl_exec($ch);
curl_close($ch);

//Random number for the data keys
$random .= md5(microtime(true).mt_rand(10000,90000));

//Array of URLs and Filetimes
$data = array(
            "Key"=>$random,
            "URL"=>$url, 
            "Date"=>$filetime);            

//Save SQLite
scraperwiki::save(array("Key"), $data);      

?>

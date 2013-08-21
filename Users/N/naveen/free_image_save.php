<?php

require 'scraperwiki/simple_html_dom.php';

$html = "";
$array = "";
$namearray = array();
$urlarray = array();

while (empty($array)) {
    
    $html_content = scraperwiki::scrape("http://unsplash.com/");
    $html = str_get_html($html_content);
    $array= array_filter($html->find("div.photo_div a"));

    if (!empty($array)) {
         echo "not empty \n";
    } else {
         echo "empty \n";
    }
}

foreach ($html->find("div.photo_div a") as $photodiv) {
    print resolveShortURL($photodiv->href). "\n";
    array_push($urlarray, resolveShortURL($photodiv->href));
    array_push($namearray ,basename(resolveShortURL($photodiv->href)));
}

for($i = 0; $i < count($urlarray); ++$i) {
print $namearray [$i]."\n";
print $urlarray[$i]."\n";
      $record = array(
        'date' => date('Y-m-d H:i:s'),
        'name' => $namearray [$i],
        'imgsrc' => $urlarray[$i]
    );
scraperwiki::save(array('date','name', 'imgsrc'), $record);
}

function is_html($string)
{
  return preg_match("/<[^<]+>/",$string,$m) != 0;
}

// Resolve Short URL
function resolveShortURL($url) {
$ch = curl_init("$url");  
curl_setopt($ch, CURLOPT_HEADER, 1);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$yy = curl_exec($ch);
curl_close($ch);
  $w = explode("\n",$yy);
 
  // Want to print the header array? Uncomment below.
  // print_r($w);

  $TheShortURL = in_array_wildcard('Location', $w);
  $url = $TheShortURL[0];
  $url = str_replace("Location:", "", "$url");
  $url = trim("$url");
return $url;
}

function in_array_wildcard ( $needle, $arr ) {
    return array_values( preg_grep( '/' . str_replace( '*', '.*', $needle ) . '/', $arr ) );
}


?>

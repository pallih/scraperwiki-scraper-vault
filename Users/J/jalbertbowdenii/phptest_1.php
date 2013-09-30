<?php
    require 'scraperwiki/simple_html_dom.php';
?>


<?php
$url="http://norfolkpublicart.org/public-art/installed-projects/";
$html = scraperWiki::scrape( $url );

$dom = new simple_html_dom();
$dom->load($html);  // 
foreach($dom->find("div[@class = 'postarea'] p") as $data){
    $linkText = $data->plaintext;
    echo $linkText;    
}


?>
<?php
    require 'scraperwiki/simple_html_dom.php';
?>


<?php
$url="http://norfolkpublicart.org/public-art/installed-projects/";
$html = scraperWiki::scrape( $url );

$dom = new simple_html_dom();
$dom->load($html);  // 
foreach($dom->find("div[@class = 'postarea'] p") as $data){
    $linkText = $data->plaintext;
    echo $linkText;    
}


?>

<?php
function scrapepage($url) {
    $html = scraperWiki::scrape($url);                
    $html = new simple_html_dom();
    $html->load($url);
    foreach($html->find("table[@class='products-list'] tr td h2 a") as $menu_link){
        $menu_link = $product_link->href;
        echo "Link to Details: " . $product_link . "<br>";
    }
}

scrapepage("http://www.ebioscience.com/new-products.htm");

?>
<?php
function scrapepage($url) {
    $html = scraperWiki::scrape($url);                
    $html = new simple_html_dom();
    $html->load($url);
    foreach($html->find("table[@class='products-list'] tr td h2 a") as $menu_link){
        $menu_link = $product_link->href;
        echo "Link to Details: " . $product_link . "<br>";
    }
}

scrapepage("http://www.ebioscience.com/new-products.htm");

?>

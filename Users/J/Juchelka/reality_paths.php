<?php
require 'scraperwiki/simple_html_dom.php';           

echo "Start";
$num = 1;           
for ($page = 1; $page <= 100 ; $page++)
{
    $html = scraperWiki::scrape("http://www.sreality.cz/search?hideRegions=0&distance=0.0&age=0&regionSuggest=&category_type_cb=1&category_main_cb=2&extension=0&price_max=3000000&price_min=&region=&discount=-1&usable_area-min=&usable_area-max=&flats-min=&flats-max=&sort=0&perPage=30&page=$page");
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[@class='text'] h3/a") as $data) {
        $path = $data->getAttribute('href');
        print $i."/".$page.": ".$path."\n";
        scraperwiki::save(array('path'), array(
            'path' => $path,
            'page' => $page,
            'lid' => $i,
            'date' => date("Y-m-d H:i:s"),
        ));
        $i++;
    }
}
<?php
require 'scraperwiki/simple_html_dom.php';           

echo "Start";
$num = 1;           
for ($page = 1; $page <= 100 ; $page++)
{
    $html = scraperWiki::scrape("http://www.sreality.cz/search?hideRegions=0&distance=0.0&age=0&regionSuggest=&category_type_cb=1&category_main_cb=2&extension=0&price_max=3000000&price_min=&region=&discount=-1&usable_area-min=&usable_area-max=&flats-min=&flats-max=&sort=0&perPage=30&page=$page");
    
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div[@class='text'] h3/a") as $data) {
        $path = $data->getAttribute('href');
        print $i."/".$page.": ".$path."\n";
        scraperwiki::save(array('path'), array(
            'path' => $path,
            'page' => $page,
            'lid' => $i,
            'date' => date("Y-m-d H:i:s"),
        ));
        $i++;
    }
}

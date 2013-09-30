<?php
require 'scraperwiki/simple_html_dom.php';           

echo "Start Rent";
$num = 1;           
for ($page = 1; $page <= 3 ; $page++)
{
    $html = scraperWiki::scrape("http://www.sreality.cz/search?category_type_cb=2&category_main_cb=2&price_min=&price_max=15000&region=Brno&distance=25&usable_area-min=&usable_area-max=&flats-min=&flats-max=&age=0&extension=1&sort=1&hideRegions=0&discount=-1&perPage=30&page=$page");
    
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

echo "Start Rent";
$num = 1;           
for ($page = 1; $page <= 3 ; $page++)
{
    $html = scraperWiki::scrape("http://www.sreality.cz/search?category_type_cb=2&category_main_cb=2&price_min=&price_max=15000&region=Brno&distance=25&usable_area-min=&usable_area-max=&flats-min=&flats-max=&age=0&extension=1&sort=1&hideRegions=0&discount=-1&perPage=30&page=$page");
    
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

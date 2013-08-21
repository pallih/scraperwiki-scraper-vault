<?php
require 'scraperwiki/simple_html_dom.php';           

echo "Start Lands JMVS";
$num = 1;           
for ($page = 1; $page < 62 ; $page++)
{
    $html = scraperWiki::scrape("http://www.sreality.cz/search?category_type_cb=1&category_main_cb=3&sub[]=19&price_min=&price_max=&region=&distance=0&rg[]=14&rg[]=9&estate_area-min=1000&estate_area-max=&age=0&extension=1&sort=1&hideRegions=0&discount=-1&perPage=30&page=$page");
    
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

<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// Page we need to visit.
$etrailer_links = array(
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=48",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=96",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=144",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=192",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=240",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=288",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=336",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=384",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=432",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=480",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=528",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=576",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=624",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=672",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=720",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=768",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=816",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=864",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=912",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=960",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=1008",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=1056"
);

foreach($etrailer_links as $etrailer_link){

    // Get the HTML.
    $html_content = scraperwiki::scrape($etrailer_link);
    $html = str_get_html($html_content);

    // Define a counter.
    $n = 1;

    // Loop over the cells.
    foreach($html->find("div[@class='summaryboxsearch']") as $data){

        // Get the link, we will need to follow this link to get more info later.
        $links = $data->find("a");
        $l = $links[0]->href;

        // Parse out the url.
        $queries = parse_url($l, PHP_URL_QUERY);

        // Get the whole querystring and parse out.
        parse_str($queries);

        // Get the querystring with the key 'url' and decode it.
        $link = urldecode($url);

        // Instantiate a new scraper.
        $page_content = scraperwiki::scrape($link);
        $page = str_get_html($page_content);

        // Get the shipping information.
        $shipping_info = $page->find("div[@class='padwide'] div[@class='indentl orderbox'] div[@class='floatl'] p", 2);
        $shipping_raw = $shipping_info->plaintext;
        if(preg_match("/Shipping Weight:/i", $shipping_raw)) {
            $shipping = str_replace("Shipping Weight:&nbsp;", "", $shipping_raw);  
            $shipping = trim(str_replace("&nbsp;"," ",$shipping));
        }
        else {
            $shipping = "";
        }

        // Get the 'features.'
        $features = "";
        $features_lists = $page->find("div[@class='setwidthxxl margintsm floatl'] ul", 0);
        if(!empty($features_lists)){
            $feature_lists = $features_lists->find("li");
            foreach($feature_lists as $f){
                $features .= $f->plaintext . " ";
            }
        }

        // Get the 'brand' information.
        $brand_info = $page->find("a[@property='v:brand']", 0);
        $brand = $brand_info->innertext;

        // Get the 'category' information.
        $category_info = $page->find("a[@property='v:category']", 0);
        $category = $category_info->innertext;

        // Get the 'specs.'
        $specs = "";    
        $specs_lists = $page->find("div[@class='setwidthxxl margintsm floatl'] ul", 1);
        if(!empty($specs_lists)){
            $spec_lists = $specs_lists->find("li");
            foreach($spec_lists as $s){
                $specs .= $s->plaintext . " ";
            }
        }

        // Get the page title.
        $titles = $page->find("h3[@class='strong ltext']");
        $title = (!empty($titles[0]->innertext)) ? $titles[0]->innertext : "";

        // Get the description.
        $descriptions = $page->find("p[@property='v:description']");
        $description = (!empty($descriptions[0]->innertext)) ? $descriptions[0]->innertext : "";

        // Handle the images.
        $images = $data->find("img");
        $img_src = $images[0]->src;
        parse_str(parse_url($img_src, PHP_URL_QUERY));
        $img = urldecode($f);
        $img_alt = $images[0]->alt;

        // Handle the SKU.
        $skus = $data->find("span.sli_grid_code");
        $sku = $skus[0]->innertext;

        // Get the price.
        $prices = $data->find("span.sli_price");
        $price = str_replace("$&nbsp;","", $prices[0]->innertext);

        // Add it to an array.
        $record = array(
            'sku' => trim($sku),
            'title' => trim($title),
            'price' => trim($price),
            'shippingweight' => trim($shipping),
            'description' => trim($description),
            'features' => trim($features),
            'specs' => trim($specs),        
            'image' => trim($img), 
            'imagealt' => trim($img_alt),        
            'link' => trim($link),
            'brand' => trim($brand),
            'category' => trim($category)
        );

        // print_r(json_encode($record));
        scraperwiki::save_sqlite(array('sku'), array($record), "swdata", 2);

        $n++;
    }

    // print_r(scraperwiki::show_tables());
    // print_r(scraperwiki::sqliteexecute("select * from swdata"));

}

?><?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// Page we need to visit.
$etrailer_links = array(
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=48",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=96",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=144",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=192",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=240",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=288",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=336",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=384",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=432",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=480",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=528",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=576",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=624",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USWSD02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=672",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=720",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=768",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=816",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=864",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=912",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=960",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=1008",
  "http://accessories.etrailer.com/search?p=Q&srid=S1-USCDR02&lbc=etrailer&ts=v2&w=Thule%20Parts&uid=403981297&cnt=48&method=and&method=and&isort=score&view=grid&srt=1056"
);

foreach($etrailer_links as $etrailer_link){

    // Get the HTML.
    $html_content = scraperwiki::scrape($etrailer_link);
    $html = str_get_html($html_content);

    // Define a counter.
    $n = 1;

    // Loop over the cells.
    foreach($html->find("div[@class='summaryboxsearch']") as $data){

        // Get the link, we will need to follow this link to get more info later.
        $links = $data->find("a");
        $l = $links[0]->href;

        // Parse out the url.
        $queries = parse_url($l, PHP_URL_QUERY);

        // Get the whole querystring and parse out.
        parse_str($queries);

        // Get the querystring with the key 'url' and decode it.
        $link = urldecode($url);

        // Instantiate a new scraper.
        $page_content = scraperwiki::scrape($link);
        $page = str_get_html($page_content);

        // Get the shipping information.
        $shipping_info = $page->find("div[@class='padwide'] div[@class='indentl orderbox'] div[@class='floatl'] p", 2);
        $shipping_raw = $shipping_info->plaintext;
        if(preg_match("/Shipping Weight:/i", $shipping_raw)) {
            $shipping = str_replace("Shipping Weight:&nbsp;", "", $shipping_raw);  
            $shipping = trim(str_replace("&nbsp;"," ",$shipping));
        }
        else {
            $shipping = "";
        }

        // Get the 'features.'
        $features = "";
        $features_lists = $page->find("div[@class='setwidthxxl margintsm floatl'] ul", 0);
        if(!empty($features_lists)){
            $feature_lists = $features_lists->find("li");
            foreach($feature_lists as $f){
                $features .= $f->plaintext . " ";
            }
        }

        // Get the 'brand' information.
        $brand_info = $page->find("a[@property='v:brand']", 0);
        $brand = $brand_info->innertext;

        // Get the 'category' information.
        $category_info = $page->find("a[@property='v:category']", 0);
        $category = $category_info->innertext;

        // Get the 'specs.'
        $specs = "";    
        $specs_lists = $page->find("div[@class='setwidthxxl margintsm floatl'] ul", 1);
        if(!empty($specs_lists)){
            $spec_lists = $specs_lists->find("li");
            foreach($spec_lists as $s){
                $specs .= $s->plaintext . " ";
            }
        }

        // Get the page title.
        $titles = $page->find("h3[@class='strong ltext']");
        $title = (!empty($titles[0]->innertext)) ? $titles[0]->innertext : "";

        // Get the description.
        $descriptions = $page->find("p[@property='v:description']");
        $description = (!empty($descriptions[0]->innertext)) ? $descriptions[0]->innertext : "";

        // Handle the images.
        $images = $data->find("img");
        $img_src = $images[0]->src;
        parse_str(parse_url($img_src, PHP_URL_QUERY));
        $img = urldecode($f);
        $img_alt = $images[0]->alt;

        // Handle the SKU.
        $skus = $data->find("span.sli_grid_code");
        $sku = $skus[0]->innertext;

        // Get the price.
        $prices = $data->find("span.sli_price");
        $price = str_replace("$&nbsp;","", $prices[0]->innertext);

        // Add it to an array.
        $record = array(
            'sku' => trim($sku),
            'title' => trim($title),
            'price' => trim($price),
            'shippingweight' => trim($shipping),
            'description' => trim($description),
            'features' => trim($features),
            'specs' => trim($specs),        
            'image' => trim($img), 
            'imagealt' => trim($img_alt),        
            'link' => trim($link),
            'brand' => trim($brand),
            'category' => trim($category)
        );

        // print_r(json_encode($record));
        scraperwiki::save_sqlite(array('sku'), array($record), "swdata", 2);

        $n++;
    }

    // print_r(scraperwiki::show_tables());
    // print_r(scraperwiki::sqliteexecute("select * from swdata"));

}

?>
<?php
require 'scraperwiki/simple_html_dom.php';           

// A map of Envirofone iPad labels to OUR iPad labels
$array = array(
    "iPad Wi-Fi 16GB" => "iPad 1 16GB Wi-Fi",
    "iPad Wi-Fi 32GB" => "iPad 1 32GB Wi-Fi",
    "iPad Wi-Fi 64GB" => "iPad 1 64GB Wi-Fi",

    "iPad Wi-Fi + 3G 16GB" => "iPad 1 16GB 3G",
    "iPad Wi-Fi + 3G 32GB" => "iPad 1 32GB 3G",
    "iPad Wi-Fi + 3G 64GB" => "iPad 1 64GB 3G",

    "iPad 2 Wi-Fi 16GB" => "iPad 2 16GB Wi-Fi",
    "iPad 2 Wi-Fi 32GB" => "iPad 2 32GB Wi-Fi",
    "iPad 2 Wi-Fi 64GB" => "iPad 2 64GB Wi-Fi",

    "iPad 2 Wi-Fi + 3G 16GB" => "iPad 2 16GB 3G",
    "iPad 2 Wi-Fi + 3G 32GB" => "iPad 2 32GB 3G",
    "iPad 2 Wi-Fi + 3G 64GB" => "iPad 2 64GB 3G",

    "iPad 3 Wi-Fi 16GB" => "iPad 3 16GB Wi-Fi",
    "iPad 3 Wi-Fi 32GB" => "iPad 3 32GB Wi-Fi",
    "iPad 3 Wi-Fi 64GB" => "iPad 3 64GB Wi-Fi",

    "iPad 3 Wi-Fi + 4G 16GB" => "iPad 3 16GB 3G",
    "iPad 3 Wi-Fi + 4G 32GB" => "iPad 3 32GB 3G",
    "iPad 3 Wi-Fi + 4G 64GB" => "iPad 3 64GB 3G",

    "iPad 4 Wi-Fi 16GB" => "iPad 4 16GB Wi-Fi",
    "iPad 4 Wi-Fi 32GB" => "iPad 4 32GB Wi-Fi",
    "iPad 4 Wi-Fi 64GB" => "iPad 4 64GB Wi-Fi",

    "iPad 4 Wi-Fi + 4G 16GB" => "iPad 4 16GB 3G",
    "iPad 4 Wi-Fi + 4G 32GB" => "iPad 4 32GB 3G",
    "iPad 4 Wi-Fi + 4G 64GB" => "iPad 4 64GB 3G",

    "iPad mini Wi-Fi 16GB" => "iPad Mini 16GB Wi-Fi",
    "iPad mini Wi-Fi 32GB" => "iPad Mini 32GB Wi-Fi",
    "iPad mini Wi-Fi 64GB" => "iPad Mini 64GB Wi-Fi",

    "iPad mini Wi-Fi + 4G 16GB" => "iPad Mini 16GB 3G",
    "iPad mini Wi-Fi + 4G 32GB" => "iPad Mini 32GB 3G",
    "iPad mini Wi-Fi + 4G 64GB" => "iPad Mini 64GB 3G",

);

$address = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
$html_content = scraperwiki::scrape($address);
$html = str_get_html($html_content);
foreach ($html->find("ul.results") as $el) {           
    foreach ($el->find("li") as $el2) {
        foreach ($el2->find("strong.price") as $el3) {
            foreach ($el2->find("img") as $img) {
                $item = $img->getAttribute("data-model");
            }
            $price = substr($el3->innertext, 6);
            // Use the mapping above to turn their item name into our item name
            $item = $array[$item];
            scraperwiki::save_sqlite(array("item", "seller"), array("item" => $item, "phoneholio" => $price, "my_title" => "test", "seller" => "Envirofone"));
        }
    }
}



$array = array(
    "iPad 1 16GB Wi-Fi" => "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers",
/*
    "iPad 1 16GB 3G" => "http://www.fonebank.com/sell-apple-ipad/apple-ipad-16gb-wifi-3g.aspx",
    "iPad 1 32GB Wi-Fi" => "http://www.fonebank.com/sell-apple-ipad/apple-ipad-32gb-wifi.aspx",
    "iPad 1 32GB 3G" => "http://www.fonebank.com/sell-apple-ipad/apple-ipad-32gb-wifi-3g.aspx",
    "iPad 1 64GB Wi-Fi" => "http://www.fonebank.com/sell-apple-ipad/apple-ipad-64gb-wifi.aspx",
    "iPad 1 64GB 3G" => "http://www.fonebank.com/sell-apple-ipad/apple-ipad-64gb-wifi-3g.aspx",


    "iPad 2 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-16gb-with-wi-fi/",
    "iPad 2 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-32gb-with-wi-fi/",
    "iPad 2 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-64gb-with-wi-fi/",

    "iPad 2 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-16gb-with-wi-fi-+-3g/",
    "iPad 2 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-32gb-with-wi-fi-+-3g/",
    "iPad 2 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-64gb-with-wi-fi-+-3g/",

    "iPad 3 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-with-wi-fi/",
    "iPad 3 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-with-wi-fi/",
    "iPad 3 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-with-wi-fi/",

    "iPad 3 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-with-wi-fi-+-4g/",
    "iPad 3 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-with-wi-fi-+-4g/",
    "iPad 3 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-with-wi-fi-+-4g/",

    "iPad 4 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-16gb-wi-fi/",
    "iPad 4 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-32gb-wi-fi/",
    "iPad 4 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-64gb-wi-fi/",

    "iPad 4 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-wi-fi-+-4g/",
    "iPad 4 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-wi-fi-+-4g//",
    "iPad 4 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-wi-fi-+-4g/",

    "iPad Mini 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-16gb-wi-fi/",
    "iPad Mini 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-32gb-wi-fi/",
    "iPad Mini 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-64gb-wi-fi/",

    "iPad Mini 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-16gb-wi-fi-+-4g/",
    "iPad Mini 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-32gb-wi-fi-+-4g/",
    "iPad Mini 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-64gb-wi-fi-+-4g/",
*/
);


foreach ($array as $item => $address) {
    $html_content = scraperwiki::scrape($address);
    $html = str_get_html($html_content);

    foreach ($html->find("span#ctl00_ContentPlaceHolder1_lblprice") as $el) {           
        $price = $el->innertext;
        print $price . "\n";
        scraperwiki::save_sqlite(array("item", "seller"), array("item" => $item, "price" => $price, "seller" => "Fonebank"));
    }
}


$array = array(
    // iPad 1
    "iPad 1 16GB 3G" => "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers",
    "iPad 1 16GB 3G" => "http://www.mazumamobile.com/sell_mobile_phone.php?action=view&prod=1696",
    "iPad 1 32GB Wi-Fi" => "http://www.mazumamobile.com/sell_mobile_phone.php?action=view&prod=1694",
    "iPad 1 32GB 3G" => "http://www.mazumamobile.com/sell_mobile_phone.php?action=view&prod=1697",
    "iPad 1 64GB Wi-Fi" => "http://www.mazumamobile.com/sell_mobile_phone.php?action=view&prod=1695",
    "iPad 1 64GB 3G" => "http://www.mazumamobile.com/sell_mobile_phone.php?action=view&prod=1698",
/*

    "iPad 2 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-16gb-with-wi-fi/",
    "iPad 2 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-32gb-with-wi-fi/",
    "iPad 2 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-2-64gb-with-wi-fi/",

    "iPad 2 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-16gb-with-wi-fi-+-3g/",
    "iPad 2 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-32gb-with-wi-fi-+-3g/",
    "iPad 2 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-2-64gb-with-wi-fi-+-3g/",

    "iPad 3 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-with-wi-fi/",
    "iPad 3 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-with-wi-fi/",
    "iPad 3 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-with-wi-fi/",

    "iPad 3 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-with-wi-fi-+-4g/",
    "iPad 3 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-with-wi-fi-+-4g/",
    "iPad 3 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-with-wi-fi-+-4g/",

    "iPad 4 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-16gb-wi-fi/",
    "iPad 4 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-32gb-wi-fi/",
    "iPad 4 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-4-64gb-wi-fi/",

    "iPad 4 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-16gb-wi-fi-+-4g/",
    "iPad 4 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-32gb-wi-fi-+-4g//",
    "iPad 4 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-3-64gb-wi-fi-+-4g/",

    "iPad Mini 16GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-16gb-wi-fi/",
    "iPad Mini 32GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-32gb-wi-fi/",
    "iPad Mini 64GB Wi-Fi" => "http://www.sellmymobile.com/phone/apple-ipad-mini-64gb-wi-fi/",

    "iPad Mini 16GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-16gb-wi-fi-+-4g/",
    "iPad Mini 32GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-32gb-wi-fi-+-4g/",
    "iPad Mini 64GB 3G" => "http://www.sellmymobile.com/phone/apple-ipad-mini-64gb-wi-fi-+-4g/",
*/
);


foreach ($array as $item => $address) {
    $html_content = scraperwiki::scrape($address);
    $html = str_get_html($html_content);

    foreach ($html->find("span#transferValue") as $el) {           
        $price = substr($el->innertext,7);
        print $price . "\n";
        scraperwiki::save_sqlite(array("item", "seller"), array("item" => $item, "seller" => $seller ));
    }
}

?>

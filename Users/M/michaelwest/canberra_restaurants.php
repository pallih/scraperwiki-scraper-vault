<?php

$html = "";
for($page = 8; $page < 9; $page++){
    $start = 50*($page-1);
    $address = "http://www.eatability.com.au/public/listings_by_category.jsp?classificationId=c2&countryId=co-au&sortBy=rating&SDM_PAGE=CATEGORY&locationId=ct6&SDM_AREA=HOME&crumbtrailLinkPageType=PAGE_LOCATION&PAGING_PAGE_NO=".$page."&st=".$start."#list_listings";
    $htmlPage = scraperWiki::scrape($address);
    $html .= $htmlPage;
    print("Scraped page ".$page."\n");
}

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
print("Loading into DOM...");
$dom->load($html);
print("complete.\n");

foreach($dom->find("div.listingDiv") as $lis){
  printInformation($lis);
}

foreach($dom->find("div.listingDivAlt") as $lis){
  printInformation($lis);
}

function printInformation($lis){

    $name = $lis->find("div.toMap a.c2");
    $nameText = $name[0]->innertext;
    if(strpos("Closed", $nameText)){ //restaurant is closed, don't continue processing
        return;
    }
    $nameText = str_replace("&amp;", "&", $nameText);
    $nameText = str_replace(", The", "", $nameText);
    $nameText = str_replace("The", "", $nameText);

    $suburb = $lis->find("div.toMap a.listingLoc");
    $suburbText = str_replace("&#187;", "", $suburb[0]->innertext); //extract text and remove the unwanted HTML symbol
    
    $rating = $lis->find("div.toMap span");
    $ratingText = $rating[0]->innertext;
    $ratingRound = round(floatval($ratingText), 0);

    $count = $lis->find("span.reviewCount");
    $ratingCount = $count[0]->innertext;

    $address = $lis->find("span.streetAddress");
    $addressText = str_replace("&amp;", "&", $address[0]->innertext);

    $costSpan = $lis->find("div.listingIcons span[style]");
    if(count($costSpan) > 0){
        $costText = ($costSpan[0]->innertext);   
    } else {
        $costText = "NA";
    }
    //printArray($costSpan);

    //categories
    $categories = array();
    foreach($lis->find("div.listingCopy span.linkGray a") as $cat){
        $categories[] = $cat->innertext;
    }
    $categoriesText = implode(",", $categories); 
    
    $licensed = (in_array("Licensed", $categories) ? "Yes" : "No");
    $byo = (in_array("BYO", $categories) ? "Yes" : "No");
    $vegetarian = (in_array("Vegetarian", $categories) ? "Yes" : "No");
    $bar = ((in_array("Bars", $categories) || in_array("Has Bar", $categories)) ? "Yes" : "No");
    $ethnicity = getEthnicity($categories);
    
    //print($nameText."; ".$ratingText."; ".$suburbText."; ".$addressText."; ".$costText."; ".$categoriesText."\n");

    $record = array(
            'random' => mt_rand(11111, 99999),
            'name' => $nameText, 
            'rating' => $ratingText,
            'rounded' => $ratingRound,
            'count' => $ratingCount,
            'suburb' => $suburbText,
            'address' => $addressText,
            'cost' => $costText,
            'categories' => $categoriesText,
            'licensed' => $licensed,
            'byo' => $byo,
            'vegetarian' => $vegetarian,
            'bar' => $bar,
            'ethnicity' => $ethnicity
    );
    scraperwiki::save(array('random'), $record); //store by random to avoid erasing duplicate restaurant names

}

function getEthnicity($categories){
//find ethnicity of food served if known
    $ethnicities = array("Modern Australian","Vegetarian","Chinese","Pizza","Italian","Asian","European","Indian","Japanese","Malaysian","Mexican / Latin American","Middle Eastern","Spanish","Sushi","Thai","Turkish","Vietnamese");
    foreach($categories as $category){
        if(in_array($category, $ethnicities)){ //found match, just return the first match
            return $category;
        }
    }
    //if no matches, return other
    return "Other";
}

function printArray($array){
    print("Array has ".count($array). " elements. ");
    foreach($array as $k => $v){
        print($k.": ".$v." | ");
    }
    print("\n");
}

?>
<?php

$html = "";
for($page = 8; $page < 9; $page++){
    $start = 50*($page-1);
    $address = "http://www.eatability.com.au/public/listings_by_category.jsp?classificationId=c2&countryId=co-au&sortBy=rating&SDM_PAGE=CATEGORY&locationId=ct6&SDM_AREA=HOME&crumbtrailLinkPageType=PAGE_LOCATION&PAGING_PAGE_NO=".$page."&st=".$start."#list_listings";
    $htmlPage = scraperWiki::scrape($address);
    $html .= $htmlPage;
    print("Scraped page ".$page."\n");
}

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
print("Loading into DOM...");
$dom->load($html);
print("complete.\n");

foreach($dom->find("div.listingDiv") as $lis){
  printInformation($lis);
}

foreach($dom->find("div.listingDivAlt") as $lis){
  printInformation($lis);
}

function printInformation($lis){

    $name = $lis->find("div.toMap a.c2");
    $nameText = $name[0]->innertext;
    if(strpos("Closed", $nameText)){ //restaurant is closed, don't continue processing
        return;
    }
    $nameText = str_replace("&amp;", "&", $nameText);
    $nameText = str_replace(", The", "", $nameText);
    $nameText = str_replace("The", "", $nameText);

    $suburb = $lis->find("div.toMap a.listingLoc");
    $suburbText = str_replace("&#187;", "", $suburb[0]->innertext); //extract text and remove the unwanted HTML symbol
    
    $rating = $lis->find("div.toMap span");
    $ratingText = $rating[0]->innertext;
    $ratingRound = round(floatval($ratingText), 0);

    $count = $lis->find("span.reviewCount");
    $ratingCount = $count[0]->innertext;

    $address = $lis->find("span.streetAddress");
    $addressText = str_replace("&amp;", "&", $address[0]->innertext);

    $costSpan = $lis->find("div.listingIcons span[style]");
    if(count($costSpan) > 0){
        $costText = ($costSpan[0]->innertext);   
    } else {
        $costText = "NA";
    }
    //printArray($costSpan);

    //categories
    $categories = array();
    foreach($lis->find("div.listingCopy span.linkGray a") as $cat){
        $categories[] = $cat->innertext;
    }
    $categoriesText = implode(",", $categories); 
    
    $licensed = (in_array("Licensed", $categories) ? "Yes" : "No");
    $byo = (in_array("BYO", $categories) ? "Yes" : "No");
    $vegetarian = (in_array("Vegetarian", $categories) ? "Yes" : "No");
    $bar = ((in_array("Bars", $categories) || in_array("Has Bar", $categories)) ? "Yes" : "No");
    $ethnicity = getEthnicity($categories);
    
    //print($nameText."; ".$ratingText."; ".$suburbText."; ".$addressText."; ".$costText."; ".$categoriesText."\n");

    $record = array(
            'random' => mt_rand(11111, 99999),
            'name' => $nameText, 
            'rating' => $ratingText,
            'rounded' => $ratingRound,
            'count' => $ratingCount,
            'suburb' => $suburbText,
            'address' => $addressText,
            'cost' => $costText,
            'categories' => $categoriesText,
            'licensed' => $licensed,
            'byo' => $byo,
            'vegetarian' => $vegetarian,
            'bar' => $bar,
            'ethnicity' => $ethnicity
    );
    scraperwiki::save(array('random'), $record); //store by random to avoid erasing duplicate restaurant names

}

function getEthnicity($categories){
//find ethnicity of food served if known
    $ethnicities = array("Modern Australian","Vegetarian","Chinese","Pizza","Italian","Asian","European","Indian","Japanese","Malaysian","Mexican / Latin American","Middle Eastern","Spanish","Sushi","Thai","Turkish","Vietnamese");
    foreach($categories as $category){
        if(in_array($category, $ethnicities)){ //found match, just return the first match
            return $category;
        }
    }
    //if no matches, return other
    return "Other";
}

function printArray($array){
    print("Array has ".count($array). " elements. ");
    foreach($array as $k => $v){
        print($k.": ".$v." | ");
    }
    print("\n");
}

?>

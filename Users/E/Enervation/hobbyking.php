<?php
require 'scraperwiki/simple_html_dom.php'; 

$startProductId = scraperwiki::get_var("currentId", -1);

if($startProductId == -1)
{
    print "No previous saved position found. Starting from scratch.";
}
else
{
    print "Resuming from product id $startProductId\n";
}

scraperwiki::attach("hobbyking_batteryidlist");
$batteries = scraperwiki::select("id from hobbyking_batteryidlist.swdata where id > $startProductId order by id asc");
$remainingCount = count($batteries);

print "Found $remainingCount batteries left to be scraped.";

$maxPerRun = 100;
$loopCount = 0;

foreach($batteries as $bat)
{
    if ($loopCount > $maxPerRun)
    {
        print "Ending run after $maxPerRun iterations.";
        break;
    }

    $productId = $bat['id'];
    print "Retrieving " . $productId . "\n";
    $html = scraperWiki::scrape("http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$productId");
    //print $html . "\n";
    
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    
    // Get the product data (located in a span tag). Should only be one product data area!
    $productDataAreasDom = $dom->find("SPAN[id=prodDataArea]");
    $productDataDom = $productDataAreasDom[0];
    //print $productData . "\n"; 
    
    $data = array();
    
    // Loop over each row in the product data.
    foreach ($productDataDom->find("tr") as $tr)
    {
        // Get the columns for this row of info.
        $columns = $tr->find("td");
    
        $attribute = $columns[0]->plaintext;
        $value = intval($columns[1]->plaintext);    
    
        // Some rows are empty, and we should exclude them.
        if (strlen($attribute) > 0)
        {
            //print $attribute . ": ";
            //print $value . "\n";
            $data["id"] = $productId;
            $data[$attribute] = $value;
        }
    }

    // Get the price.
    $priceDom = $dom->find("td[background*=add_cart_bgd02.jpg]");
    $price = floatval(str_replace('$', "", $priceDom[0]->plaintext));
    $data["price"] = $price;

    // Calculate out a few extra fields:
    $cells = $data["Config(s)"];
    $capacity = $data["Capacity(mAh)"];
    $energy = $cells * 3.7 * $capacity / 1000;
    $value = $energy / $price;

    $data["Energy (Wh)"] = $energy;
    $data["Value (Wh/$)"] = $value;

    //print_r($data);
    scraperwiki::save(array("id"), $data);
    scraperwiki::save_var("currentId", $productId);
    $loopCount++;
}

// Check to see if we have scraped everything - if so, start again!
$lastBattery = end($batteries);
if($lastBattery['id'] == $productId)
{
    print "All known batteries processed. Clearing progress marker so scraper can start again.";
    scraperwiki::save_var("currentId", -1);
}
?>
<?php
require 'scraperwiki/simple_html_dom.php'; 

$startProductId = scraperwiki::get_var("currentId", -1);

if($startProductId == -1)
{
    print "No previous saved position found. Starting from scratch.";
}
else
{
    print "Resuming from product id $startProductId\n";
}

scraperwiki::attach("hobbyking_batteryidlist");
$batteries = scraperwiki::select("id from hobbyking_batteryidlist.swdata where id > $startProductId order by id asc");
$remainingCount = count($batteries);

print "Found $remainingCount batteries left to be scraped.";

$maxPerRun = 100;
$loopCount = 0;

foreach($batteries as $bat)
{
    if ($loopCount > $maxPerRun)
    {
        print "Ending run after $maxPerRun iterations.";
        break;
    }

    $productId = $bat['id'];
    print "Retrieving " . $productId . "\n";
    $html = scraperWiki::scrape("http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$productId");
    //print $html . "\n";
    
    $dom = new simple_html_dom(); 
    $dom->load($html); 
    
    // Get the product data (located in a span tag). Should only be one product data area!
    $productDataAreasDom = $dom->find("SPAN[id=prodDataArea]");
    $productDataDom = $productDataAreasDom[0];
    //print $productData . "\n"; 
    
    $data = array();
    
    // Loop over each row in the product data.
    foreach ($productDataDom->find("tr") as $tr)
    {
        // Get the columns for this row of info.
        $columns = $tr->find("td");
    
        $attribute = $columns[0]->plaintext;
        $value = intval($columns[1]->plaintext);    
    
        // Some rows are empty, and we should exclude them.
        if (strlen($attribute) > 0)
        {
            //print $attribute . ": ";
            //print $value . "\n";
            $data["id"] = $productId;
            $data[$attribute] = $value;
        }
    }

    // Get the price.
    $priceDom = $dom->find("td[background*=add_cart_bgd02.jpg]");
    $price = floatval(str_replace('$', "", $priceDom[0]->plaintext));
    $data["price"] = $price;

    // Calculate out a few extra fields:
    $cells = $data["Config(s)"];
    $capacity = $data["Capacity(mAh)"];
    $energy = $cells * 3.7 * $capacity / 1000;
    $value = $energy / $price;

    $data["Energy (Wh)"] = $energy;
    $data["Value (Wh/$)"] = $value;

    //print_r($data);
    scraperwiki::save(array("id"), $data);
    scraperwiki::save_var("currentId", $productId);
    $loopCount++;
}

// Check to see if we have scraped everything - if so, start again!
$lastBattery = end($batteries);
if($lastBattery['id'] == $productId)
{
    print "All known batteries processed. Clearing progress marker so scraper can start again.";
    scraperwiki::save_var("currentId", -1);
}
?>

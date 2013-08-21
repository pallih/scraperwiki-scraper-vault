<?php
require 'scraperwiki/simple_html_dom.php';
$maxCells = 6;
$minCapacity = 0;
$maxCapacity = 99999;

for ($cells = 1; $cells <= $maxCells; $cells++)
{
    print "Retrieving Lipo list for $cells cells\n";
    
    $url = "http://www.hobbyking.com/hobbyking/store/lithium_polymer_battery_configuration.asp?con=$cells&cap1=$minCapacity&cap2=$maxCapacity&location=INT";
    
    $html = scraperWiki::scrape($url);
    //print $html . "\n";
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // Get table of batteries:
    // Each row contains the following (amongst other stuff too):
    // <SPAN id="tst11895" onClick="toggle(11895)" style="cursor:pointer">+</SPAN>
    // Where the 11895 is the product Id we are looking for.
    // So look for span tags that contain 'tst' in the id attribute.
    $batteriesTableDom = $dom->find("span[id*=tst]");
    
    foreach ($batteriesTableDom as $data)
    {
        $id = intval(str_replace("tst", "", $data->id));
        scraperwiki::save(array("id"), array( "id" => $id, "cells" => $cells));
        //print $id . "\n";
    }
}
?><?php
require 'scraperwiki/simple_html_dom.php';
$maxCells = 6;
$minCapacity = 0;
$maxCapacity = 99999;

for ($cells = 1; $cells <= $maxCells; $cells++)
{
    print "Retrieving Lipo list for $cells cells\n";
    
    $url = "http://www.hobbyking.com/hobbyking/store/lithium_polymer_battery_configuration.asp?con=$cells&cap1=$minCapacity&cap2=$maxCapacity&location=INT";
    
    $html = scraperWiki::scrape($url);
    //print $html . "\n";
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    // Get table of batteries:
    // Each row contains the following (amongst other stuff too):
    // <SPAN id="tst11895" onClick="toggle(11895)" style="cursor:pointer">+</SPAN>
    // Where the 11895 is the product Id we are looking for.
    // So look for span tags that contain 'tst' in the id attribute.
    $batteriesTableDom = $dom->find("span[id*=tst]");
    
    foreach ($batteriesTableDom as $data)
    {
        $id = intval(str_replace("tst", "", $data->id));
        scraperwiki::save(array("id"), array( "id" => $id, "cells" => $cells));
        //print $id . "\n";
    }
}
?>
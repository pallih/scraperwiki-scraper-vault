<?php

$baseurl = "http://www.socmachemicaldirectory.com/advanced-search/results/taxonomy%3A3162";
$pages[] = $baseurl;

//get pharma companies
 $original_file = file_get_contents("$baseurl");
 $stripped_file = strip_tags($original_file, "<a>");
  preg_match_all("/<a(?:[^>]*)href=\"([^\"]*)\"(?:[^>]*)>(?:[^<]*)<\/a>/is", $stripped_file, $matches);

//extract pages
foreach ($matches[1] as $key=>$value)
{
    if (strstr($value,"?page="))
        {$searchpages[]="http://www.socmachemicaldirectory.com".$value;}
}
#array_unique($searchpages);
array_pop($searchpages);
array_pop($searchpages);
#print_r($searchpages);


//get company page list
foreach ($searchpages as $searchpage)
{
    $original_file = file_get_contents("$searchpage");
    $stripped_file = strip_tags($original_file, "<a>");
    preg_match_all("/<a(?:[^>]*)href=\"([^\"]*)\"(?:[^>]*)>(?:[^<]*)<\/a>/is", $stripped_file, $matches);

    //extract pages
    foreach ($matches[1] as $key=>$value)
    {
        if (strstr($value,"/company/"))
            {$companypages[]=$value;}
    }
}
#print_r($companypages);
foreach ($companypages as $key=>$value)
{
$html = file_get_contents($value);
$dom = new DomDocument();
$dom->loadHtml($html);
$xpath = new DomXpath($dom);
$companies[$key]['name'] = trim($xpath->query('//*[@id="or-name"]')->item(0)->nodeValue);
$companies[$key]['title']= trim($xpath->query('//*[@id="or-job-title"]')->item(0)->nodeValue);
#$companies[$key]['company']= $xpath->query('//*[@title]')->item(0);
$companies[$key]['company']= ucwords(str_replace('-',' ',(substr($value,strrpos($value,'/')+1))));
$companies[$key]['address']= trim($xpath->query('//*[@class="street-address"]')->item(0)->nodeValue);
$companies[$key]['city']= trim($xpath->query('//*[@class="locality"]')->item(0)->nodeValue);
$companies[$key]['state']= trim($xpath->query('//*[@class="region"]')->item(0)->nodeValue);
$companies[$key]['zip']= trim($xpath->query('//*[@class="postal-code"]')->item(0)->nodeValue);
$companies[$key]['country']= trim($xpath->query('//*[@class="country-name"]')->item(0)->nodeValue);

}



foreach ($companies as $value)
{
    scraperwiki::save(array('name','title','company','address','city','state','zip','country'),$value);
    echo implode(',', $value) . PHP_EOL;
}

#echo "<pre>";
#print_r($companies);
#echo "</pre>";
?><?php

$baseurl = "http://www.socmachemicaldirectory.com/advanced-search/results/taxonomy%3A3162";
$pages[] = $baseurl;

//get pharma companies
 $original_file = file_get_contents("$baseurl");
 $stripped_file = strip_tags($original_file, "<a>");
  preg_match_all("/<a(?:[^>]*)href=\"([^\"]*)\"(?:[^>]*)>(?:[^<]*)<\/a>/is", $stripped_file, $matches);

//extract pages
foreach ($matches[1] as $key=>$value)
{
    if (strstr($value,"?page="))
        {$searchpages[]="http://www.socmachemicaldirectory.com".$value;}
}
#array_unique($searchpages);
array_pop($searchpages);
array_pop($searchpages);
#print_r($searchpages);


//get company page list
foreach ($searchpages as $searchpage)
{
    $original_file = file_get_contents("$searchpage");
    $stripped_file = strip_tags($original_file, "<a>");
    preg_match_all("/<a(?:[^>]*)href=\"([^\"]*)\"(?:[^>]*)>(?:[^<]*)<\/a>/is", $stripped_file, $matches);

    //extract pages
    foreach ($matches[1] as $key=>$value)
    {
        if (strstr($value,"/company/"))
            {$companypages[]=$value;}
    }
}
#print_r($companypages);
foreach ($companypages as $key=>$value)
{
$html = file_get_contents($value);
$dom = new DomDocument();
$dom->loadHtml($html);
$xpath = new DomXpath($dom);
$companies[$key]['name'] = trim($xpath->query('//*[@id="or-name"]')->item(0)->nodeValue);
$companies[$key]['title']= trim($xpath->query('//*[@id="or-job-title"]')->item(0)->nodeValue);
#$companies[$key]['company']= $xpath->query('//*[@title]')->item(0);
$companies[$key]['company']= ucwords(str_replace('-',' ',(substr($value,strrpos($value,'/')+1))));
$companies[$key]['address']= trim($xpath->query('//*[@class="street-address"]')->item(0)->nodeValue);
$companies[$key]['city']= trim($xpath->query('//*[@class="locality"]')->item(0)->nodeValue);
$companies[$key]['state']= trim($xpath->query('//*[@class="region"]')->item(0)->nodeValue);
$companies[$key]['zip']= trim($xpath->query('//*[@class="postal-code"]')->item(0)->nodeValue);
$companies[$key]['country']= trim($xpath->query('//*[@class="country-name"]')->item(0)->nodeValue);

}



foreach ($companies as $value)
{
    scraperwiki::save(array('name','title','company','address','city','state','zip','country'),$value);
    echo implode(',', $value) . PHP_EOL;
}

#echo "<pre>";
#print_r($companies);
#echo "</pre>";
?>
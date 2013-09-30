<?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page
for ($pn = 0000064; $pn < 0001000; $pn++) 
{
$url = "http://www.imdb.com/title/tt".$pn."/";
$html = scraperwiki::scrape($url);
//print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td[id=overview-top]') as $data)
{
     $i = 0;  
    foreach($data->find('h1,.infobar,div[class=star-box-details],.txt-block') as $m_name)
    {

    $m_data[$i]= $m_name->plaintext;  
    //echo $i."   ".$m_name->plaintext . "\n" ;          
    $i++;
     }
 $record = array('murl'=>$url,'mname'=>$m_data[0],'minfo'=>$m_data[1],'mrating'=>$m_data[2],'mdirector'=>$m_data[3],'mstar'=>$m_data[4]);
            //print_r($record);
$m_data = "";
 scraperwiki::save_sqlite(array("murl","mname","minfo","mrating","mdirector","mstar"),$record,"movdb");
    //print $data->plaintext . "\n";
   
}
}

?>

<?php
require  'scraperwiki/simple_html_dom.php';
# Welcome to the second ScraperWiki PHP tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page
for ($pn = 0000064; $pn < 0001000; $pn++) 
{
$url = "http://www.imdb.com/title/tt".$pn."/";
$html = scraperwiki::scrape($url);
//print $html;

# Next we use the PHP Simple HTML DOM Parser to extract the values from the HTML 
# source. Uncomment the next six lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('td[id=overview-top]') as $data)
{
     $i = 0;  
    foreach($data->find('h1,.infobar,div[class=star-box-details],.txt-block') as $m_name)
    {

    $m_data[$i]= $m_name->plaintext;  
    //echo $i."   ".$m_name->plaintext . "\n" ;          
    $i++;
     }
 $record = array('murl'=>$url,'mname'=>$m_data[0],'minfo'=>$m_data[1],'mrating'=>$m_data[2],'mdirector'=>$m_data[3],'mstar'=>$m_data[4]);
            //print_r($record);
$m_data = "";
 scraperwiki::save_sqlite(array("murl","mname","minfo","mrating","mdirector","mstar"),$record,"movdb");
    //print $data->plaintext . "\n";
   
}
}

?>


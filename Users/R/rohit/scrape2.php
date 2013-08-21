<?php
ini_set('display_errors', '1');
    ini_set('log_errors', 1);
    ini_set('error_log', dirname(__FILE__) . '/error_log.txt');
    error_reporting(E_ALL);
require 'scraperwiki/simple_html_dom.php';
echo $s_time=time();
$html2 = file_get_html('http://www.flipkart.com/search/a/books?query=Patternmaking+For+Fashion+Design+And+DVD+Package&vertical=books&dd=0&autosuggest[as]=off&autosuggest[as-submittype]=entered&autosuggest[as-grouprank]=0&autosuggest[as-overallrank]=0&Search=%20&_r=0h9MLtw6hndyakNsI8DCuw--&_l=MHzwajeMCXBPHY1KaGPeZQ--&ref=0d21b9f5-faac-4f71-9010-1deb8069712a&selmitem=');
if(isset($html2))
echo "successful";
else echo "not successful";
$html3=$html2->find('div[class=fk-srch-item fk-inf-scroll-item]');
if(!empty($html3))
echo "successful";
else echo "not successful";
echo count($html3);
/*oreach($html3 as $text)
{
    for($i=1;$i<=2;$i++)
    {
        echo $text->plaintext;
        echo "<br>";
        $text=$text->next_sibling();
    }
    echo "<br>"."<br>";
}*/

echo $f_time=time();
echo "<br>";
echo "time_inv=".($f_time-$s_time);

?>



<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.ossieindoor.com.au/tuesday");
//print $html;

$dom = new simple_html_dom();
$dom->load($html);
//print $dom;

$date_match = array(); 
$date = '';

$time_match = array(); 
$current_time = '';
$timeWAVD = '';
$timeDIGGY = '';

foreach ($dom->find('a[href]') as $element)
{
    //if( preg_match( '/\b\w+,\s\d\d?\s\w+\s\d\d\d\d/', $element->plaintext, $date_match))
    //if( preg_match( '/\b\w+\b\sFixtures\s\d\d?\/\d\d\/\d\d/', $element->plaintext, $date_match))
    if( preg_match( '/\b\w+\b\sFixtures\s(\d\d?\/\d\d\/\d\d)/', $element->plaintext, $date_match))
    {
        $date = $date_match[1];
        break;
    }
}

foreach ($dom->find('span[data-scayt_word]') as $element)
{
    //print $element->plaintext;
    //print "\n";

    if( preg_match( '/\d\.\d\dpm/', $element->plaintext, $time_match))
    {
        //print $current_time;
        $current_time = $time_match[0];
    }

    if( preg_match('/WAVD/', $element->plaintext))
    {
        $timeWAVD = $current_time;
    }

    if( preg_match('/DIGGY/', $element->plaintext))
    {
        $timeDIGGY = $current_time;
    }
}

echo "${date}\n";
echo "WAVD @ ${timeWAVD}\n";
echo "GETTIN DIGGY @ ${timeDIGGY}\n";

//scraperwiki::save_sqlite(array("data"),array("data"=>"WAVD", "date"=>$date, "time"=>$time));

scraperwiki::save_var("date", $date);
scraperwiki::save_var("timeWAVD", $timeWAVD);
scraperwiki::save_var("timeDIGGY", $timeDIGGY);


?>
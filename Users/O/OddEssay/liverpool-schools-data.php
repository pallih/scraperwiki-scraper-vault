<?php
require  'scraperwiki/simple_html_dom.php';
# Edit this line to the region of your choice (Or develop another loop at the previous page and scrape all regions!)
$html = scraperwiki::scrape('http://www.dcsf.gov.uk/cgi-bin/performancetables/group_09.pl?Mode=Z&Type=LA&Begin=s&No=341&Base=b&Phase=1&F=1&L=50&Year=09');
echo $html;
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('tr') as $data)
{
    ++$c;
    echo $c.' ';
    $school = $data->children(0);
    $link = $school->children(0);
      if($link->href)
      {
        $url = str_replace('&amp;','&','http://www.dcsf.gov.uk'.$link->href);
        echo 'Trying '.$url;
        $schoolDetailHtml = scraperwiki::scrape($url);
          echo $schoolDetailHtml;
        $schoolDetail = new simple_html_dom();
        $schoolDetail->load($schoolDetailHtml);
    
        $content = $schoolDetail->find('dl');
        $address = $content[0]->find('dd');;
        $splitAddress = explode('<br />',$address[0]->innertext);
        $postcode = $splitAddress[count($splitAddress) - 2]; // Post code is in the second to last element;
          
        $schoolStatsList = $schoolDetail->find('dl.schoolsstatslist',0);
        $totalNumberOfPupilsAllAges = $schoolStatsList->find('dd',0)->plaintext;
        $totalNumberOfPupilsWithSENSupportedAtSchoolAction = $schoolStatsList->find('dd',1)->plaintext;
        
        
        scraperwiki::save(
            array
            (
                'name',
                'postcode',
                'totalNumberOfPupilsAllAges',
                'totalNumberOfPupilsWithSENSupportedAtSchoolAction'
            ),
            array
            (
                'name' => $school->plaintext,
                'postcode' => $postcode,
                'totalNumberOfPupilsAllAges' => $totalNumberOfPupilsAllAges,
                'totalNumberOfPupilsWithSENSupportedAtSchoolAction' => $totalNumberOfPupilsWithSENSupportedAtSchoolAction
            )
        );
    }
    echo "\n";
} 
?><?php
require  'scraperwiki/simple_html_dom.php';
# Edit this line to the region of your choice (Or develop another loop at the previous page and scrape all regions!)
$html = scraperwiki::scrape('http://www.dcsf.gov.uk/cgi-bin/performancetables/group_09.pl?Mode=Z&Type=LA&Begin=s&No=341&Base=b&Phase=1&F=1&L=50&Year=09');
echo $html;
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('tr') as $data)
{
    ++$c;
    echo $c.' ';
    $school = $data->children(0);
    $link = $school->children(0);
      if($link->href)
      {
        $url = str_replace('&amp;','&','http://www.dcsf.gov.uk'.$link->href);
        echo 'Trying '.$url;
        $schoolDetailHtml = scraperwiki::scrape($url);
          echo $schoolDetailHtml;
        $schoolDetail = new simple_html_dom();
        $schoolDetail->load($schoolDetailHtml);
    
        $content = $schoolDetail->find('dl');
        $address = $content[0]->find('dd');;
        $splitAddress = explode('<br />',$address[0]->innertext);
        $postcode = $splitAddress[count($splitAddress) - 2]; // Post code is in the second to last element;
          
        $schoolStatsList = $schoolDetail->find('dl.schoolsstatslist',0);
        $totalNumberOfPupilsAllAges = $schoolStatsList->find('dd',0)->plaintext;
        $totalNumberOfPupilsWithSENSupportedAtSchoolAction = $schoolStatsList->find('dd',1)->plaintext;
        
        
        scraperwiki::save(
            array
            (
                'name',
                'postcode',
                'totalNumberOfPupilsAllAges',
                'totalNumberOfPupilsWithSENSupportedAtSchoolAction'
            ),
            array
            (
                'name' => $school->plaintext,
                'postcode' => $postcode,
                'totalNumberOfPupilsAllAges' => $totalNumberOfPupilsAllAges,
                'totalNumberOfPupilsWithSENSupportedAtSchoolAction' => $totalNumberOfPupilsWithSENSupportedAtSchoolAction
            )
        );
    }
    echo "\n";
} 
?>
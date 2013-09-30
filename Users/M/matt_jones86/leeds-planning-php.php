<?php
require  'scraperwiki/simple_html_dom.php';
# $html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");
# print $html;
    
#$dom = new simple_html_dom();
#$dom->load($html);
#foreach($dom->find('td') as $data)
#{
#    print $data->plaintext . "\n";
#}

    
function convDate($d)
{
    return date('Y-m-d', strtotime($d));
}
       
function mainDate($sDate)
{
    $lDateStart = date('d/m/Y', strtotime($sDate));
    $lDateEnd = $lDateStart;
    
    //create array of data to be posted
    # $postData['searchCriteria.ward'] = 'HORSFN';
    $postData['searchType'] = 'Application';
    $postData['dates(applicationValidatedStart)'] = $lDateStart;
    $postData['dates(applicationValidatedEnd)'] = $lDateEnd;
    
    print "LDATE START=".$lDateStart;

    //traverse array and prepare data for posting (key1=value1)
    foreach ( $postData as $key => $value) {
        $postItems[] = $key . '=' . $value;
    }

    //create the final string to be posted using implode()
    $postString = implode ('&', $postItems);
    
    $url = "https://publicaccess.leeds.gov.uk/online-applications/advancedSearchResults.do?action=firstPage";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
    curl_setopt($ch, CURLOPT_USERAGENT,
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);

    //set data to be posted
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);

    //perform our request
    $result = curl_exec($ch);   
    
    # print_r(curl_getinfo($curl_connection));
    # echo curl_errno($curl_connection) . '-' . curl_error($curl_connection);
    
    //close the connection
    curl_close($ch);

    echo $result;
    
}    

function begin()
{
    $dateFrom = scraperwiki::get_metadata("datefrom", "1980-01-01");
    $dateTo = scraperwiki::get_metadata("dateto", "1980-01-01");   
        
    $dayFrom = $dateFrom;
    $dayTo = $dateTo;

    for ($i=1 ; $i<=1; $i++)
    {
        $nextDay = mktime(0, 0, 0, date("m", strtotime($dayFrom)), date("d", strtotime($dayFrom))+1, date("y", strtotime($dayFrom)));
        $dayFrom = date('Y-m-d', $nextDay);
        mainDate($dayFrom);
        scraperwiki::save_metadata("datefrom", date('Y-m-d', strtotime($dayFrom)));
        scraperwiki::save_metadata("dateto", date('Y-m-d', strtotime($dayTo)));
    }
}
    
begin();
?>
<?php
require  'scraperwiki/simple_html_dom.php';
# $html = scraperwiki::scrape("http://scraperwiki.com/hello_world.html");
# print $html;
    
#$dom = new simple_html_dom();
#$dom->load($html);
#foreach($dom->find('td') as $data)
#{
#    print $data->plaintext . "\n";
#}

    
function convDate($d)
{
    return date('Y-m-d', strtotime($d));
}
       
function mainDate($sDate)
{
    $lDateStart = date('d/m/Y', strtotime($sDate));
    $lDateEnd = $lDateStart;
    
    //create array of data to be posted
    # $postData['searchCriteria.ward'] = 'HORSFN';
    $postData['searchType'] = 'Application';
    $postData['dates(applicationValidatedStart)'] = $lDateStart;
    $postData['dates(applicationValidatedEnd)'] = $lDateEnd;
    
    print "LDATE START=".$lDateStart;

    //traverse array and prepare data for posting (key1=value1)
    foreach ( $postData as $key => $value) {
        $postItems[] = $key . '=' . $value;
    }

    //create the final string to be posted using implode()
    $postString = implode ('&', $postItems);
    
    $url = "https://publicaccess.leeds.gov.uk/online-applications/advancedSearchResults.do?action=firstPage";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
    curl_setopt($ch, CURLOPT_USERAGENT,
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);

    //set data to be posted
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postString);

    //perform our request
    $result = curl_exec($ch);   
    
    # print_r(curl_getinfo($curl_connection));
    # echo curl_errno($curl_connection) . '-' . curl_error($curl_connection);
    
    //close the connection
    curl_close($ch);

    echo $result;
    
}    

function begin()
{
    $dateFrom = scraperwiki::get_metadata("datefrom", "1980-01-01");
    $dateTo = scraperwiki::get_metadata("dateto", "1980-01-01");   
        
    $dayFrom = $dateFrom;
    $dayTo = $dateTo;

    for ($i=1 ; $i<=1; $i++)
    {
        $nextDay = mktime(0, 0, 0, date("m", strtotime($dayFrom)), date("d", strtotime($dayFrom))+1, date("y", strtotime($dayFrom)));
        $dayFrom = date('Y-m-d', $nextDay);
        mainDate($dayFrom);
        scraperwiki::save_metadata("datefrom", date('Y-m-d', strtotime($dayFrom)));
        scraperwiki::save_metadata("dateto", date('Y-m-d', strtotime($dayTo)));
    }
}
    
begin();
?>

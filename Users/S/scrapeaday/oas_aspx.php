<?php
require  'scraperwiki/simple_html_dom.php';



for($year = 2012; $year <= 2015; $year++)
{
    for($month = 1; $month <= 12; $month++)
    {
        if($year == 2012 && $month < 10)
        {
        continue;    
        }
        $post_string2 = 'RadCalendar1_SD=%5B%5B
        2012%2C10%2C22%5D%2C%5B
        '.$year.'%2C'.$month.'%2C1%5D%2C%5B
        '.$year.'%2C'.$month.'%2C2%5D%2C%5B
        '.$year.'%2C'.$month.'%2C3%5D%2C%5B
        '.$year.'%2C'.$month.'%2C4%5D%2C%5B
        '.$year.'%2C'.$month.'%2C5%5D%2C%5B
        '.$year.'%2C'.$month.'%2C6%5D%2C%5B
        '.$year.'%2C'.$month.'%2C7%5D%2C%5B
        '.$year.'%2C'.$month.'%2C8%5D%2C%5B
        '.$year.'%2C'.$month.'%2C9%5D%2C%5B
        '.$year.'%2C'.$month.'%2C10%5D%2C%5B
        '.$year.'%2C'.$month.'%2C11%5D%2C%5B
        '.$year.'%2C'.$month.'%2C12%5D%2C%5B
        '.$year.'%2C'.$month.'%2C13%5D%2C%5B
        '.$year.'%2C'.$month.'%2C14%5D%2C%5B
        '.$year.'%2C'.$month.'%2C15%5D%2C%5B
        '.$year.'%2C'.$month.'%2C16%5D%2C%5B
        '.$year.'%2C'.$month.'%2C17%5D%2C%5B
        '.$year.'%2C'.$month.'%2C18%5D%2C%5B
        '.$year.'%2C'.$month.'%2C19%5D%2C%5B
        '.$year.'%2C'.$month.'%2C20%5D%2C%5B
        '.$year.'%2C'.$month.'%2C21%5D%2C%5B
        '.$year.'%2C'.$month.'%2C22%5D%2C%5B
        '.$year.'%2C'.$month.'%2C23%5D%2C%5B
        '.$year.'%2C'.$month.'%2C24%5D%2C%5B
        '.$year.'%2C'.$month.'%2C25%5D%2C%5B
        '.$year.'%2C'.$month.'%2C26%5D%2C%5B
        '.$year.'%2C'.$month.'%2C27%5D%2C%5B
        '.$year.'%2C'.$month.'%2C28%5D%2C%5B
        '.$year.'%2C'.$month.'%2C29%5D%2C%5B
        '.$year.'%2C'.$month.'%2C30%5D%5D
        
        &RadCalendar1_AD=%5B%5B
        1980%2C1%2C1%5D%2C%5B
        2099%2C12%2C30%5D%2C%5B
        '.$year.'%2C'.$month.'%2C1%5D%5D
        
        &Agenda_ClientState=&RadAJAXControlID=ctl02';
        
$post_string = $post_string1 . $post_string2;


$ch = curl_init();
curl_setopt ($ch, CURLOPT_URL, 'http://www.apps.oas.org/oasmeetings/default.aspx?Lang=EN');
curl_setopt ($ch, CURLOPT_HEADER, 0);

curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1) ;
$contents = curl_exec ($ch);
curl_close ($ch);

echo $contents;

$dom->load($contents);

$arr = array();
foreach ($dom->find('td') as $td)
    array_push($arr, $td->plaintext);

?>
<?php
require  'scraperwiki/simple_html_dom.php';



for($year = 2012; $year <= 2015; $year++)
{
    for($month = 1; $month <= 12; $month++)
    {
        if($year == 2012 && $month < 10)
        {
        continue;    
        }
        $post_string2 = 'RadCalendar1_SD=%5B%5B
        2012%2C10%2C22%5D%2C%5B
        '.$year.'%2C'.$month.'%2C1%5D%2C%5B
        '.$year.'%2C'.$month.'%2C2%5D%2C%5B
        '.$year.'%2C'.$month.'%2C3%5D%2C%5B
        '.$year.'%2C'.$month.'%2C4%5D%2C%5B
        '.$year.'%2C'.$month.'%2C5%5D%2C%5B
        '.$year.'%2C'.$month.'%2C6%5D%2C%5B
        '.$year.'%2C'.$month.'%2C7%5D%2C%5B
        '.$year.'%2C'.$month.'%2C8%5D%2C%5B
        '.$year.'%2C'.$month.'%2C9%5D%2C%5B
        '.$year.'%2C'.$month.'%2C10%5D%2C%5B
        '.$year.'%2C'.$month.'%2C11%5D%2C%5B
        '.$year.'%2C'.$month.'%2C12%5D%2C%5B
        '.$year.'%2C'.$month.'%2C13%5D%2C%5B
        '.$year.'%2C'.$month.'%2C14%5D%2C%5B
        '.$year.'%2C'.$month.'%2C15%5D%2C%5B
        '.$year.'%2C'.$month.'%2C16%5D%2C%5B
        '.$year.'%2C'.$month.'%2C17%5D%2C%5B
        '.$year.'%2C'.$month.'%2C18%5D%2C%5B
        '.$year.'%2C'.$month.'%2C19%5D%2C%5B
        '.$year.'%2C'.$month.'%2C20%5D%2C%5B
        '.$year.'%2C'.$month.'%2C21%5D%2C%5B
        '.$year.'%2C'.$month.'%2C22%5D%2C%5B
        '.$year.'%2C'.$month.'%2C23%5D%2C%5B
        '.$year.'%2C'.$month.'%2C24%5D%2C%5B
        '.$year.'%2C'.$month.'%2C25%5D%2C%5B
        '.$year.'%2C'.$month.'%2C26%5D%2C%5B
        '.$year.'%2C'.$month.'%2C27%5D%2C%5B
        '.$year.'%2C'.$month.'%2C28%5D%2C%5B
        '.$year.'%2C'.$month.'%2C29%5D%2C%5B
        '.$year.'%2C'.$month.'%2C30%5D%5D
        
        &RadCalendar1_AD=%5B%5B
        1980%2C1%2C1%5D%2C%5B
        2099%2C12%2C30%5D%2C%5B
        '.$year.'%2C'.$month.'%2C1%5D%5D
        
        &Agenda_ClientState=&RadAJAXControlID=ctl02';
        
$post_string = $post_string1 . $post_string2;


$ch = curl_init();
curl_setopt ($ch, CURLOPT_URL, 'http://www.apps.oas.org/oasmeetings/default.aspx?Lang=EN');
curl_setopt ($ch, CURLOPT_HEADER, 0);

curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1) ;
$contents = curl_exec ($ch);
curl_close ($ch);

echo $contents;

$dom->load($contents);

$arr = array();
foreach ($dom->find('td') as $td)
    array_push($arr, $td->plaintext);

?>

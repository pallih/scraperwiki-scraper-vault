<?php
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();

for ($i=3000; $i <= 9999; $i++){
$page_URL = "http://www.utsu.ca/club/clubslist.php?id=".$i;
$html = scraperWiki::scrape($page_URL);       
//print $html . "\n";

$dom->load($html);

$Club_Name = "";
$Short_Form = "";
$Campus = "";
$Group_Type = "";
$Website = "";
$Description = "";
$Email = "";
$Contact = "";
$Phone_Number ="";



    foreach($dom->find("tr") as $tr)
    {
    $tdArr = array(); 
        foreach ($tr->find('td') as $tds)
        {
           // $key = 0;
             array_push($tdArr , $tds->plaintext );
          //  if (count($tdArr) > 1)
           // {
                $key = $tdArr[0];
                $key = str_replace(":","", str_replace (" ","_", trim($key)));
                if (count($tdArr) > 1){
                    $value = $tdArr[1];
                }
          
    }
        switch ($key) {
            case 'Club_Name':
            if (count($tdArr) > 1){
//                echo $key."-Club_Name:".$value;
                $Club_Name= $value;
            }
            break;
            case 'Short_Form':
//                echo "Short_Form:".$value;
                $Short_Form = $value;
                break;
            case 'Campus':
//                echo "Campus:".$value;
                $Campus= $value;
                break;
            case 'Group_Type':
//                echo "Group_Type:".$value;
                $Group_Type = $value;
                break;
            case 'Website':
                echo "Website:".$value;
                $Website = $value;
                break;
            case 'Description':
//                echo "Description:".$value;
                $Description = $value;
                break;
            case 'Phone_Number':
                echo "Phone_Number:".$value;
                $Phone_Number = $value;
                break;
            case 'Email':
//                echo "Email:".$value;
                $Email = $value;
                break;
            case 'Contact':
//                echo "Contact:".$value;
                $Contact = $value;
                break;
        }
//        print "\n";
    }

$dataArray = array(
        'page_URL' => $page_URL,
        'Club_Name' => htmlspecialchars ($Club_Name),
        'Short_Form' => htmlspecialchars ($Short_Form),
        'Campus' => htmlspecialchars ($Campus),
        'Group_Type' => htmlspecialchars ($Group_Type),
        'Description' => htmlspecialchars ($Description),
        'Phone_Number' => htmlspecialchars ($Phone_Number) ,
        'Email' => $Email,
        'Contact' => htmlspecialchars ($Contact),
        'Website' => $Website       
    );

if (strlen ( trim($dataArray['Club_Name']))>0){
 
  scraperwiki::save(array('page_URL','Club_Name','Short_Form','Campus','Group_Type','Website','Description','Email','Contact','Phone_Number'), $dataArray );
    print_r($dataArray );
    print "\n";
}else{
    print($i.'skipped' );
    print "\n";
}

}


?>
<?php
require 'scraperwiki/simple_html_dom.php';  
$dom = new simple_html_dom();

for ($i=3000; $i <= 9999; $i++){
$page_URL = "http://www.utsu.ca/club/clubslist.php?id=".$i;
$html = scraperWiki::scrape($page_URL);       
//print $html . "\n";

$dom->load($html);

$Club_Name = "";
$Short_Form = "";
$Campus = "";
$Group_Type = "";
$Website = "";
$Description = "";
$Email = "";
$Contact = "";
$Phone_Number ="";



    foreach($dom->find("tr") as $tr)
    {
    $tdArr = array(); 
        foreach ($tr->find('td') as $tds)
        {
           // $key = 0;
             array_push($tdArr , $tds->plaintext );
          //  if (count($tdArr) > 1)
           // {
                $key = $tdArr[0];
                $key = str_replace(":","", str_replace (" ","_", trim($key)));
                if (count($tdArr) > 1){
                    $value = $tdArr[1];
                }
          
    }
        switch ($key) {
            case 'Club_Name':
            if (count($tdArr) > 1){
//                echo $key."-Club_Name:".$value;
                $Club_Name= $value;
            }
            break;
            case 'Short_Form':
//                echo "Short_Form:".$value;
                $Short_Form = $value;
                break;
            case 'Campus':
//                echo "Campus:".$value;
                $Campus= $value;
                break;
            case 'Group_Type':
//                echo "Group_Type:".$value;
                $Group_Type = $value;
                break;
            case 'Website':
                echo "Website:".$value;
                $Website = $value;
                break;
            case 'Description':
//                echo "Description:".$value;
                $Description = $value;
                break;
            case 'Phone_Number':
                echo "Phone_Number:".$value;
                $Phone_Number = $value;
                break;
            case 'Email':
//                echo "Email:".$value;
                $Email = $value;
                break;
            case 'Contact':
//                echo "Contact:".$value;
                $Contact = $value;
                break;
        }
//        print "\n";
    }

$dataArray = array(
        'page_URL' => $page_URL,
        'Club_Name' => htmlspecialchars ($Club_Name),
        'Short_Form' => htmlspecialchars ($Short_Form),
        'Campus' => htmlspecialchars ($Campus),
        'Group_Type' => htmlspecialchars ($Group_Type),
        'Description' => htmlspecialchars ($Description),
        'Phone_Number' => htmlspecialchars ($Phone_Number) ,
        'Email' => $Email,
        'Contact' => htmlspecialchars ($Contact),
        'Website' => $Website       
    );

if (strlen ( trim($dataArray['Club_Name']))>0){
 
  scraperwiki::save(array('page_URL','Club_Name','Short_Form','Campus','Group_Type','Website','Description','Email','Contact','Phone_Number'), $dataArray );
    print_r($dataArray );
    print "\n";
}else{
    print($i.'skipped' );
    print "\n";
}

}


?>

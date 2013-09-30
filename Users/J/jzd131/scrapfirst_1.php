<?php

$myUrl = "https://pincushion.needle.com/profiles/";
       // echo('Chats,'. 'Sales Amount,'. 'sales,'. 'same Chat Sales,'.'free Skate Time,'.'commit Time'.'<br>');
//scraperwiki::save_sqlite(array("index"),array("index"=>0, "Chats"=>"Chats", "SalesAmount"=>"SalesAmount", "Sales"=>"Sales","sameChatSales"=>"Same Chat Sales","freeSkateTime"=>"Free Skate Time","commitTime"=>"Commit Time"));           

        
for ($i = 5438; $i <= 7300; $i++) {
    $html = file_get_contents($myUrl . $i);
    // Create new DOM object:
    $dom = new DomDocument();

    // Load HTML code:
    @$dom->loadHTML($html);

    $xpath = new DOMXPath($dom);
    
    $chats1 = $xpath->query("//td[.='Chats']/following::td");
    if ($chats1->length) {//a DOMNodelist has a length-property
        $chats = $chats1->item(0)->nodeValue;
        $salesAmount = $xpath->query("//td[.='Sales Amount']/following::td")->item(0)->nodeValue;
        $sales = $xpath->query("//td[.='Sales']/following::td")->item(0)->nodeValue;
        $sameChatSales = $xpath->query("//td[.='Same Chat Sales']/following::td")->item(0)->nodeValue;
        $freeSkateTime = $xpath->query("//td[.='Free Skate Time']/following::td")->item(0)->nodeValue;
        $commitTime = $xpath->query("//td[.='Commit Time']/following::td")->item(0)->nodeValue;
        //echo $chats. $salesAmount. $sales. $sameChatSales.$freeSkateTime.$commitTime. "<br>";
        //csv related
        // output headers so that the file is downloaded rather than displayed
        
// loop over the rows, outputting them
      // echo($chats.','. $salesAmount.','. $sales.','. $sameChatSales.','.$freeSkateTime.','.$commitTime.'<br>');
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Chats"=>$chats, "SalesAmount"=>$salesAmount, "Sales"=>$sales,"sameChatSales"=>$sameChatSales,"freeSkateTime"=>$freeSkateTime,"commitTime"=>$commitTime));

    }
    //foreach($chats as $chat)
    //{
    //  echo $chat->nodeValue;
    //}
}
?><?php

$myUrl = "https://pincushion.needle.com/profiles/";
       // echo('Chats,'. 'Sales Amount,'. 'sales,'. 'same Chat Sales,'.'free Skate Time,'.'commit Time'.'<br>');
//scraperwiki::save_sqlite(array("index"),array("index"=>0, "Chats"=>"Chats", "SalesAmount"=>"SalesAmount", "Sales"=>"Sales","sameChatSales"=>"Same Chat Sales","freeSkateTime"=>"Free Skate Time","commitTime"=>"Commit Time"));           

        
for ($i = 5438; $i <= 7300; $i++) {
    $html = file_get_contents($myUrl . $i);
    // Create new DOM object:
    $dom = new DomDocument();

    // Load HTML code:
    @$dom->loadHTML($html);

    $xpath = new DOMXPath($dom);
    
    $chats1 = $xpath->query("//td[.='Chats']/following::td");
    if ($chats1->length) {//a DOMNodelist has a length-property
        $chats = $chats1->item(0)->nodeValue;
        $salesAmount = $xpath->query("//td[.='Sales Amount']/following::td")->item(0)->nodeValue;
        $sales = $xpath->query("//td[.='Sales']/following::td")->item(0)->nodeValue;
        $sameChatSales = $xpath->query("//td[.='Same Chat Sales']/following::td")->item(0)->nodeValue;
        $freeSkateTime = $xpath->query("//td[.='Free Skate Time']/following::td")->item(0)->nodeValue;
        $commitTime = $xpath->query("//td[.='Commit Time']/following::td")->item(0)->nodeValue;
        //echo $chats. $salesAmount. $sales. $sameChatSales.$freeSkateTime.$commitTime. "<br>";
        //csv related
        // output headers so that the file is downloaded rather than displayed
        
// loop over the rows, outputting them
      // echo($chats.','. $salesAmount.','. $sales.','. $sameChatSales.','.$freeSkateTime.','.$commitTime.'<br>');
        scraperwiki::save_sqlite(array("index"),array("index"=>$i, "Chats"=>$chats, "SalesAmount"=>$salesAmount, "Sales"=>$sales,"sameChatSales"=>$sameChatSales,"freeSkateTime"=>$freeSkateTime,"commitTime"=>$commitTime));

    }
    //foreach($chats as $chat)
    //{
    //  echo $chat->nodeValue;
    //}
}
?>
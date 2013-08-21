<?php

require  'scraperwiki/simple_html_dom.php';
$baseurl ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/';
$request_url ='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/index.jsp';
 
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);   
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  
    $result = curl_exec($ch);
    curl_close($ch);
    //$regex='|<a.*?href="(.*?)"|';
    preg_match_all('|<a.*?href="(.*?)"|',$result,$parts);
    $links=$parts[1];
    foreach($links as $link){
        //echo $link."\r\n";
  //print_r($link);
        if(!strstr( $link, 'dagoverzicht.jsp')) {
         continue;
        }

 $ch2 = curl_init();
        $timeout = 5;
        curl_setopt($ch2,CURLOPT_URL,$baseurl .$link);
        curl_setopt($ch2,CURLOPT_RETURNTRANSFER,1);
        curl_setopt($ch2,CURLOPT_CONNECTTIMEOUT,$timeout);
        $result = curl_exec($ch2);
        curl_close($ch2);
 //       return $data;
       // echo $link."\r\n";
       //print 'inspected '.$link.' done'/r/n';
       // print_r($data);

   
       $ch3 = curl_init();
    curl_setopt($ch3, CURLOPT_URL,$baseurl. $link);   
    curl_setopt($ch3, CURLOPT_RETURNTRANSFER, true);  
    $result2 = curl_exec($ch3);
    curl_close($ch3);
    //echo $result2;
    preg_match_all('|<a.*?href="(.*?)"|',$result2,$newlinks);
    $newlinks=$newlinks[1];
    //echo $newlinks;
   foreach ($newlinks as $newlink) {
    if(!strstr( $newlink, 'details.jsp')) {
         continue;
        }

 $ch4 = curl_init();
        $timeout = 5;
        curl_setopt($ch4,CURLOPT_URL,$baseurl .$newlink);
        curl_setopt($ch4,CURLOPT_RETURNTRANSFER,1);
        curl_setopt($ch4,CURLOPT_CONNECTTIMEOUT,$timeout);
        $data = curl_exec($ch4);
        //echo $data;
        curl_close($ch4);
 //       return $data;
        //echo $newlink."\r\n";
       //print 'inspected '.$link.' done'/r/n';
       // print_r($data);

 

$html = scraperwiki::scrape($baseurl . $newlink);

$dom = new simple_html_dom();
$dom->load($html);


    $data=get_data($dom);
    $exp_1=preg_split("/(<div class=\"mocca\">)|(<div id=\"contact\">)/",$data);//print_r($exp_1[1]);
    $exp_2=preg_split("/<hr\/>/",$exp_1[1]);
    
    for($i=0;$i<sizeof($exp_2);$i++)
    {
        
            $exp=preg_split("/<td[^>]*>/",$exp_2[$i]);
            
            if($i==0)
            {
                $dat_type=explode("</strong>",$exp[0]);
                $dt=explode(" ",(trim(strip_tags($dat_type[0]))),2);
                $date=$dt[1];
                $type=trim(strip_tags($dat_type[1]));
            }
            else
            {
                $type=trim(strip_tags($exp[0]));
            }
            /*start time and end time*/
            $tm=explode("</b>",$exp[2]);
            $tm=trim(strip_tags($tm[0]));
            $tm_2=explode("-",$tm);
            $start_time=trim($tm_2[0]);
            $end_time=trim($tm_2[1]);
            
            if(sizeof($exp)==9 && !preg_match("/Status/",$exp[7]))
            {          
              
              $v_t=explode("</td>",$exp[8]);
              preg_match_all("/href=\"([^\"]+)\"/",$v_t[1],$link);
              $pnum=preg_split("/=|&/",$link[1][0],3);
                                  
              $location=trim(strip_tags($exp[4]));
              $soort=trim(strip_tags($exp[6]));
              $voortouwcommissie=trim(strip_tags($v_t[0]));
              $title=trim(strip_tags($v_t[1]));
              $title = mysql_real_escape_string($title);
              
              $link='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/'.$link[1][0];
              $parlisnumber=$pnum[1];
              $description=description($link);
              
              $status="confirmed";
              
                scraperwiki::save($parlisnumber);
                scraperwiki::save($location);
                scraperwiki::save($soort);
                scraperwiki::save($voortouwcommissie);
                scraperwiki::save($title);
                scraperwiki::save($link);
                scraperwiki::save($description);
                scraperwiki::save($status);              
            }
            if(sizeof($exp)==9 && preg_match("/Status/",$exp[7]))
            {          
              
              /*status and title and link and parlisnumber*/
              $s_t=explode("</td>",$exp[8]);              
              preg_match_all("/href=\"([^\"]+)\"/",$s_t[1],$link);
              $pnum=preg_split("/=|&/",$link[1][0],3);
                    
              $location="No location";
              $soort=trim(strip_tags($exp[4]));
              $voortouwcommissie=trim(strip_tags($exp[6]));
              
              $status=trim(strip_tags($s_t[0]));
              $title=trim(strip_tags($s_t[1]));
              
              $title = mysql_real_escape_string($title);
              
              $link='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/'.$link[1][0];
              $parlisnumber=$pnum[1];
              $description=description($link);          

              $obj->executeQuery("insert into tkc_wcl_info (date,start_time,end_time,location,soort,voortouwcommissie,status,title,type,link,parlisnumber,description,dateU) values('$date','$start_time','$end_time','$location','$soort','$voortouwcommissie','$status','$title','$type','$link','$parlisnumber','$description',$start_from)");
            }
            if(sizeof($exp)==7)
            {          
              
              /*voortouwcommissie and title and link and parlisnumber*/
              $v_t=explode("</td>",$exp[6]);
              preg_match_all("/href=\"([^\"]+)\"/",$v_t[1],$link);
              $pnum=preg_split("/=|&/",$link[1][0],3);
                    
              $location="No location";
              $soort=trim(strip_tags($exp[4]));
              $voortouwcommissie=trim(strip_tags($v_t[0]));
              
              $status="confirmed";
              $title=trim(strip_tags($v_t[1]));
              
              $title = mysql_real_escape_string($title);
              
              $link='http://www.tweedekamer.nl/vergaderingen/commissievergaderingen/volgende_weken/'.$link[1][0];
              $parlisnumber=$pnum[1];
              $description=description($link);     

/*$arr = array();
 foreach($dom->find('div.mocca') as $article) {
    $item['Date']     = $article->find('.left', 0)->plaintext;
    $item['Class']    = $article->find('.iconopen', 0)->plaintext;
    $item['Time'] = $article->find('td', 0)->plaintext;
    $item['Location'] = $article->find('td', 2)->plaintext;
    $item['Type'] = $article->find('td', 4)->plaintext;
    $item['Category'] = $article->find('td', 6)->plaintext;
    $item['Title'] = $article->find('td', 10)->plaintext;
    $item['Description'] = $article->find('td', 12)->plaintext;
    $articles[] = $item;
}

print_r($articles);
/*foreach ($dom->find('td,.iconopen, .left,.clear, .width:100%;') as $td)
       
    array_push($arr, $td->plaintext);

print_r($arr);


for ($i = 0; $i < count($arr); $i+=4) {
    $new[] = Array(
        'Date' => $arr[$i+0],
        'Class' => $arr[$i+1],
        'Time' => $arr[$i+3],
        'Type' => $arr[$i+5],
        'Category' => $arr[$i+7],
        'Status' => $arr[$i+9],
        'Title' => $arr[$i+10],
        //'Description' => $arr[$i+12]
    );   */ 

/*scraperwiki::save(array('Class'), $new);
scraperwiki::save(array('Date'), $new);
scraperwiki::save(array('Time'), $new);
scraperwiki::save(array('Type'), $new);
scraperwiki::save(array('Category'), $new);
scraperwiki::save(array('Status'), $new);
scraperwiki::save(array('Description'), $new);
scraperwiki::save(array('Title'), $new);
*/

  }
}

  
?>
<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$l='ABCDEFGHIJKLMNOPQRSTUVWXYZ';

$centers['name'] = array();
$centers['url'] = array();
$counter = 0;
for ($i=0; $i<strlen($l); $i++) {
    $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter='.substr($l,$i,1).'&CAT=-1&s=&TypeID=17&TestType=');
    
    preg_match_all('|<li><a href="(.*?)" title="Go to page (.*?)">.*?</a></li>|',$html,$nums);
    
    $max = array_pop($nums[2]);
    if ($max == '') { $max = 1; }
    for($p=1; $p<=$max;$p++) {
    
        $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter='.substr($l,$i,1).'&CAT=-1&page='.$p.'&TypeID=17&TestType=');


        preg_match_all('|<dt><a href="(.*?)" title="(.*?)">.*?</a></dt>|',$html,$arr);
        if (isset($arr[1][0])) {
    
            $centers['name'] = array_merge($centers['name'],$arr[2]);
            $centers['url'] = array_merge($centers['url'],$arr[1]);

        }
        
    }
}
$i=0;
foreach ($centers['url'] as $url) {
    if ($url != '') {
        $html = oneline(scraperwiki::scrape('http://www.dft.gov.uk/dsa/'.$url));
        preg_match_all('|<h3>(.*?)</h3>.*?<p>(.*?)</p><br />.*?<h3>|',$html,$a);
        $name = trim($a[1][0]);
        $address = trim(str_replace('<br />',', ',$a[2][0]));
        
        if (strstr($html,'<strong>Car</strong>')) { $car = 'YES'; } else { $car = 'NO'; }        
        if (strstr($html,'<strong>Motorcycle Module ')) { $bike = 'YES'; } else { $bike = 'NO'; }
        if (strstr($html,'<strong>Taxi</strong>')) { $taxi = 'YES'; } else { $taxi = 'NO'; }    
        if (strstr($html,'<strong>Vocational</strong>')) { $lgv = 'YES'; } else { $lgv = 'NO'; }    


        scraperwiki::save(array('id'), array('id' => ''.$counter,'name' => $name,
                                             'address' => $address,'car'=>$car,'taxi'=>$taxi
                                ,'motorcycle'=>$bike,'lgv'=>$lgv,'theory'=>'NO'));    
          $i++;
        $counter++;
    }
}

$centers['name'] = array();
$centers['url'] = array();

for ($i=0; $i<strlen($l); $i++) {

    $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/dsa_theory_test_az.asp?letter='.substr($l,$i,1).'&CAT=-1&s=&TypeID=18&TestType=');
    
    preg_match_all('|<li><a href="(.*?)" title="Go to page (.*?)">.*?</a></li>|',$html,$nums);
   
    $max = array_pop($nums[2]);
    if ($max == '') { $max = 1; }
    for($p=1; $p<=$max;$p++) {
    
        $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/dsa_theory_test_az.asp?letter='.substr($l,$i,1).'&CAT=-1&amp;page='.$p.'&TypeID=18&TestType=');


        preg_match_all('|<dt><a href="(.*?)" title="(.*?)">.*?</a></dt>|',$html,$arr);
        if (isset($arr[1][0])) {
    
            $centers['name'] = array_merge($centers['name'],$arr[2]);
            $centers['url'] = array_merge($centers['url'],$arr[1]);

        }
       
    }
}
$i=0;
foreach ($centers['url'] as $url) {
    if ($url != '') {

        $html = oneline(scraperwiki::scrape('http://www.dft.gov.uk/dsa/'.$url));
        preg_match_all('|<h3>(.*?)</h3>.*?<p>(.*?)</p><br />.*?<h3>|',$html,$a);
        $name = trim($a[1][0]);
        $address = trim(str_replace('<br />',', ',$a[2][0]));
        $address = trim(str_replace('<br>',', ',$address));

        
           


        scraperwiki::save(array('id'), array('id' => ''.$counter,'name' => $name,
                                             'address' => $address,'car'=>'NO','taxi'=>'NO'
                                ,'motorcycle'=>'NO','lgv'=>'NO','theory'=>'YES'));    
          $i++;
        $counter++;
    }
}



    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        return $code;
    }
?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$l='ABCDEFGHIJKLMNOPQRSTUVWXYZ';

$centers['name'] = array();
$centers['url'] = array();
$counter = 0;
for ($i=0; $i<strlen($l); $i++) {
    $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter='.substr($l,$i,1).'&CAT=-1&s=&TypeID=17&TestType=');
    
    preg_match_all('|<li><a href="(.*?)" title="Go to page (.*?)">.*?</a></li>|',$html,$nums);
    
    $max = array_pop($nums[2]);
    if ($max == '') { $max = 1; }
    for($p=1; $p<=$max;$p++) {
    
        $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter='.substr($l,$i,1).'&CAT=-1&page='.$p.'&TypeID=17&TestType=');


        preg_match_all('|<dt><a href="(.*?)" title="(.*?)">.*?</a></dt>|',$html,$arr);
        if (isset($arr[1][0])) {
    
            $centers['name'] = array_merge($centers['name'],$arr[2]);
            $centers['url'] = array_merge($centers['url'],$arr[1]);

        }
        
    }
}
$i=0;
foreach ($centers['url'] as $url) {
    if ($url != '') {
        $html = oneline(scraperwiki::scrape('http://www.dft.gov.uk/dsa/'.$url));
        preg_match_all('|<h3>(.*?)</h3>.*?<p>(.*?)</p><br />.*?<h3>|',$html,$a);
        $name = trim($a[1][0]);
        $address = trim(str_replace('<br />',', ',$a[2][0]));
        
        if (strstr($html,'<strong>Car</strong>')) { $car = 'YES'; } else { $car = 'NO'; }        
        if (strstr($html,'<strong>Motorcycle Module ')) { $bike = 'YES'; } else { $bike = 'NO'; }
        if (strstr($html,'<strong>Taxi</strong>')) { $taxi = 'YES'; } else { $taxi = 'NO'; }    
        if (strstr($html,'<strong>Vocational</strong>')) { $lgv = 'YES'; } else { $lgv = 'NO'; }    


        scraperwiki::save(array('id'), array('id' => ''.$counter,'name' => $name,
                                             'address' => $address,'car'=>$car,'taxi'=>$taxi
                                ,'motorcycle'=>$bike,'lgv'=>$lgv,'theory'=>'NO'));    
          $i++;
        $counter++;
    }
}

$centers['name'] = array();
$centers['url'] = array();

for ($i=0; $i<strlen($l); $i++) {

    $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/dsa_theory_test_az.asp?letter='.substr($l,$i,1).'&CAT=-1&s=&TypeID=18&TestType=');
    
    preg_match_all('|<li><a href="(.*?)" title="Go to page (.*?)">.*?</a></li>|',$html,$nums);
   
    $max = array_pop($nums[2]);
    if ($max == '') { $max = 1; }
    for($p=1; $p<=$max;$p++) {
    
        $html = scraperwiki::scrape('http://www.dft.gov.uk/dsa/dsa_theory_test_az.asp?letter='.substr($l,$i,1).'&CAT=-1&amp;page='.$p.'&TypeID=18&TestType=');


        preg_match_all('|<dt><a href="(.*?)" title="(.*?)">.*?</a></dt>|',$html,$arr);
        if (isset($arr[1][0])) {
    
            $centers['name'] = array_merge($centers['name'],$arr[2]);
            $centers['url'] = array_merge($centers['url'],$arr[1]);

        }
       
    }
}
$i=0;
foreach ($centers['url'] as $url) {
    if ($url != '') {

        $html = oneline(scraperwiki::scrape('http://www.dft.gov.uk/dsa/'.$url));
        preg_match_all('|<h3>(.*?)</h3>.*?<p>(.*?)</p><br />.*?<h3>|',$html,$a);
        $name = trim($a[1][0]);
        $address = trim(str_replace('<br />',', ',$a[2][0]));
        $address = trim(str_replace('<br>',', ',$address));

        
           


        scraperwiki::save(array('id'), array('id' => ''.$counter,'name' => $name,
                                             'address' => $address,'car'=>'NO','taxi'=>'NO'
                                ,'motorcycle'=>'NO','lgv'=>'NO','theory'=>'YES'));    
          $i++;
        $counter++;
    }
}



    function oneline($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        return $code;
    }
?>
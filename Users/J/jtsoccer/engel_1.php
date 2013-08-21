<?php
require  'scraperwiki/simple_html_dom.php';


















$p = scraperwiki::get_var('last_page'); 



for($p;$p<60850;$p++){
scraperwiki::save_var('last_page', $p);  

print($p."\n");

$name='';
 $str='';
 $nr='';
 $plz='';
 $ort='';
 $tel='';
 $web='';
 $kat='';
 $add='';
 $str_str='';

$html = scraperwiki::scrape("http://www.freizeitengel.de/Angebot/Ausflug/auswahl?p=$p");


    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);



$j=0;
foreach($dom->find('a.txt8pb') as $kat){
          # Store data in the datastore
          $kat=$kat->plaintext;
          
            if($j==4){break;}

            $j++;
      }

if($kat=='Passwort vergessen ?'){continue;}


//NAME
    foreach($dom->find('td.txt8pbm strong') as $name){
        # Store data in the datastore
             $name = $name->plaintext;
           //print $name. "\n";
            break;
        //scraperwiki::save(array('data'), array('data' => $data->plaintext));
    }


//MAIL
    foreach($dom->find('a.txt7p p.txt7p') as $web){
         # Store data in the datastore
              $web= $web->plaintext;
            //print $web. "\n";
            break;
         //scraperwiki::save(array('data'), array('data' => $data->plaintext));
     }

//STR
      $x = 0;
    foreach($dom->find('div.divframeboxlwhite form  div.divframeboxlwhitelr table.divframeboxcatnf tbody tr td.txt8p div  table.tbl-frame tbody tr td.txt8pm[colspan=2] strong') as $stra){
   # Store data in the datastore
            if($x==2){
                $str_str=$stra->plaintext;
            }
            if($x==3){
        
                $add=$stra->plaintext;
            break;
            }        
            $x++;
       }

//plz+ort
$add=explode(" ", $add);
$add_c=count($add);
$plz=$add[0];

if($add_c==2){
    $ort=$add[1];
}
elseif($add_c>2){
   for($i=1;$i<$add_c;$i++){
    $ort=$ort." ".$add[$i];
   }
}

//str+nr

$str_str=explode(" ", $str_str);
$str_str_c=count($str_str);

if($str_str_c>1){
    $nr=$str_str[$str_str_c-1];

   for($i=0;$i<$str_str_c-1;$i++){
    $str=$str." ".$str_str[$i];
   }

    
}elseif($str_str_c==1){
    $str=$str_str[0];
}

$lk1=0;
foreach($dom->find('td.txt8pm') as $tel1){
         # Store data in the datastore
              if($tel1->plaintext=='Telefon:'){break;}
                $lk1++;
     }

$lk=0;
foreach($dom->find('td.txt8pm') as $tel){
          # Store data in the datastore
               $tel= $tel->plaintext;
       if($lk==$lk1+1){break;}
            $lk++;
      }






$name=utf8_encode($name);
$str=utf8_encode($str);
 $ort=utf8_encode($ort);
  $kat=utf8_encode($kat);


scraperwiki::save(array('p', 'name','str','nr','plz','ort','tel','web','kat'), array('p' => $p ,'name' => $name ,'str' => $str, 'nr' => $nr, 'plz' => $plz, 'ort' => $ort, 'tel' => $tel, 'web' => $web, 'kat' => $kat));

}
?>

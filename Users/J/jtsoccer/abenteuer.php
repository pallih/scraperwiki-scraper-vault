<?php
require  'scraperwiki/simple_html_dom.php';
 



  
    //ÜBERSICHT
    $html1 =  scraperwiki::scrape('http://www.freizeitabenteuer.de/katalog_der_einrichtungen.html');
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

$doofBisHier = 862;


$zaehler = 0;


foreach($dom1->find('tr td h1 a') as $link){
         # Store data in the datastore
         $link=$link->href;


    print $zaehler."\n";
    if($zaehler<$doofBisHier){
        $zaehler++;
        continue;
    }
    


////////
//
//   AB HIER EINZELEINTRÄGE
//
////////



$html = scraperwiki::scrape('http://www.freizeitabenteuer.de/'.$link);
//$html = scraperwiki::scrape('http://www.freizeitabenteuer.de/regional/hessen/203/einrichtung/50er-jahre-museum-buedingen.html');
 

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);



$plz='';
$stadt='';
$web='';
$mail='';
$name='';
$tel='';
$str='';
$nr='';
$fax='';
$kat='';

//Name
foreach($dom->find('span.org') as $name1){
         # Store data in the datastore
         $name=$name1->innertext;
        //print $name."\n";
        }
$name= str_replace('\'','',$name);
$name= str_replace('\"','',$name);
$name= str_replace(',','',$name);


//web
$z = 0;
foreach($dom->find('span a') as $web1){
                $web=$web1->href;
                break;
        }

foreach($dom->find('span a') as $mail1){
                $mail=$mail1->href;
        }

//alles ab auser wichtige
$mail = str_replace('javascript:linkTo_UnCryptMailto(\'','',str_replace('\');','',$mail));


//straße
foreach($dom->find('span.street-address') as $stra){
           # Store data in the datastore
           $stra=$stra->innertext;
          }
$stra = explode(' ',$stra);
$str_c = count($stra);

if($str_c>0){
    $nr = $stra[$str_c-1];
    $str = '';
    for($st = 0; $st<$str_c-1; $st++){
        $str = $str." ".$stra[$st];
    }
}else{
    $nr = '';
    $str = $stra;   
}

//print $nr. "\n" . $str."\n" ;

//plz
foreach($dom->find('span.postal-code') as $plz){
            # Store data in the datastore
            $plz=$plz->innertext;
           }
//print $plz;

//ort
foreach($dom->find('span.country-name') as $stadt1){
             # Store data in the datastore
             $stadt=$stadt1->innertext;
            }
//tel
foreach($dom->find('span.tel') as $tel){
               # Store data in the datastore
               $tel=$tel->innertext;
              }
$tel = str_replace("Tel: ","",$tel);
//print $tel;


//fax
foreach($dom->find('span.fax') as $fax){
               # Store data in the datastore
               $fax=$fax->innertext;
              }
$fax= str_replace("Fax: ","",$fax);
//print $fax;

//kat
foreach($dom->find('div#location_single h1') as $kat){
                # Store data in the datastore
                $kat=$kat->innertext;
                //print $kat."\n";
               }
$kat= str_replace('\'','',$kat);
$kat= str_replace('\"','',$kat);
$kat= str_replace(',','',$kat);



//STRING PALACE
$str=utf8_encode($str);
$stadt=utf8_encode($stadt);
$name=utf8_encode($name);
$kat=utf8_encode($kat);

$plz=utf8_encode($plz);
$web=utf8_encode($web);
$mail=utf8_encode($mail);
$tel=utf8_encode($tel);
 $fax=utf8_encode($fax);
$nr=utf8_encode($nr);


$plz=trim($plz);
$ort=trim($stadt);
$web=trim($web);
$mail=trim($mail);
$name=trim($name);
$tel=trim($tel);
$str=trim($str);
$nr=trim($nr);
 $fax=trim($fax);
$kat=trim($kat);




scraperwiki::save(array('name','str','nr','plz','ort','tel','mail','web','kat','fax'), array('name' => $name ,'str' => $str, 'nr' => $nr, 'plz' => $plz, 'ort' => $stadt, 'tel' => $tel, 'mail' => $mail ,'web' => $web ,'kat' => $kat ,'fax' => $fax));

$zaehler++;

}

?>
<?php
require  'scraperwiki/simple_html_dom.php';
 



  
    //ÜBERSICHT
    $html1 =  scraperwiki::scrape('http://www.freizeitabenteuer.de/katalog_der_einrichtungen.html');
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

$doofBisHier = 862;


$zaehler = 0;


foreach($dom1->find('tr td h1 a') as $link){
         # Store data in the datastore
         $link=$link->href;


    print $zaehler."\n";
    if($zaehler<$doofBisHier){
        $zaehler++;
        continue;
    }
    


////////
//
//   AB HIER EINZELEINTRÄGE
//
////////



$html = scraperwiki::scrape('http://www.freizeitabenteuer.de/'.$link);
//$html = scraperwiki::scrape('http://www.freizeitabenteuer.de/regional/hessen/203/einrichtung/50er-jahre-museum-buedingen.html');
 

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);



$plz='';
$stadt='';
$web='';
$mail='';
$name='';
$tel='';
$str='';
$nr='';
$fax='';
$kat='';

//Name
foreach($dom->find('span.org') as $name1){
         # Store data in the datastore
         $name=$name1->innertext;
        //print $name."\n";
        }
$name= str_replace('\'','',$name);
$name= str_replace('\"','',$name);
$name= str_replace(',','',$name);


//web
$z = 0;
foreach($dom->find('span a') as $web1){
                $web=$web1->href;
                break;
        }

foreach($dom->find('span a') as $mail1){
                $mail=$mail1->href;
        }

//alles ab auser wichtige
$mail = str_replace('javascript:linkTo_UnCryptMailto(\'','',str_replace('\');','',$mail));


//straße
foreach($dom->find('span.street-address') as $stra){
           # Store data in the datastore
           $stra=$stra->innertext;
          }
$stra = explode(' ',$stra);
$str_c = count($stra);

if($str_c>0){
    $nr = $stra[$str_c-1];
    $str = '';
    for($st = 0; $st<$str_c-1; $st++){
        $str = $str." ".$stra[$st];
    }
}else{
    $nr = '';
    $str = $stra;   
}

//print $nr. "\n" . $str."\n" ;

//plz
foreach($dom->find('span.postal-code') as $plz){
            # Store data in the datastore
            $plz=$plz->innertext;
           }
//print $plz;

//ort
foreach($dom->find('span.country-name') as $stadt1){
             # Store data in the datastore
             $stadt=$stadt1->innertext;
            }
//tel
foreach($dom->find('span.tel') as $tel){
               # Store data in the datastore
               $tel=$tel->innertext;
              }
$tel = str_replace("Tel: ","",$tel);
//print $tel;


//fax
foreach($dom->find('span.fax') as $fax){
               # Store data in the datastore
               $fax=$fax->innertext;
              }
$fax= str_replace("Fax: ","",$fax);
//print $fax;

//kat
foreach($dom->find('div#location_single h1') as $kat){
                # Store data in the datastore
                $kat=$kat->innertext;
                //print $kat."\n";
               }
$kat= str_replace('\'','',$kat);
$kat= str_replace('\"','',$kat);
$kat= str_replace(',','',$kat);



//STRING PALACE
$str=utf8_encode($str);
$stadt=utf8_encode($stadt);
$name=utf8_encode($name);
$kat=utf8_encode($kat);

$plz=utf8_encode($plz);
$web=utf8_encode($web);
$mail=utf8_encode($mail);
$tel=utf8_encode($tel);
 $fax=utf8_encode($fax);
$nr=utf8_encode($nr);


$plz=trim($plz);
$ort=trim($stadt);
$web=trim($web);
$mail=trim($mail);
$name=trim($name);
$tel=trim($tel);
$str=trim($str);
$nr=trim($nr);
 $fax=trim($fax);
$kat=trim($kat);




scraperwiki::save(array('name','str','nr','plz','ort','tel','mail','web','kat','fax'), array('name' => $name ,'str' => $str, 'nr' => $nr, 'plz' => $plz, 'ort' => $stadt, 'tel' => $tel, 'mail' => $mail ,'web' => $web ,'kat' => $kat ,'fax' => $fax));

$zaehler++;

}

?>

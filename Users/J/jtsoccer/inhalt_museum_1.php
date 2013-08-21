<?php
require  'scraperwiki/simple_html_dom.php';

//max = 5806
for($i = 1; $i<=5806; $i++){
    print($i."\n");


    
    $html = scraperwiki::scrape("http://museum.de/mhome.php?mid=$i");
    //print $html;


    //NAME

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

   

//NAME


    foreach($dom->find('span.ueberschrift') as $name){
        # Store data in the datastore
             $name = $name->plaintext;
           //print $name. "\n";
        //scraperwiki::save(array('data'), array('data' => $data->plaintext));
    }


    //MAIL/WEB/BEIDES
        $z = 0;
        $mail='';
        $web='';

       
    foreach($dom->find('table tbody tr table tbody tr table tbody tr a[href]') as $hi){
        $z++;
       
        //wenn 2, dann beides sonst email !!ACHTUNG!!! AUCH 3 MÖGLICH
     }  
     
// print($z."\n");


//WEB/MAIL

    if($z==1){
    //EMAIL
    foreach($dom->find('table tbody tr table tbody tr table tbody tr a[href]') as $mail1){
        # Store data in the datastore
            $mail = $mail1->plaintext;
      }
    }
    

    if($z==2){

        $z2 = 1;
        foreach($dom->find('table tbody tr table tbody tr table tbody tr a[href]') as $mail1){
         # Store data in the datastore


            if($z2==1){
                $web=$mail1->plaintext; 
            }
            if($z2==2){      
                $mail=$mail1->plaintext;
                break;
            }
            $z2++; 
       }
    
    }
   



     if($z==3){

        $z2 = 1;
        foreach($dom->find('table tbody tr table tbody tr table tbody tr a[href]') as $mail1){
          # Store data in the datastore


            if($z2==2){
                $web=$mail1->plaintext;
            }
            if($z2==3){

                $mail=$mail1->plaintext;
                break;
            }
            $z2++;
 
        }
    } 
    $z=0;



//gibt es telefon?
    $tel_b = 0;

    foreach($dom->find('table td[width=55px]') as $tel1){
        # Store data in the datastore
            if($tel1->plaintext=='phone'){
                $tel_b=1;
            };
    }

    //tel existiert
    if($tel_b==1){
    
        $z_t = 1;

        foreach($dom->find('table tbody tr td table tbody tr td table tbody tr td table tbody tr td table tbody tr td ') as $tel){
            # Store data in the datastore
                if($z_t==3){
                    $tel=$tel->plaintext;
                    break;
                }
                $z_t++;
         }
    }

    //tel gibts net
    if($tel_b==0){
        $tel='';
    }






//ADDRESSE
            $a_b = 0;
        foreach($dom->find('td[colspan=2]') as $add){
            # Store data in the datastore
                  if($a_b==1){
                        $add = $add->plaintext;
                        break;
                  }
                  $a_b++;

         }
    


   // print $add."\n";

    //, teilen => 3 teile

    $teil= explode(",", $add);
    
    //bundesland = letztes
    $bundesland = $teil[2];

   // print("Bunedsland: ".$bundesland."\n");


    //erstes bei ' ' trennen => Straße
    $teil_str= explode(" ", $teil[0]);
   
    //ausgabe string
    $stra = '';

    //größe des str.
    $size_str = count($teil_str);
    



    if($size_str==2){
        $nr = $teil_str[1];
        $stra = $teil_str[0];
    
    }
    if($size_str>2){
        for($k = 0; $k < $size_str-1; $k++){
            $stra = $stra." ".$teil_str[$k];
        }
        $nr = $teil_str[$size_str-1];
    }



   //print("Nr: ".$nr."\n");
   //print("Str: ".$stra."\n");

    

//PLZ ORT

$ort= explode(" ", $teil[1]);
$gr_ort = count($ort);
$stadt='';

$zip = $ort[1];

//print("Zip: ".$zip."\n");


if($gr_ort-1==2){
    $stadt = str_replace('Kreisfrei','',$ort[2]);
}else{

    for($k=2;$k<$gr_ort-1;$k++){
        $stadt=$stadt." ".$ort[$k];
    }
    $stadt = str_replace('Kreis','',$stadt);
}

    $size_str = 0;



if($name==''&&$stadt==''&&$zip==''){
}else{

//UTF-8 draus wegen tabelle
$name=utf8_encode($name);
$stra=utf8_encode($stra);
$bundesland=utf8_encode($bundesland);

$stadt=str_replace('\n','',$stadt);
$stadt=str_replace('<br>','',$stadt);
$stadt=str_replace('<br />','',$stadt);
$stadt=str_replace(chr(13), '', $stadt);
$stadt=str_replace(chr(16), '', $stadt);
$stadt=ltrim($stadt);

 $stadt=utf8_encode($stadt);


scraperwiki::save(array('mid','name','str','nr','plz','ort','tel','mail','web','bundesland'), array('mid' => $i,'name' => $name ,'str' => $stra, 'nr' => $nr, 'plz' => $zip, 'ort' => $stadt, 'tel' => $tel, 'mail' => $mail ,'web' => $web,'bundesland' => $bundesland));


}

/*
print("name ".$name."\n");
print("plz ".$zip."\n");
print("ort ".$stadt."\n");
print("str ".$stra."\n");
print("nr ".$nr."\n");
print("mail ".$mail."\n");
print("tel ".$tel."\n");
 print("web ".$web."\n");
 print("bundesland ".$bundesland."\n");

*/

$name='';
$zip='';
$stadt='';
$stra='';
$nr='';
$mail='';
$tel='';
$web='';
$bundesland='';


}

?>

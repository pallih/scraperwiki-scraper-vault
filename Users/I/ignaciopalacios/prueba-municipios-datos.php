<?php

# Blank PHP


require 'scraperwiki/simple_html_dom.php';

    //$datos_pueblo_0 = new simple_html_dom();
      

        $html_pueblo_detalle_content = scraperwiki::scrape("http://www.lawebmunicipal.com/municipiosdeespana/municipio/_c_Yohpun483zyu3E-xQOIHor8PeX7rkj9gSijmxfrv8");

         //$html_pueblo_detalle_content = scraperwiki::scrape("http://www.lawebmunicipal.com/municipiosdeespana/municipio/_c_Yohpun48368dvL0TVsRzvgsdYwSopF");

        $html_pueblo_detalle = str_get_html($html_pueblo_detalle_content);

        $element = $html_pueblo_detalle->find('span[class="EBDSTYLE_2052]');
        $webs = $html_pueblo_detalle->find('a[class="EBDSTYLE_2052"]');
        //$mail = $html_pueblo_detalle->find('span[class="EBDSTYLE_2052] a[class="EBDSTYLE_2052"]');

        foreach($html_pueblo_detalle->find('span[class="EBDSTYLE_2052]') as $mail)
        {
            foreach($mail->find('a[class="EBDSTYLE_2052]') as $mail_dato)
            {  
            }
        }

    
        //$datos_pueblo_0 = array();
                
        //$i = 0;

        /*foreach ($html_pueblo_detalle->find('span[class="EBDSTYLE_2052"]') as $datos_pueblo)
        {
            if($i < 9)
            {
                if($i = 0){ $datos_pueblo_0[] = $datos_pueblo_0;}
                if($i = 1){ $datos_pueblo_1 = $datos_pueblo;}
                if($i = 2){ $datos_pueblo_2 = $datos_pueblo;}
                if($i = 3){ $datos_pueblo_3 = $datos_pueblo;}
                if($i = 4){ $datos_pueblo_4 = $datos_pueblo;}
                if($i = 5){ $datos_pueblo_5 = $datos_pueblo;}
                if($i = 6){ $datos_pueblo_6 = $datos_pueblo;}
                if($i = 7){ $datos_pueblo_7 = $datos_pueblo;}
                if($i = 8){ $datos_pueblo_8 = $datos_pueblo;}

                
    
                $i++;
            }
        }*/
      
          $muni = array('Mail'=>$element[6]->plaintext, 'Pagina Web'=>$webs[0]->innertext, 'FAX'=>$element[5]->innertext, 'Telefono'=>$element[4]->innertext, 'Nº Habitantes'=>$element[3]->innertext, 'C.P'=>$element[2]->innertext, 'Direccion' =>$element[1]->innertext, 'Municipio' => $element[0]->innertext );

        scraperwiki::save(array('Municipio'), $muni);

        //print $datos_pueblo_array[0] . "\n"; 

//$record = array( 'municipio' => $datos_pueblo_array[0], 'direccion' => $datos_pueblo_array[1]->plaintex); 
 //scraperwiki::save(array('municipio'), $record);



?>

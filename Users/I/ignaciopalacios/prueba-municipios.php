<?php

# Blank PHP

$html_content = scraperwiki::scrape("http://www.lawebmunicipal.com/municipiosdeespana/_6cARqRrTH-_u2rE1kFTYGA");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html_content);




$i=0;

foreach ($dom->find('a[class="EBDSTYLE_1018"]') as $dire_municipio)
{$i++;

if($i < 20)
{
    //$provincia = $dom->find('a[class="EBDSTYLE_1018"]');
    
    $dire_mun = $dire_municipio->href;

    $pad_length = strlen($dire_mun);
    $pad_string = "http://www.lawebmunicipal.com";

    $dire_completa_mu = str_pad  ($dire_mun, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);

    $html_pueblo_content = scraperwiki::scrape($dire_completa_mu);
    $html_pueblo = str_get_html($html_pueblo_content);


//------------------------------------------------------------------------------------------------------

    foreach ($html_pueblo->find('a[class="EBDSTYLE_2052"]') as $dire_pueblo)
    {
        
        $dire_pu = $dire_pueblo->href;

        $pad_length = strlen($dire_pu);
        $pad_string = "http://www.lawebmunicipal.com";

        $dire_completa_pu = str_pad  ($dire_pu, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);

        $html_pueblo_detalle_content = scraperwiki::scrape($dire_completa_pu);
        $html_pueblo_detalle = str_get_html($html_pueblo_detalle_content);
        
        $element = $html_pueblo_detalle->find('span[class="EBDSTYLE_2052]');
        $webs = $html_pueblo_detalle->find('a[class="EBDSTYLE_2052"]');

        $muni = array('Mail'=>$element[6]->plaintext, 'Pagina Web'=>$webs[0]->innertext, 'FAX'=>$element[5]->innertext, 'Telefono'=>$element[4]->innertext, 'Nº Habitantes'=>$element[3]->innertext, 'C.P'=>$element[2]->innertext, 'Direccion' =>$element[1]->innertext, 'Municipio' => $element[0]->innertext, 'Provincia' => $dire_municipio->plaintext );

        scraperwiki::save(array('Municipio'), $muni);

//------------------------------------------------------------------------------------------------------    
    
    //$muni = array('Municipio' => $dire_completa_pu);
    //scraperwiki::save(array('Municipio'), $muni);
    }
}
}





?>
<?php

# Blank PHP

$html_content = scraperwiki::scrape("http://www.lawebmunicipal.com/municipiosdeespana/_6cARqRrTH-_u2rE1kFTYGA");

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();
$dom->load($html_content);




$i=0;

foreach ($dom->find('a[class="EBDSTYLE_1018"]') as $dire_municipio)
{$i++;

if($i < 20)
{
    //$provincia = $dom->find('a[class="EBDSTYLE_1018"]');
    
    $dire_mun = $dire_municipio->href;

    $pad_length = strlen($dire_mun);
    $pad_string = "http://www.lawebmunicipal.com";

    $dire_completa_mu = str_pad  ($dire_mun, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);

    $html_pueblo_content = scraperwiki::scrape($dire_completa_mu);
    $html_pueblo = str_get_html($html_pueblo_content);


//------------------------------------------------------------------------------------------------------

    foreach ($html_pueblo->find('a[class="EBDSTYLE_2052"]') as $dire_pueblo)
    {
        
        $dire_pu = $dire_pueblo->href;

        $pad_length = strlen($dire_pu);
        $pad_string = "http://www.lawebmunicipal.com";

        $dire_completa_pu = str_pad  ($dire_pu, ($pad_length + strlen($pad_string)), $pad_string, STR_PAD_LEFT);

        $html_pueblo_detalle_content = scraperwiki::scrape($dire_completa_pu);
        $html_pueblo_detalle = str_get_html($html_pueblo_detalle_content);
        
        $element = $html_pueblo_detalle->find('span[class="EBDSTYLE_2052]');
        $webs = $html_pueblo_detalle->find('a[class="EBDSTYLE_2052"]');

        $muni = array('Mail'=>$element[6]->plaintext, 'Pagina Web'=>$webs[0]->innertext, 'FAX'=>$element[5]->innertext, 'Telefono'=>$element[4]->innertext, 'Nº Habitantes'=>$element[3]->innertext, 'C.P'=>$element[2]->innertext, 'Direccion' =>$element[1]->innertext, 'Municipio' => $element[0]->innertext, 'Provincia' => $dire_municipio->plaintext );

        scraperwiki::save(array('Municipio'), $muni);

//------------------------------------------------------------------------------------------------------    
    
    //$muni = array('Municipio' => $dire_completa_pu);
    //scraperwiki::save(array('Municipio'), $muni);
    }
}
}





?>

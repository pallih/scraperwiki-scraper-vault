<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");

/*$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");*/

$html = str_get_html($html_content);

//--------- TITULO ----------------------------------------

foreach ($html->find('h3[class="detailTitle"]') as $nombre_tramite);
print $nombre_tramite . "\n";

$titulo = array( 'Titulo' => $nombre_tramite->plaintext); 
scraperwiki::save(array('Titulo'), $titulo);

//--------- ENTRADILLA ------------------------------------

$i = 0;
 
foreach ($html->find('div[class="entradilla"] div[class="parrafo"]') as $entradilla_tramite)
{
    if ($i < 1)
    {
        $entradilla = array( 'Entradilla' => $entradilla_tramite->innertext);
        //print_r($record);
    
        scraperwiki::save(array('Entradilla'), $entradilla);
    }
$i++;
}

//---------- CAMPOS COMUNES ------------------------------

$i=0;

foreach ($html->find('div[class="tabContent"] a[id]') as $id)
{    

    if ($i == 0)
    { 
        foreach ($html->find('div[id="tabContent_0"] div[class="parrafo"]') as $campos_tramite)
        {
            $campo = array( $id->plaintext => $campos_tramite->innertext);
            scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 1)
    {
        foreach ($html->find('div[id="tabContent_1"] div[class="parrafo"]') as $campos_tramite)
        {
           $campo = array( $id->plaintext => $campos_tramite->innertext);         
           scraperwiki::save(array($id->plaintext), $campo);
        }
    }


    if ($i == 2)
    {
        foreach ($html->find('div[id="tabContent_2"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);          
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 3)
    {
        foreach ($html->find('div[id="tabContent_3"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);         
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 4)
    {
        foreach ($html->find('div[id="tabContent_4"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);         
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

$i++;
}

//------- FORMAS DE TRAMITAR ----------------------------

$i=0;


foreach ($html->find('div[class="subficha"] h5[class]') as $forma_tramite)
{$j=0;
    foreach ($html->find('ul[class="tramites"]') as $forma_texto_tramite)
        {
            if($i==0 && $j==0)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }

            if($i==1 && $j==1)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }
            
            if($i==2 && $j==2)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }
            
            if($i==3 && $j==3)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }$j++;
        }

$i++;    
}

//----------- DESCARGAR IMPRESOS -----------------------

foreach ($html->find('div[class="parrafo"] span[class="saveResultAction ftr"]') as $descargar_documento)
{
    
    $documento = array( 'Descargar Impresos' => $descargar_documento->innertext);          
    scraperwiki::save(array('Descargar Impresos'), $documento);
}

?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");

/*$html_content = scraperwiki::scrape("https://sede.madrid.es/portal/site/tramites/menuitem.d3089948cb18b1bb68d8a521ecd08a0c/?vgnextoid=4e24424d52a61110VgnVCM2000000c205a0aRCRD&vgnextchannel=b10737c190180210VgnVCM100000c90da8c0RCRD");*/

$html = str_get_html($html_content);

//--------- TITULO ----------------------------------------

foreach ($html->find('h3[class="detailTitle"]') as $nombre_tramite);
print $nombre_tramite . "\n";

$titulo = array( 'Titulo' => $nombre_tramite->plaintext); 
scraperwiki::save(array('Titulo'), $titulo);

//--------- ENTRADILLA ------------------------------------

$i = 0;
 
foreach ($html->find('div[class="entradilla"] div[class="parrafo"]') as $entradilla_tramite)
{
    if ($i < 1)
    {
        $entradilla = array( 'Entradilla' => $entradilla_tramite->innertext);
        //print_r($record);
    
        scraperwiki::save(array('Entradilla'), $entradilla);
    }
$i++;
}

//---------- CAMPOS COMUNES ------------------------------

$i=0;

foreach ($html->find('div[class="tabContent"] a[id]') as $id)
{    

    if ($i == 0)
    { 
        foreach ($html->find('div[id="tabContent_0"] div[class="parrafo"]') as $campos_tramite)
        {
            $campo = array( $id->plaintext => $campos_tramite->innertext);
            scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 1)
    {
        foreach ($html->find('div[id="tabContent_1"] div[class="parrafo"]') as $campos_tramite)
        {
           $campo = array( $id->plaintext => $campos_tramite->innertext);         
           scraperwiki::save(array($id->plaintext), $campo);
        }
    }


    if ($i == 2)
    {
        foreach ($html->find('div[id="tabContent_2"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);          
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 3)
    {
        foreach ($html->find('div[id="tabContent_3"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);         
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

    if ($i == 4)
    {
        foreach ($html->find('div[id="tabContent_4"] div[class="parrafo"]') as $campos_tramite)
        {
          $campo = array( $id->plaintext => $campos_tramite->innertext);         
          scraperwiki::save(array($id->plaintext), $campo);
        }
    }

$i++;
}

//------- FORMAS DE TRAMITAR ----------------------------

$i=0;


foreach ($html->find('div[class="subficha"] h5[class]') as $forma_tramite)
{$j=0;
    foreach ($html->find('ul[class="tramites"]') as $forma_texto_tramite)
        {
            if($i==0 && $j==0)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }

            if($i==1 && $j==1)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }
            
            if($i==2 && $j==2)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }
            
            if($i==3 && $j==3)
            {
                $forma = array( $forma_tramite->plaintext => $forma_texto_tramite->innertext);          
                scraperwiki::save(array($forma_tramite->plaintext), $forma);
                
            }$j++;
        }

$i++;    
}

//----------- DESCARGAR IMPRESOS -----------------------

foreach ($html->find('div[class="parrafo"] span[class="saveResultAction ftr"]') as $descargar_documento)
{
    
    $documento = array( 'Descargar Impresos' => $descargar_documento->innertext);          
    scraperwiki::save(array('Descargar Impresos'), $documento);
}

?>

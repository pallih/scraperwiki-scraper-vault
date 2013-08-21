<?php
require  'scraperwiki/simple_html_dom.php';

$listville = array ('Dreux','Chartres','Oysonville','montargis','Orléans','Chambord','Blois','Tours','faverolles','vierzon','Bourges','Verneuil','Châteauroux');

foreach ($listville as $ville)
    {
    $ville=$ville;

    $url   = 'http://www.ligair.fr/aspx/chf_StatGeographique.aspx?sVille=' . $ville;
    $html = file_get_html($url); 
            
    // Qualité de l'air
    $ret = $html->find('table[id=wtInfoAtmo] th');
    $t1 = $ret[0]->innertext() ;
    preg_match('/(?P<digit>\d+)/', $t1, $qteaire);
    $r_qteaire =  $qteaire[1];   

    // Le polluant en cause est
    $ret2 = $html->find('table[id=wtInfoAtmo] td');
    $t2 = $ret2[0]->innertext() ;
    preg_match('#<([ib])>(.*?)</\1>#', $t2, $polluant);
    $r_polluant=$polluant[2];
      
    // Prévision pour demain
    $t3 = $ret2[1]->innertext() ;
    preg_match('#<([ib])>(.*?)</\1>#', $t3, $prevision);
    $r_prevision=$prevision[2];    
              
    $ret4 = $html->find('span[id=wlDate]');
    $date = $ret4[0]->innertext() ;
    $id=$ville.date('dm');
      
scraperwiki::save
            (    array('id'),
                 array
                     (    'id'         => $id, 
                          'ville'         => $ville,
                          'qualite_air'       => $r_qteaire,
                          'polluant'        => $r_polluant,
                          'prevision'        => $r_prevision,
                          'date'      => $date
                     )
            ) ;  
        
       echo"$ville\n"; 
    }



?>
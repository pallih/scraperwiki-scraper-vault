<?php

require 'scraperwiki/simple_html_dom.php';        

/*
scraperwiki::save_var("LastRunCounter", 0);
scraperwiki::save_var("EstadoCounter", 0);
scraperwiki::save_var("MunicipioCounter", 0);
scraperwiki::save_var("ParroquiaCounter", 0);
scraperwiki::save_var("CentroCounter", 0);
scraperwiki::save_var("MesaCounter", 0);
*/
 
    $html_URL = "http://www.cne.gob.ve/resultado_presidencial_2013/r/1/reg_210000.html";
    $estado_name = "ZULIA";

$estado_dom = new simple_html_dom();
$municipio_dom = new simple_html_dom();
$parroquia_dom = new simple_html_dom();
$centro_dom = new simple_html_dom();
$mesa_dom = new simple_html_dom();

$SVestado_counter = 0;
$SVmunicipio_counter = 0;
$SVparroquia_counter = 0;
$SVcentro_counter = 0;
$SVmesa_counter = 0;


    $html = scraperWiki::scrape($html_URL); 

    $estado_dom->load($html);


    foreach($estado_dom->find("tr.tbsubtotalrow") as $data) { 

      $tds = $data->find("td.lightRowContent");

      if(count($tds)>0){
        $record = array(
          'LEVEL' => "ESTADO",
          'Estado' => $estado_name,
          'Candidato' => preg_replace('/[ ]{2,}|[\t]/', ' ', trim($tds[1]->plaintext)), 
          'Votos' => preg_replace('/#/',',', preg_replace('/\./',',',preg_replace('/\,/','#', $tds[2]->plaintext))),
          'Porcentaje' => preg_replace('/\,/','.', preg_replace('/%/','',$tds[3]->plaintext)),
          'URL' => $html_URL
          );

        scraperwiki::save(array('VOTOS'), $record);
        $saved_counter++;
        scraperwiki::save_var("LastRunCounter", $saved_counter);

      }

    } 

    $municipio_counter = 0;

    foreach($estado_dom->find("li.region-nav-item a#region_ref") as $municipio_data) {

      if ($municipio_counter >= $SVmunicipio_counter) {


        $html_URL = "http://www.cne.gob.ve/resultado_presidencial_2013" . preg_replace('/\.\.\/\.\./', '', $municipio_data->href);

        $html = scraperWiki::scrape($html_URL); 

        $municipio_dom->load($html);

        foreach($municipio_dom->find("tr.tbsubtotalrow") as $data){ 

          $tds = $data->find("td.lightRowContent");

          if(count($tds)>0){
            $record = array(
              'LEVEL' => "MUNICIPIO",
              'Estado' => $estado_name,
              'Municipio' => $municipio_data->plaintext,
              'Candidato' => preg_replace('/[ ]{2,}|[\t]/', ' ', trim($tds[1]->plaintext)), 
              'Votos' => preg_replace('/#/',',', preg_replace('/\./',',',preg_replace('/\,/','#', $tds[2]->plaintext))),
              'Porcentaje' => preg_replace('/\,/','.', preg_replace('/%/','',$tds[3]->plaintext)),
              'URL' => $html_URL
              );
            scraperwiki::save(array('VOTOS'), $record);
            $saved_counter++;
            scraperwiki::save_var("LastRunCounter", $saved_counter);

          }

        }

        // Parroquia
        $parroquia_counter = 0;

        foreach($municipio_dom->find("li.region-nav-item a#region_ref") as $parroquia_data) {


          if ($parroquia_counter >= $SVparroquia_counter)
          {

            $html_URL = "http://www.cne.gob.ve/resultado_presidencial_2013" . preg_replace('/\.\.\/\.\./', '', $parroquia_data->href);

            $html = scraperWiki::scrape($html_URL); 

            $parroquia_dom->load($html);

            foreach($parroquia_dom->find("tr.tbsubtotalrow") as $data){ 


              $tds = $data->find("td.lightRowContent");

              if(count($tds)>0){
                $record = array(
                  'LEVEL' => "PARROQUIA",
                  'Estado' => $estado_name,
                  'Municipio' => $municipio_data->plaintext,
                  'Parroquia' => $parroquia_data->plaintext,
                  'Candidato' => preg_replace('/[ ]{2,}|[\t]/', ' ', trim($tds[1]->plaintext)), 
                  'Votos' => preg_replace('/#/',',', preg_replace('/\./',',',preg_replace('/\,/','#', $tds[2]->plaintext))),
                  'Porcentaje' => preg_replace('/\,/','.', preg_replace('/%/','',$tds[3]->plaintext)),
                  'URL' => $html_URL
                  );
                scraperwiki::save(array('VOTOS'), $record);
                $saved_counter++;
                scraperwiki::save_var("LastRunCounter", $saved_counter);

              }

            }

            // Centro
            $centro_counter = 0;

            foreach($parroquia_dom->find("li.region-nav-item a#region_ref") as $centro_data) {

              $mesa_counter = 0;

              if ($centro_counter >= $SVcentro_counter)
              {

                $html_URL = "http://www.cne.gob.ve/resultado_presidencial_2013" . preg_replace('/\.\.\/\.\./', '', $centro_data->href);

                $html = scraperWiki::scrape($html_URL); 

                $centro_dom->load($html);

                foreach($centro_dom->find("tr.tbsubtotalrow") as $data){ 

                  $tds = $data->find("td.lightRowContent");

                  if(count($tds)>0){
                    $record = array(
                      'LEVEL' => "CENTRO",
                      'Estado' => $estado_name,
                      'Municipio' => $municipio_data->plaintext,
                      'Parroquia' => $parroquia_data->plaintext,
                      'Centro' => $centro_data->plaintext,
                      'Candidato' => preg_replace('/[ ]{2,}|[\t]/', ' ', trim($tds[1]->plaintext)), 
                      'Votos' => preg_replace('/#/',',', preg_replace('/\./',',',preg_replace('/\,/','#', $tds[2]->plaintext))),
                      'Porcentaje' => preg_replace('/\,/','.', preg_replace('/%/','',$tds[3]->plaintext)),
                      'URL' => $html_URL
                      );

                    scraperwiki::save(array('VOTOS'), $record);
                    $saved_counter++;
                    scraperwiki::save_var("LastRunCounter", $saved_counter);

                  }

                }
                // Mesa
                $mesa_counter = 0;

                foreach($centro_dom->find("li.region-nav-item a#region_ref") as $mesa_data) {

                  if ($mesa_counter >= $SVmesa_counter)
                  {

                    $html_URL = "http://www.cne.gob.ve/resultado_presidencial_2013" . preg_replace('/\.\.\/\.\./', '', $mesa_data->href);

                    $html = scraperWiki::scrape($html_URL); 

                    $mesa_dom->load($html);

                    foreach($mesa_dom->find("tr.tbsubtotalrow") as $data){ 

                      $tds = $data->find("td.lightRowContent");

                      if(count($tds)>0){
                        $record = array(
                          'LEVEL' => "MESA",
                          'Estado' => $estado_name,
                          'Municipio' => $municipio_data->plaintext,
                          'Parroquia' => $parroquia_data->plaintext,
                          'Centro' => $centro_data->plaintext,
                          'Mesa' => $mesa_data->plaintext,
                          'Candidato' => preg_replace('/[ ]{2,}|[\t]/', ' ', trim($tds[1]->plaintext)), 
                          'Votos' => preg_replace('/#/',',', preg_replace('/\./',',',preg_replace('/\,/','#', $tds[2]->plaintext))),
                          'Porcentaje' => preg_replace('/\,/','.', preg_replace('/%/','',$tds[3]->plaintext)),
                          'URL' => $html_URL
                          );
                        scraperwiki::save(array('VOTOS'), $record);
                        $saved_counter++;
                        scraperwiki::save_var("LastRunCounter", $saved_counter);
                      }

                    }

                    scraperwiki::save_var("MesaCounter", $mesa_counter);
                  }
                  $mesa_counter++;


        } // Mesa


        scraperwiki::save_var("CentroCounter", $centro_counter);
      }
      $centro_counter++;


        } // Centro


        scraperwiki::save_var("ParroquiaCounter", $parroquia_counter);
      }
      $parroquia_counter++;


        } // Parroquia


        scraperwiki::save_var("MunicipioCounter", $municipio_counter);
      }
      $municipio_counter++;


    } // Municipio

    scraperwiki::save_var("EstadoCounter", $estado_counter);
# print $html . "\n";

?>
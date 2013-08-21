<?php
require 'scraperwiki/simple_html_dom.php';

$bairro = array(
'Bangu','Bonsucesso','Campo%20dos%20Afonsos','Campo%20Grande','Cascadura','Del%20Castilho','Duque%20de%20Caxias',v'Freguesia','Guadalupe','Humait%E1','Icara%ED','Jardim%20Botânico','Largo%20do%20Machado','Madureira','Mallet','Nil%F3polis','Niter%F3i','Nova%20Igua%E7u','Olaria','Penha','Taquara','Vargem%20Grande','Vassouras','Vila%20da%20Penha');

/*
'Bangu','Barra da Tijuca','Bonsucesso','Botafogo','Campo dos Afonsos','Campo Grande','Cascadura','Centro','Copacabana','Del Castilho','Duque de Caxias','Flamengo','Freguesia','Gávea','Guadalupe','Humaitá','Icaraí','Ilha do Governador','Ipanema','Jacarepaguá','Jardim Botânico','Largo do Machado','Leblon','Madureira','Mallet','Méier','Nilópolis','Niterói','Nova Iguaçu','Olaria','Penha','Recreio dos Bandeirantes','Taquara','Tijuca','Vargem Grande','Vassouras','Vila da Penha','Vila Isabel'
*/

for ($i=0; $i < sizeof($bairro); $i++){
    //scrape($bairro[$i]);
}

function scrape($bairro)
{
$url = "http://www.gegmedical.com.br/1024/pesquisa.php?esp=Odontologia&bai=".$bairro;

$html = scraperWiki::scrape($url);            

$html = str_replace('&iacute;','í',$html);
$html = str_replace('&oacute;','ó',$html);
$html = str_replace('&aacute;','á',$html);
$html = str_replace('&uacute;','ú',$html);
$html = str_replace('&eacute;','é',$html);
$html = str_replace('&ecirc;','ê',$html);
$html = str_replace('&acirc;','â',$html);
$html = str_replace('&ocirc;','ô',$html);
$html = str_replace('&ccedil;','ç',$html);
$html = str_replace('&atilde;','ã',$html);
$html = str_replace('&otilde;','õ',$html);
$html = str_replace('&ordf;','ª',$html);
$html = str_replace('&ordm;','º',$html);     

$dom = new simple_html_dom();
$dom->load($html);


 foreach($dom->find('div[id=box_medico]') as $medico)
  {

 foreach($medico->find('span[class=nome]') as $data)
  {
      $nome = trim($data->plaintext);
 
      print $nome."\n";
  };

/*
 foreach($medico->find('span[class=crm]') as $data)
  {
      $crm= trim($data->plaintext);
 
      print $crm."\n";
  };
*/

 foreach($medico->find('div[class=endereco]') as $data)
   {
       $endereco= trim($data->plaintext);
  
       print $endereco."\n";

   };

   scraperwiki::save(array('nome'), array('nome' => $nome, 'endereco' => $endereco, 'bairro' => $bairro));
};

}
?>


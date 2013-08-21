<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.fundamentus.com.br/detalhes.php?papel=&x=37&y=26");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$i=1;
$count=1;

$text="INSERT INTO acao(codigo,nome,area) VALUES ";

foreach($dom->find('td') as $data)
{
    if($i==1) {
        $text .= "('{$data->plaintext}',";
        $codigo[] = $data->plaintext;
        $i = 2;
    }
    else if ($i ==2) {
        $text .= "'{$data->plaintext}',";
        $nomecomercial[] = $data->plaintext;
        $i = 3;
    }
    else if ($i == 3) {
        $text .= "'{$data->plaintext}') ,";
        $razaosocial[] = $data->plaintext;
        $i = 1;
    }
    $count++;
    print $count;
    //if($count==7) break;
}

print $text;

//foreach($codigo as $j => $cod) 
//    scraperwiki::save(array('codigo','nomecomercial','razaosocial'),array('codigo'=>$cod,'nomecomercial'=>$nomecomercial[$j],'razaosocial'=>$razaosocial[$j]));

?>
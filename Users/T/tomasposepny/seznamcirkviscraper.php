<?php
######################################
# PHP scraper for Seznam cirkvi
######################################

require  'scraperwiki/simple_html_dom.php';

#function odstranDiakritiku($text)
#{
#    return iconv("windows-1250", "ascii//TRANSLIT", $text);
#}

$html = scraperwiki::scrape("http://www3.mkcr.cz/cns_internet/CNS/detail_cns.aspx?id_subj=147&str_zpet=Seznam_cns.aspx");
#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
$nazev = false;
$table = $dom->getElementById('Table3'); 
foreach($table->find('td') as $data)
{
    print $data;

    #kdyz konci dvojteckou, indexuji timto slovem
    if(ereg(":$",$data))
    {
        if(($nazev == true) && ($data->plaintext == "Název:"))
        {
            $data = "Nazev organu cirkve:"; 
        }
        elseif($data->plaintext == "Název:")
        {
            $nazev = true;
        }
        $index = odstranDiakritiku($data->plaintext);
    }

    #jinak ukladam do pole indexovaneho textovou hodnotou
    else
    {
        $output[$index] = $data;
   }
}



#foreach($dom->find('td') as $data)
#{
    # Store data in the datastore
#    print $data->plaintext . "\n";
#    scraperwiki::save(array('data'), array('data' => $data->plaintext));
#}

?>
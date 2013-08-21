<?php
# Blank PHP
require  'scraperwiki/simple_html_dom.php';

function toIndex($text){
$text= iconv('Windows-1252', 'ASCII//TRANSLIT', $text);
return  Str_Replace(' ','_',$text);
}

$html = scraperwiki::scrape("http://www3.mkcr.cz/cns_internet/CNS/detail_cns.aspx?id_subj=147&str_zpet=Seznam_cns.aspx");
$dom = new simple_html_dom();
$dom->load($html);
#print toIndex("Dataž :");
#$table=$data->find('table[id=Table3]');
$curIndex="";
foreach($dom->getElementById('Table3')->find('td') as $data)
{
            $txt=$data->plaintext;
            if(ereg(":$",$txt)){
            $curIndex=toIndex($txt);
        
        }   
        else{
        $field[$curIndex]=$txt;
    print $field[$curIndex] . "\n";   
    }
    
}
foreach($field as $i=>$a){
print $i . $a . "\n";
}
print "fbjksdhf\n";
?>
//
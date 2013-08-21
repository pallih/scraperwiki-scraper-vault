<?php
require 'scraperwiki/simple_html_dom.php';
//scraperwiki::sqliteexecute("create table tzz (`word` string, `link` string, `description` string)");

for ($i=1094;$i<1923;++$i) {
    $html_content = scraperwiki::scrape("http://www.zodynas.lt/terminu-zodynas/?page=".$i);
    $html = str_get_html($html_content);
    foreach ($html->find("ul.abc_list li") as $el) {
        $word = trim(str_replace(' ','',$el->find('a',0)->innertext),'.- \r\n\0\x0B\t');
        $word_full = trim($el->find('a',0)->innertext,'.- \r\n\0\x0B\t');
        $link = $el->find('a',0)->href;
        $desc = '';
        //$html_content_2 = scraperwiki::scrape("http://www.zodynas.lt".$link);
        //$html_2 = str_get_html($html_content_2);
        //$desc = trim(str_replace($word_full,'',$html_2->find('h1',0)->next_sibling()->innertext));
        //$desc = explode(',',$desc,2);
        //$desc = $desc[1];
        //$html_2->__destruct();
        //print $word.'|'.$link.'|'.$desc.'\r';
        scraperwiki::save_sqlite(array("word"),array("word"=>$word, "link"=>$link,"description"=>$desc));
    }
    $html->__destruct();
}
scraperwiki::sqlitecommit(); 

?>

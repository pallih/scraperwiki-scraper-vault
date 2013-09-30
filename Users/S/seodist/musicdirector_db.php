<?php

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 1; $pn < 6; $pn++) 
{
    $url = "http://en.600024.com/musicdirector/list/page/".$pn."/";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('table') as $data)
    {
        //print "inside first loop";
        //print $data->href;
        foreach ($data->find('td') as $el)
        {
        $el1 = $el->find('a');
        $url2 = $el1[1]->href;
        //print "\n";
        $html2 = scraperwiki::scrape($url2);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
            foreach($dom2->find('td[class="model"]') as $data2)
            {
                print 'inside';
                $detail = $data2->find('span');
                $label  = $data2->find('label');
                $record = array(trim($label[0]->plaintext)=>trim($detail[0]->plaintext),
                                trim($label[1]->plaintext)=>trim($detail[1]->plaintext),
                                trim($label[2]->plaintext)=>trim($detail[2]->plaintext),
                                trim($label[3]->plaintext)=>trim($detail[3]->plaintext),
                                trim($label[4]->plaintext)=>trim($detail[4]->plaintext)); 
           scraperwiki::save_sqlite(array(trim($label[0]->plaintext),
                                          trim($label[1]->plaintext),
                                          trim($label[2]->plaintext),
                                          trim($label[3]->plaintext),
                                          trim($label[4]->plaintext)),$record,"MusicDirectory");
            }
                    
        }
        
    }
}
  
?>


<?php

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 1; $pn < 6; $pn++) 
{
    $url = "http://en.600024.com/musicdirector/list/page/".$pn."/";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('table') as $data)
    {
        //print "inside first loop";
        //print $data->href;
        foreach ($data->find('td') as $el)
        {
        $el1 = $el->find('a');
        $url2 = $el1[1]->href;
        //print "\n";
        $html2 = scraperwiki::scrape($url2);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
            foreach($dom2->find('td[class="model"]') as $data2)
            {
                print 'inside';
                $detail = $data2->find('span');
                $label  = $data2->find('label');
                $record = array(trim($label[0]->plaintext)=>trim($detail[0]->plaintext),
                                trim($label[1]->plaintext)=>trim($detail[1]->plaintext),
                                trim($label[2]->plaintext)=>trim($detail[2]->plaintext),
                                trim($label[3]->plaintext)=>trim($detail[3]->plaintext),
                                trim($label[4]->plaintext)=>trim($detail[4]->plaintext)); 
           scraperwiki::save_sqlite(array(trim($label[0]->plaintext),
                                          trim($label[1]->plaintext),
                                          trim($label[2]->plaintext),
                                          trim($label[3]->plaintext),
                                          trim($label[4]->plaintext)),$record,"MusicDirectory");
            }
                    
        }
        
    }
}
  
?>



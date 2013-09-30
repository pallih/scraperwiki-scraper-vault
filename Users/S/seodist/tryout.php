<?php

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 2; $pn < 3; $pn++) 
{
    $url = "http://en.600024.com/musicdirector/list/page/".$pn."/";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('table') as $data)
    {
        foreach ($data->find('td') as $el)
        {
        $el1 = $el->find('a');
        $url2 = $el1[1]->href;
        //print "\n";
        $html2 = scraperwiki::scrape($url2);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
            foreach($dom2->find('td.model div.detail_row') as $data2)
            {
                $nomov = trim($data2->children(0)->plaintext);
                if ( $nomov == "No of Movies:")
                    {
                    //print $nomov;
                    $pnmax2 = trim($data2->children(1)->plaintext);
                    $pnmax2 = ceil($pnmax2/15);
                    print "pnmax2:".$pnmax2."\n";
                    for ($i= 1; $i <= $pnmax2; $i++)
                    {
                    $url3 = $data2->children(1)->href."page/".$i."/";
                    print "url3:".$url3."\n";               
                    $html3 = scraperwiki::scrape($url3);
                    $dom3 = new simple_html_dom();
                    $dom3->load($html3);
                    foreach($dom3->find('div[class="movietitle"]') as $data3)
                        {
                            $divs = $data3->find("a");
                            $url4 = trim($divs[0]->href);
                            print "url4:".$url4."\n";               
                            $html4 = scraperwiki::scrape($url4);
                            $dom4 = new simple_html_dom();
                            $dom4->load($html4);
                            foreach($dom4->find('td[class="model"]') as $data4)
                            {
                               $detail = $data4->find('span');
                               $label  = $data4->find('label');
                               //print trim($label[2]->plaintext); 
                               //print "\n"; 
                               $record = array(trim($label[0]->plaintext)=>trim($detail[0]->plaintext),
                                               trim($label[1]->plaintext)=>trim($detail[1]->plaintext),
                                               trim($label[2]->plaintext)=>trim($detail[2]->plaintext),
                                               trim($label[3]->plaintext)=>trim($detail[3]->plaintext),
                                               trim($label[4]->plaintext)=>trim($detail[4]->plaintext)); 
                               scraperwiki::save_sqlite(array(trim($label[0]->plaintext),
                                                              trim($label[1]->plaintext),
                                                              trim($label[2]->plaintext),
                                                              trim($label[3]->plaintext),
                                                              trim($label[4]->plaintext)),$record,"FullMovDB");
                    
                               
                            }
                       }

                   
                    }
                }

                
            }                    
        }        
    }
}
  
?>


<?php

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 2; $pn < 3; $pn++) 
{
    $url = "http://en.600024.com/musicdirector/list/page/".$pn."/";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('table') as $data)
    {
        foreach ($data->find('td') as $el)
        {
        $el1 = $el->find('a');
        $url2 = $el1[1]->href;
        //print "\n";
        $html2 = scraperwiki::scrape($url2);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
            foreach($dom2->find('td.model div.detail_row') as $data2)
            {
                $nomov = trim($data2->children(0)->plaintext);
                if ( $nomov == "No of Movies:")
                    {
                    //print $nomov;
                    $pnmax2 = trim($data2->children(1)->plaintext);
                    $pnmax2 = ceil($pnmax2/15);
                    print "pnmax2:".$pnmax2."\n";
                    for ($i= 1; $i <= $pnmax2; $i++)
                    {
                    $url3 = $data2->children(1)->href."page/".$i."/";
                    print "url3:".$url3."\n";               
                    $html3 = scraperwiki::scrape($url3);
                    $dom3 = new simple_html_dom();
                    $dom3->load($html3);
                    foreach($dom3->find('div[class="movietitle"]') as $data3)
                        {
                            $divs = $data3->find("a");
                            $url4 = trim($divs[0]->href);
                            print "url4:".$url4."\n";               
                            $html4 = scraperwiki::scrape($url4);
                            $dom4 = new simple_html_dom();
                            $dom4->load($html4);
                            foreach($dom4->find('td[class="model"]') as $data4)
                            {
                               $detail = $data4->find('span');
                               $label  = $data4->find('label');
                               //print trim($label[2]->plaintext); 
                               //print "\n"; 
                               $record = array(trim($label[0]->plaintext)=>trim($detail[0]->plaintext),
                                               trim($label[1]->plaintext)=>trim($detail[1]->plaintext),
                                               trim($label[2]->plaintext)=>trim($detail[2]->plaintext),
                                               trim($label[3]->plaintext)=>trim($detail[3]->plaintext),
                                               trim($label[4]->plaintext)=>trim($detail[4]->plaintext)); 
                               scraperwiki::save_sqlite(array(trim($label[0]->plaintext),
                                                              trim($label[1]->plaintext),
                                                              trim($label[2]->plaintext),
                                                              trim($label[3]->plaintext),
                                                              trim($label[4]->plaintext)),$record,"FullMovDB");
                    
                               
                            }
                       }

                   
                    }
                }

                
            }                    
        }        
    }
}
  
?>



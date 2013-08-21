<?php
$scrape=Array("http://www.anc.org.za/caucus/mplist.php?type=National%20Assembly","http://www.anc.org.za/caucus/mplist.php?type=National%20Council%20of%20Provinces");
$house=Array('NA','NCOP');
require 'scraperwiki/simple_html_dom.php'; 
for ($i=0;$i<2;$i++) {
    $html = scraperWiki::scrape($scrape[$i]);                
    $dom = new simple_html_dom();
    $dom->load($html);
    $tables = $dom->find("table"); //we only need the first one...
    foreach ($tables[0]->find("a") as $link) {
        //now loop through the list of surname pages
        //print 'http://www.anc.org.za/caucus/'.$link->href;
        $html2 = scraperWiki::scrape(str_replace(' ','%20','http://www.anc.org.za/caucus/'.$link->href)) ;
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
        //foreach ($dom2->find("table") as $t) {
        //    print $t->plaintext;
        //}
        $members_table = $dom2->find("table"); //we want the second one
        if (count($members_table)>2) {
            foreach ($members_table[1]->find('a') as $member_link) {
                $html3=scraperWiki::scrape('http://www.anc.org.za/caucus/'.$member_link->href);
                $dom3 = new simple_html_dom();
                $dom3->load($html3);
                $gotname=false;
                $gottable=false;
                $member=array();
                $pre='';//bit to identify section
                $doingcommittees=false;
                //get anc website id
                $id_find=explode('?q=',$member_link->href);
                $member['web_id']=$id_find[1];
                $member['House']=$house[$i];
                foreach ($dom3->find("table") as $key=>$member_table) {
                    if (!$gottable) {
                        foreach ($member_table->find("tr") as $tr) {
                            $td = $tr->find("td");
                            if ($td[0]->colspan==2) {
                                //we have a two column row - probably some kind of title
                                $pre='';
                                if (!$gotname) {
                                    //haven't got the name - remove brackets (site inconsistent about use)
                                    $components1=explode(' (',$td[0]->plaintext);
                                    $member['Name']=$components1[0];
                                    $gotname=true;
                                }
                                else if ($td[0]->plaintext=='Parliamentary Committee Membership') {
                                    $doingcommittees=true;
                                }
                                else if ($doingcommittees) {
                                    $member['Parliamentary Committee Membership']=$td[0]->plaintext;
                                    $doingcommittees=false;
                                }
                                else {
                                    $pre=str_replace(':','',$td[0]->plaintext).' ';
                                }
                             }
                             else if (count($img=$td[0]->find("img"))>0) {
                                    //photo
                                    $member['Photo URL']='http://www.anc.org.za/caucus/members_images/'.$img[0]->src;
                             }
                             else {
                                //ordinary 2 columns
                                if (($td[0]->plaintext!='&nbsp;')&&($td[1]->plaintext!='&nbsp;')) $member[$pre.str_replace(':','',$td[0]->plaintext)]=$td[1]->plaintext;
                            }
                        }
                        
                        $gottable=true;
                    }
                }
            //uncomment to only scrape one MP (useful for testing)
            //print_r($member);
            //break 2;
            try {
                scraperwiki::save(array('web_id'), $member);
            }
            catch (Exception $e) {
                print 'Caught exception: '.$e->getMessage()."\n";
            }
            }
        }
    }
}

?>

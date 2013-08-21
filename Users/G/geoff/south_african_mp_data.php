<?php
require 'scraperwiki/simple_html_dom.php';

function clean($in) {
    return str_replace(" ",'',str_replace('&nbsp;','',str_replace("\t",'',str_replace("\n",'',$in))));
}

//clear the tables
scraperwiki::sqliteexecute("drop table if exists mps");
scraperwiki::sqliteexecute("drop table if exists register");
scraperwiki::sqliteexecute("drop table if exists memberships");

$html = scraperWiki::scrape('http://www.parliament.gov.za/live/content.php?Category_ID=97');                
$dom = new simple_html_dom();
$dom->load($html);
$tables = $dom->find(".tableOrange_sep");
$headers=Array();
$exp=Array();
foreach ($tables[0]->find("tr") as $key => $tr) {
    $mps=Array();
    $count=0;
    foreach ($tr->find('td') as $k=>$td) {
        
        if ($td->colspan==7) continue 2; //don't log spacer rows
        if (($td->class!='pad')&&($td->class!='table_col_bg')) continue; //don't log spacer columns
        if ($key==0) $headers[]=$td->plaintext;
        else {
            $mps[$headers[$count]]=str_replace("\n",'',utf8_encode($td->plaintext));
            if ($k==0) {
                $link=$td->find('a');
                $part=explode('MemberID=',$link[0]->href);
                $mps['parliament_mp_id']=$part[1];
               
                //if ($mps['parliament_mp_id']!=978) continue 2;
                //print "'".$mps['parliament_mp_id']."'";
            }
            if (($headers[$count]==' E-mail address')||($headers[$count]=='Party')) unset($mps[$headers[$count]]);
            
        }
        
        $count++;
        //print $count;
    }
    if (isset($mps['parliament_mp_id'])) {
        //now get MP specific info from page
        $html2 = scraperWiki::scrape('http://www.parliament.gov.za/live/content.php?Item_ID=184&MemberID='.$mps['parliament_mp_id']);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
        foreach ($dom2->find("table") as $k2=>$mp_table) {
            //print $k2;
            //print $mp_table->plaintext;
            if ($k2==17) {
                //print 'table'.$mp_table->innertext."\n";
                foreach ($mp_table->find("tr") as $mp_detail) {
                    //print 'row'.$mp_detail->plaintext."\n";
                    $mp_col=$mp_detail->find('td');
                    if (($mp_col[0]->colspan!=3)&&(count($mp_col)>1)) {
                        if ($mp_col[0]->plaintext=='Members Register:') {
                            $reg=$mp_col[1]->find('a');
                            $html3 = scraperWiki::scrape('http://www.parliament.gov.za/live/'.$reg[0]->href);
                            //print $reg[0]->href;
                            $dom3 = new simple_html_dom();
                            $dom3->load($html3);
                            //print $dom3->plaintext;
                            $process=false;$dont=false;
                            foreach ($dom3->find('table[border=0]') as $t3i=>$t3) {
                                //print $t3i.$t3->plaintext."\n";
                                if ($t3i==13) {
                                    $t3_name=$t3->find('.darker');
                                    //print '\''.$t3_name[0]->plaintext.'\''."\n"; //get MP name again, helps users verify
                                    }
                                if ($t3i==15) { //get the year
                                    $t3_tr=$t3->find('tr');
                                    print '\''.str_replace(' ','',str_replace('&nbsp;','',str_replace("\t",'',$t3_tr[1]->plaintext))).'\'';
                                }
                                if ($process) { //previous table indicates this is something we want to track
                                    //print 'working'.$t3->plaintext;
                                    unset($header2);
                                   $header2=Array();
                                    foreach ($t3->find('tr') as $t4i=>$t4) {
                                        
                                        $expenses=Array();
                                        $expenses['person']=utf8_encode($t3_name[0]->plaintext);
                                        $expenses['parliament_mp_id']=$mps['parliament_mp_id'];
                                        $expenses['year']=str_replace(' ','',str_replace('&nbsp;','',str_replace("\t",'',$t3_tr[1]->plaintext)));
                                        foreach ($t4->find('td') as $t5i=>$t5) {
                                            //print $t4->bgcolor;
                                            //print $t5->colspan.'-'.$t5i.'-'.$t5->height."\n";
                                            if ($t5->height==3) break; //spacer row, ignore
                                            if (count($t5->find('table'))>0) break;
                                            if ($t4i==0) $header2[$t5i]=$t5->plaintext;
                                            else if (($t4i!=0)&&(($t4->bgcolor!='#FFFFFF')&&(count($t4->find('b'))>0))) {
                                                //print 'hi'.count($t4->find('b'));
                                                //print "trigger\n";
                                                break 2;
                                            }
                                            else if (isset($header2[$t5i])) {$expenses[str_replace('&nbsp;','',$header2[$t5i])]=utf8_encode(str_replace('&nbsp;','',$t5->plaintext)); }
                                        }
                                        if (count($expenses)>3) {
                                            scraperwiki::save_sqlite(array(), $expenses, $table_name="register"); 
                                            print_r($expenses);
                                        }
                                    }
                                    
                                    $process=false;
                                }
                                else if ($dont) {
                                    $dont=false;
                                }
                                else if ($t3i>16) {
                                    $row=clean($t3->plaintext);
                                    //if (($row==' Sharesandotherfinancialinterests')||($row==' Directorshipsandpartnerships')||($row==' Landandproperty')||($row=='Giftsandhospitality')||($row=='Travel')) $process=true;
                                    $t3d=$t3->find('td');//print $t3d[0]->colspan."part1\n";print $row;
                                    if ((count($t3d)>0)&&($t3d[0]->colspan==2)) {
                                        //if ($t3d[0]->colspan==2) print "'".str_replace(' ','',clean($t3->plaintext))."'\n";
                                        $process=true;//print "part2\n";
                                    }
                                }
                            }
                        }
                        else if ($mp_col[0]->plaintext=='Speeches:') {
                            print $mp_col[1]->plaintext; //test to see if any speeches are stored
                        }
                        
                        else {
                            $mps[str_replace(':','',$mp_col[0]->plaintext)]=$mp_col[1]->plaintext;
                            //print $mp_col[0]->colspan;
                        }
                    }
                    else if ($mp_col[0]->colspan==3) { //assuming this is the committee list
                            //print 'memberships';
                            foreach ($mp_col[0]->find('a') as $com_link) {
                                $com=array();
                                $com['name']=$mps['First names '].' '.$mps['Surname '];
                                $com['parliament_mp_id']=$mps['parliament_mp_id'];
                                $com['committee']=$com_link->plaintext;
                                $temp1=explode('&CommitteeID=',$com_link->href);
                                $com['parliament_committee_id']=$temp1[1];
                                scraperwiki::save_sqlite(array(), $com, $table_name="memberships");
                            }
                        }
                }
            }
        }
            
    }
    scraperwiki::save_sqlite(array('parliament_mp_id'), $mps, $table_name="mps");
    //if ($key==6) break;
}

?>

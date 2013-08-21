<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

#$csv = "http://api.scraperwiki.com/api/1.0/datastore/getdata?format=csv&name=ireland_cands_from_irelandelections";
$contents = file_get_contents("http://api.scraperwiki.com/api/1.0/datastore/getdata?format=csv&name=ireland_cands_from_irelandelections&limit=100&offset=0");
$lines = split("\n",$contents);
$data = array();
$c = 0;
foreach($lines as $line)
{
#    echo "\n" . $c . " -- " . $line ;
    if ($c == 0)
    {
        $c++;
    }
    else if (trim($line) != "")
    {
        $name = "";
        $activities = array();
        $dom = new simple_html_dom();
        $html = scraperwiki::scrape($line);
#        $html = scraperwiki::scrape("http://electionsireland.org/candidate.cfm?ID=7752");
        $dom->load($html);
        
        $name = trim($dom->find('h1',0)->plaintext);
       
        $activtable;
        $tablefound = false;
        $tables = $dom->find('table');
        foreach ($tables as $table)
        {
            if (!$tablefound)
            {
                $rows = $table->find('tr');
                $firstrow = $rows[0];
                $cols = $firstrow->find('td');
                $firstcol = $cols[0];
                $bolds = $firstcol->find('b');
                if ($bolds)
                {
                    $bold = $bolds[0]->plaintext;
                    if ($bold == "&nbsp;Date&nbsp;")
                    {
                        $tablefound = true;
                        $activtable = $table;
                    }
                }
            }
        }
        
        $rowCount = 0;
        $done = false;
        foreach($activtable->find('tr') as $row)
        {
            if ($rowCount > 1 && !$done)
            {
                $values = $row->find('td');
                if (count($values) == 1)
                {
                    $done = true;
                }
                else
                {
                    $colCount = 0;
                    $activity = array();
                    foreach($values as $cellvalue)
                    {
#                        print $colCount . " _ " . $cellvalue->plaintext . "\n";
                        switch($colCount)
                        {
                            case 0:
                                $date = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                $activity['date'] = $date;
                                break;
                            case 2:
                                $election = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                $activity['election'] = $election;
                                break;
                            case 4:
                                $children_lvl1 = $cellvalue->children;
                                $child_lvl1 = $children_lvl1[0];
                                $children_lvl2 = $child_lvl1->children;
                                $child_lvl2 = $children_lvl2[0];
                                $attrs = $child_lvl2->attr;
                                $title = $attrs['title'];
                                $party = trim(str_replace("&nbsp;", "", $title));
                                $activity['party'] = $party;
                                break;
                            case 6:
                                 $status = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                 $activity['status'] = $status;
                                 break;
                            case 8:
                                 $constituency = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                 $activity['constituency'] = $constituency;
                                 break;
                            case 10:
                                 $seat = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                 $activity['seat'] = $seat;
                                 break;
                            case 12:
                                 $count = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                 $activity['count'] = $count;
                                 break;
                            case 14:
                                  $votes = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                  $activity['votes'] = $votes;
                                  break;
                            case 16:
                                  $share = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                  $activity['share'] = $share;
                                  break;
                            case 18:
                                  $quota = trim(str_replace("&nbsp;", "", $cellvalue->plaintext));
                                  $activity['quota'] = $quota;
                                  break;
                        }
                        $colCount++;  
                    }
                    array_push($activities, $activity);
                }
            }      
            $rowCount++;
        }
        $data[$name] = $activities;
        $c++;
        sleep(1);
    }
        
}

#print $c . "\n\n";
$json = json_encode($data);
print $json;
?>
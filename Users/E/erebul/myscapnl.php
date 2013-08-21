<?php
set_time_limit(0);

$i=5;
$flag = true;
$last = '0|0|0';
$last = explode('|',$last);

$letters = array('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0');
for($i=$last[0];$i<count($letters);$i++)
{
    for($j=$last[1];$j<count($letters);$j++)
    {
        for($k=$last[2];$k<count($letters);$k++)
        {
            $s = $letters[$i].$letters[$j].$letters[$k];
            scraperwiki::save_var('last_search', $s);
echo $s;exit;
            $flag = true;
            while($flag)
            {
            
                $html = scraperWiki::scrape("http://www.kvk.nl/zoek/?q=".$s."&site=alles&start=".$i);
                
                if (strpos($html,'voor uw zoekopdracht') === FALSE)
                {
                    preg_match_all('/<h3>(.*?)<\/h3>/smi',$html,$output);
                    preg_match_all('/<ul class="kvk-meta">(.*?)<\/ul>/smi',$html,$output2);
                    preg_match('/<div class="feedback">(\d*?) resultaten/smi',$html,$found);
                    if (!empty($found[1]))
                    {
                        scraperwiki::save_var('found', $found[1]);
            
                        unset($output[1][0]);
                        $k = 0;
                        foreach($output[1] as $key=>$value)
                        {
                            $id = 0;
                
                            $tdata = explode("<li>",trim($output2[1][$k]));
                            $id = trim(str_replace('KVK','',strip_tags($tdata[1])));
                            if (!empty($id))
                            {
                                $data = array(
                                    'id' => $id,
                                    'name'=>strip_tags($value),
                                    'internal' => trim(str_replace('Vestigingsnr.','',strip_tags($tdata[2]))),
                                    'address' => trim(strip_tags($tdata[3])),
                                    'location' => trim(strip_tags($tdata[4])).' '.trim(strip_tags($tdata[5])),
                                    'type' => trim(strip_tags($tdata[6])),
                                    'time' => time(),
                                );
                                scraperwiki::save_sqlite(array('id'), $data);
                            }
                           $k++;
                            if ($i+1 >= (int)$found[1])
                            {
                                $flag = false;
                            }
                        }
                    }
                    else
                    {
                        $flag = false;
                    }
                }
                else
                {
                    $flag = false;
                }
                $i+=5;
                scraperwiki::save_var('last_page', $i);
            }
        }
    }
}
    
?>

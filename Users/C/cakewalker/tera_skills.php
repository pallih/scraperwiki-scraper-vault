<?php
    $classes = array('Archer'/*,'Beserker','Lancer','Mystic','Priest','Slayer','Sorcerer','Warrior'*/);
    //scraperwiki::sqliteexecute("create table tera_skills(`name`, `cast_time`,`skill_power`, `mana_cost`,`cool_down`, `detail`,`cost`)"); 
    //scraperwiki::sqliteexecute("drop table tera_skills"); 
    //die('SQLLite Setup Die');
    foreach($classes as $key => $job)
    {
        $class_name = $job;
        $id = $key+1;
        $url = "http://teracodex.com/skill.php?class=";
        $html = scraperWiki::scrape($url . $id);
        require_once 'scraperwiki/simple_html_dom.php';           
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find('table.itemList tr') as $row)
        {
            $tds = $row->find("td");
            $id = $row->find("td.tn a.codexToolTip");

            $record = array(
                'item_id' => $id[0]->attr['href'],
                'skill_name' => $tds[0]->plaintext,
                
            );
            $base_url = "http://teracodex.com";
            $new_html = scraperWiki::scrape($base_url . $record['item_id']);
            
            $skill_dom = new simple_html_dom();
            $skill_dom->load($new_html);

            foreach($skill_dom->find("div#content-inner") as $skill_row)
            {
                $name = $skill_row->find(" div.codex-window-box div.name");
                
                $divs = $skill_row->find(" div.codex-window-box table.stat tr td.stls + td");
                $derp = count($divs);

                $cost = $skill_row->find(" div.box-right div.item-page-details ul li:last div");
                $desc = $skill_row->find(" div.codex-window-box div.desc");
                echo $divs[0];
                die;
                if($derp == 2){
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => '',
                    'mana_cost' => '',
                    'skill_power' => $divs[5]->plaintext,
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );
                }elseif($derp == 3){
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => $divs[5]->plaintext,
                    'mana_cost' => $divs[7]->plaintext,
                    'skill_power' => '',
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );

                }else {
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => $divs[5]->plaintext,
                    'mana_cost' => $divs[7]->plaintext,
                    'skill_power' => $divs[9]->plaintext,
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );
                }
                scraperwiki::save_sqlite(array(), $skill_record, 'tera_skills');

                
            }
        }
        
    }

?>
<?php
    $classes = array('Archer'/*,'Beserker','Lancer','Mystic','Priest','Slayer','Sorcerer','Warrior'*/);
    //scraperwiki::sqliteexecute("create table tera_skills(`name`, `cast_time`,`skill_power`, `mana_cost`,`cool_down`, `detail`,`cost`)"); 
    //scraperwiki::sqliteexecute("drop table tera_skills"); 
    //die('SQLLite Setup Die');
    foreach($classes as $key => $job)
    {
        $class_name = $job;
        $id = $key+1;
        $url = "http://teracodex.com/skill.php?class=";
        $html = scraperWiki::scrape($url . $id);
        require_once 'scraperwiki/simple_html_dom.php';           
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find('table.itemList tr') as $row)
        {
            $tds = $row->find("td");
            $id = $row->find("td.tn a.codexToolTip");

            $record = array(
                'item_id' => $id[0]->attr['href'],
                'skill_name' => $tds[0]->plaintext,
                
            );
            $base_url = "http://teracodex.com";
            $new_html = scraperWiki::scrape($base_url . $record['item_id']);
            
            $skill_dom = new simple_html_dom();
            $skill_dom->load($new_html);

            foreach($skill_dom->find("div#content-inner") as $skill_row)
            {
                $name = $skill_row->find(" div.codex-window-box div.name");
                
                $divs = $skill_row->find(" div.codex-window-box table.stat tr td.stls + td");
                $derp = count($divs);

                $cost = $skill_row->find(" div.box-right div.item-page-details ul li:last div");
                $desc = $skill_row->find(" div.codex-window-box div.desc");
                echo $divs[0];
                die;
                if($derp == 2){
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => '',
                    'mana_cost' => '',
                    'skill_power' => $divs[5]->plaintext,
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );
                }elseif($derp == 3){
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => $divs[5]->plaintext,
                    'mana_cost' => $divs[7]->plaintext,
                    'skill_power' => '',
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );

                }else {
                  $skill_record = array(
                    'name' => $name[0]->plaintext,
                    'cast_time' => $divs[3]->plaintext,
                    'cool_down' => $divs[5]->plaintext,
                    'mana_cost' => $divs[7]->plaintext,
                    'skill_power' => $divs[9]->plaintext,
                    'detail' => $desc[0]->plaintext,
                    'cost' => $cost[0]->plaintext,
                  );
                }
                scraperwiki::save_sqlite(array(), $skill_record, 'tera_skills');

                
            }
        }
        
    }

?>

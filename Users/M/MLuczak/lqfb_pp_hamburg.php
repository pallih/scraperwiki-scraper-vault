<?php

require 'scraperwiki/simple_html_dom.php';

function crawlAreaPage($area_name, $url, $area_state_name, $base_page){
    $issues_tbl_name = "issues";
    $initiatives_tbl_name = "initiatives";
    $suggestions_tbl_name = "suggestions";
    $pagination = 0;
    $latest = "";
    while(true){      
        $pagination = $pagination + 1;
        $area_content = scraperwiki::scrape($url."&page=".$pagination);

        $area_html = str_get_html($area_content);
        $new = $area_html->find("a.issue_id",0);
        if(strcmp($latest,$new->innertext) == 0) break;
        $latest = $new->innertext;
        //crawl issues
        foreach ($area_html->find("div.issue") as $next_issue) {
            if(count(scraperwiki::select("* from crawled where url='".str_replace("../..",$base_page,$next_issue->children(1)->children(0)->href)."'")) == 0){
                $issue_content = scraperwiki::scrape(str_replace("../..",$base_page,$next_issue->children(1)->children(0)->href));
                $issue_html = str_get_html($issue_content);
                foreach ($issue_html->find("div.issue") as $this_issue) {
                    $issue_title = $this_issue->children(0)->children(0)->innertext;
                    $data=array("title"=>$issue_title ,"area"=>$area_name,"state"=>$area_state_name);
                    //save the issues
                    scraperwiki::save_sqlite(array("title"), $data, $table_name=$issues_tbl_name);
                    unset($data);
                    //crawl initiatives of issues
                    foreach ($this_issue->find("div.initiative") as $next_initiative) {
                        $ini_id = preg_match("/([0-9]*)\.html/",$next_initiative->children(2)->first_child()->href,$matches);
                        if(count(scraperwiki::select("* from crawled where url='".str_replace("../..",$base_page,$next_initiative->children(2)->first_child()->href)."'")) == 0){
                            $sug_pagination = 1;
                            $initiative_content = scraperwiki::scrape(str_replace("../..",$base_page,$next_initiative->children(2)->first_child()->href)."&page=".$sug_pagination);
                            $initiative_html = str_get_html($initiative_content);
                            $initiative_title = $initiative_html->find("div.slot_default div.title",0)->innertext;
                            //iterate versions
                            $initiative_versions_content = scraperwiki::scrape($base_page."/draft/list.html?initiative_id=".$matches[1]);
                            $initiative_versions_html = str_get_html($initiative_versions_content);
                            $following_v = "";
                            foreach ($initiative_versions_html->find("form tr.ui_list_row") as $next_version) {
                                $initiative_text = "";
                                //inititative text
                                $temp = explode(" ",$next_version->children(0)->first_child()->innertext);
                                $date = explode(".",$temp[0]);
                                $time = explode(":",$temp[1]);
                                $tstamp = mktime($time[0],$time[1],$time[2],$date[0],$date[1],$date[2]);
                                $link = str_replace("..",$base_page,$next_version->children(2)->first_child()->href);
                                $initiative_version_content = scraperwiki::scrape($link);
                                $initiative_version_html = str_get_html($initiative_version_content);
                                $this_initiative = $initiative_version_html->find("div.slot_default",0);
                                $initiative_text = $this_initiative->find("div.draft_content",0)->plaintext;
                                $data=array("title"=>$initiative_title ,"txt"=>$initiative_text,"issue"=>$issue_title,"parent"=>$following_v,"tstamp"=>$tstamp);
                                scraperwiki::save_sqlite(array("title","tstamp"), $data, $table_name=$initiatives_tbl_name);
                                unset($data);
                                $following_v = $link;
                            }
                            //suggestions for initiative
                            $this_suggestions = $initiative_html->find("div.initiative_head",1);                    
                            foreach ($this_suggestions->find("tr.ui_list_row") as $next_suggestion) {
                                if(count(scraperwiki::select("* from crawled where url='".str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href)."'")) == 0){
                                    $suggestion_content = scraperwiki::scrape(str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href));
                                    $suggestion_html = str_get_html($suggestion_content);
                                    $suggestion_text = "";
                                    $this_suggestion = $suggestion_html->find("div.ui_tabs_content",0);
                                    $author = $this_suggestion->first_child()->first_child()->children(1)->innertext;
                                    $title = $this_suggestion->first_child()->children(1)->children(1)->innertext;
                                    $suggestion_text = $this_suggestion->first_child()->children(2)->plaintext;
                                    $data=array("author"=>$author, "title"=> $title,"txt"=>$suggestion_text,"initiative"=>$initiative_title);
                                    scraperwiki::save_sqlite(array("author","title","initiative"), $data, $table_name=$suggestions_tbl_name);
                                    unset($data);
                                    scraperwiki::save_sqlite(array("url"), array("url"=>str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href)), $table_name="crawled");
                                }
                            }
                            while(true){
                                if(count($this_suggestions->find("tr.ui_list_row",0))>0) $sug_latest = $this_suggestions->find("tr.ui_list_row",0)->children(1)->first_child()->href;
                                else break;
                                $sug_pagination = $sug_pagination + 1;
                                $initiative_content = scraperwiki::scrape(str_replace("../..",$base_page,$next_initiative->children(2)->first_child()->href)."&page=".$sug_pagination);
                                $initiative_html = str_get_html($initiative_content);
                                $this_suggestions = $initiative_html->find("div.initiative_head",1);
                                $sug_new = $this_suggestions->find("tr.ui_list_row",0)->children(1)->first_child()->href;
                                if(strcmp($sug_latest,$sug_new) == 0) break;
                                foreach ($this_suggestions->find("tr.ui_list_row") as $next_suggestion) {
                                    if(count(scraperwiki::select("* from crawled where url='".str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href)."'")) == 0){
                                        $suggestion_content = scraperwiki::scrape(str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href));
                                        $suggestion_html = str_get_html($suggestion_content);
                                        $suggestion_text = "";
                                        $this_suggestion = $suggestion_html->find("div.ui_tabs_content",0);
                                        $author = $this_suggestion->first_child()->first_child()->children(1)->innertext;
                                        $title = $this_suggestion->first_child()->children(1)->children(1)->innertext;
                                        $suggestion_text = $this_suggestion->first_child()->children(2)->plaintext;
                                        $data=array("author"=>$author, "title"=> $title,"txt"=>$suggestion_text,"initiative"=>$initiative_title);
                                        scraperwiki::save_sqlite(array("author","title","initiative"), $data, $table_name=$suggestions_tbl_name);
                                        unset($data);
                                        scraperwiki::save_sqlite(array("url"), array("url"=>str_replace("../..",$base_page,$next_suggestion->children(1)->first_child()->href)), $table_name="crawled");
                                    }
                                }
                                $sug_latest = $sug_new;
                                scraperwiki::save_sqlite(array("url"), array("url"=>str_replace("../..",$base_page,$next_initiative->children(2)->first_child()->href)), $table_name="crawled");
                            }
                        }
                    }
                }
            scraperwiki::save_sqlite(array("url"), array("url"=>str_replace("../..",$base_page,$next_issue->children(1)->children(0)->href)), $table_name="crawled");
            }
        }
    }
}

$base_page = "https://lqpp.de/hh";

//start at area pages and get all areas, counter of issue states, links to area pages for each state
$html_content = scraperwiki::scrape($base_page."/unit/show/1.html");
$html = str_get_html($html_content);

scraperwiki::sqliteexecute("create table if not exists crawled ('url' string)");
scraperwiki::sqliteexecute("create table if not exists topicoverview ('area' string, 'crawled' boolean)");

foreach ($html->find("div.area") as $el) {
    $area_name =  str_replace(" ", "_", $el->first_child()->first_child()->first_child()->innertext);
    $crawled = scraperwiki::select("* from topicoverview where area='".$area_name."' AND crawled=1");
    if((count($crawled) == 0) && (strpos($area_name,'Sandkasten') === false)){
        
        $data=array("area"=>$area_name,"crawled"=>true);
    
        foreach ($el->first_child()->next_sibling()->children() as $area_states) {
            $val = explode(" ", $area_states->innertext);
            $area_state_url = str_replace("amp;","",str_replace("../..", $base_page, $area_states->href));
            if(count($val) > 2){
                $area_state_name = str_replace(" ", "_", $val[1]. " " . $val[2]);
            }
            else{
                $area_state_name = $val[1];
            }
    
            crawlAreaPage($area_name, $area_state_url, $area_state_name, $base_page);
        }
        scraperwiki::save_sqlite(array("area"), $data, $table_name="topicoverview");
        unset($data);
    }
}

?>

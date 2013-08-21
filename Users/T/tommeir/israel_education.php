<?php
require  'scraperwiki/simple_html_dom.php';

/*$list = scraperWiki::scrape("http://cpo.co.il/tom/education_url2.txt");           
$urls = explode("\n", $list );      
print "start\n";
  foreach($urls as $url) {
    $record = array();
    $record['id'] = substr($url,58);
    scraperwiki::save(array('id'), $record);    
  }*/
//     scraperwiki::sqliteexecute("delete from swdata where id IS NULL");   
//$a = scraperwiki::sqliteexecute("delete from swdata where id IS NULL");  
//$swdata = (scraperwiki::select("* from swdata where id = 470591"));   
/*
$swdata = (scraperwiki::select("* from swdata where id IS NOT NULL AND education_type IS NULL AND legal_status IS NULL"));   
foreach($swdata as $data) {

    $url = 'http://hinuch.education.gov.il/imsnet/PirteiMosad.aspx?Sm=' . $data['id'];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
    $htmlParser = new simple_html_dom();
    $htmlParser->load($html);
    $data['name'] = $htmlParser->find("#ctl00_Main_ddShem",0)->innertext;
    $data['yeshuv'] = $htmlParser->find("#ctl00_Main_ddYeshuv",0)->innertext; 
    $data['address'] = $htmlParser->find("#ctl00_Main_HatabUc_LblKtovetMosad",0)->innertext;
    $data['city'] = $htmlParser->find("#ctl00_Main_HatabUc_LblYeshuvMosad",0)->innertext;
    $data['authority'] = $htmlParser->find("#ctl00_Main_HatabUc_LblReshutHinuch",0)->innertext;
    $data['mail_address'] = $htmlParser->find("#ctl00_Main_HatabUc_LblKtovetMihtav",0)->innertext;
    $data['zipcode'] = $htmlParser->find("#ctl00_Main_HatabUc_LblMikud",0)->innertext;
    $data['phone'] = $htmlParser->find("#ctl00_Main_HatabUc_LblTelMosad",0)->innertext;
    $data['fax'] = $htmlParser->find("#ctl00_Main_HatabUc_LblFaxMosad",0)->innertext;
    $data['manager_name'] = $htmlParser->find("#ctl00_Main_HatabUc_LblShemMinhel",0)->innertext;
    $data['supervisor_name'] = $htmlParser->find("#ctl00_Main_HatabUc_LblShemMifakeah",0)->innertext;

    $data['education_levels'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblShlav_Hinuch",0)->innertext;
    $data['education_type'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblSug_Hinuch",0)->innertext;
    $data['supervision_type'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblPikuach",0)->innertext;
    $data['migzat'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblMigzar",0)->innertext;
    $data['legal_status'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblMeamadMishpati",0)->innertext;
    $data['supervising_unit'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblDivuach",0)->innertext;
    $data['ownership'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblBealut",0)->innertext;
    $data['languages'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblSfatLimud",0)->innertext;
    $data['long_school_day'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblYocha",0)->innertext;
    $data['from_grade'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblMeShihva",0)->innertext;
    $data['to_grade'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblAdShihva",0)->innertext;
    $data['year_established'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblShnatYesod",0)->innertext;
    $data['supports_ofek_hadash'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblOfek",0)->innertext;
    $data['special_education_class'] = $htmlParser->find("#ctl00_Main_MeafieneiMosaduc_LblLakut",0)->innertext;
    @$data['description'] = $htmlParser->find("#ctl00_Main_mosadMatzig1_divTeurContent",0)->innertext;
    @$data['special_activities'] = $htmlParser->find("#ctl00_Main_mosadMatzig1_divPeilutContent",0)->innertext;
    @$data['website_link'] = $htmlParser->find("#ctl00_Main_mosadMatzig1_lnkMosad2",0)->href;
    @$data['file_link'] = $htmlParser->find("#ctl00_Main_mosadMatzig1_lnkKovets",0)->href;
    @$data['last_update'] = $htmlParser->find("#ctl00_Main_mosadMatzig1_lblIdkunAcharon",0)->href;
    @$data['authority_desv'] = $htmlParser->find("#ctl00_Main_rashutMatziga1_divTeurRashutContent",0)->innertext;
    @$data['authority_website_link'] = $htmlParser->find("#ctl00_Main_rashutMatziga1_lnkRashutAtar",0)->href;
    @$data['authority_file_link'] = $htmlParser->find("#ctl00_Main_rashutMatziga1_lnkRashutKovets",0)->href;
    @$data['authority_last_update'] = $htmlParser->find("#ctl00_Main_rashutMatziga1_lblRashutIdkun",0)->innertext;
    $data['PirteiMosad_page_extracted'] = 1;//mark attemp to scrape
    if(    $data['phone'] != "" ) $data['basic_extract_success'] = 1;  //mark attemp successfull

    $htmlParser->__destruct();

    $url2 = 'http://hinuch.education.gov.il/mddnet/MosadIFrame.aspx?semel=' . $data['id'];
    $html_content2 = scraperwiki::scrape($url2);
    $html2 = str_get_html($html_content2);
    $htmlParser2 = new simple_html_dom();
    $htmlParser2->load($html2);

    @$data['test_achievement_decile'] = $htmlParser2->find("div#spnAsironim table tbody tr td.number",0)->innertext;
    @$data['test_fairness_decile'] = $htmlParser2->find("div#spnAsironim table tbody tr td.number",1)->innertext;
    @$data['student_retention_decile'] = $htmlParser2->find("div#spnAsironim table tbody tr td.number",2)->innertext;
    @$data['helptext_decile1'] = $htmlParser2->find(".chaimText1",0)->innertext;    
    @$data['boys_recruit_percent'] = $htmlParser2->find("div#spnAsironim table[2] tbody tr td.number",0)->innertext;
    @$data['girls_recruit_percent'] = $htmlParser2->find("div#spnAsironim table[2] tbody tr td.number",1)->innertext;
    @$data['combatant_recruit_percent'] = $htmlParser2->find("div#spnAsironim table[2] tbody tr td.number",2)->innertext;
    @$data['army_help_text_decile2'] =  $htmlParser2->find(".chaimText2",1)->innertext;

    @$data['shiur_zakaim_lebagrut'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",0)->innertext;
    @$data['hefresh_zakaim_lebagrut_lelo_hinuh_meyuhad'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",1)->innertext;
    @$data['shiur_mitztainim'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",2)->innertext;
    @$data['english_pass_high_level_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",3)->innertext;
    @$data['math_pass_high_level_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",4)->innertext;
    @$data['civil_pass_all_levels_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",5)->innertext;
    @$data['mother_language_pass_all_levels_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",6)->innertext;
    @$data['bible_language_pass_all_levels_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",7)->innertext;
    @$data['literature_language_pass_all_levels_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",8)->innertext;
    @$data['history_language_pass_all_levels_percent'] = $htmlParser2->find("div#spnBehinot table tbody tr td.number",9)->innertext;
    @$data['percentage_update_date'] = $htmlParser2->find("div.idkun dl dd",0)->innertext;  
    //missing img from #ctl00_Main_mosadMatzig1_imgMosad
    if($data['test_achievement_decile'] != "") $data['MosadIFrame_page_extracted'] = 1; //mark succesful bagrut details extraction


    $htmlParser2->__destruct();  

     scraperwiki::save_sqlite(array('id'),$data);   


 
}*/

//name and city extract fix
$swdata = (scraperwiki::select("* from swdata where id IS NOT NULL AND name IS NULL"));   

foreach($swdata as $data) {

    $url = 'http://hinuch.education.gov.il/imsnet/PirteiMosad.aspx?Sm=' . $data['id'];
    $html_content = scraperwiki::scrape($url);
    $html = str_get_html($html_content);
    $htmlParser = new simple_html_dom();
    $htmlParser->load($html);

    $data['name'] = $htmlParser->find("#ctl00_Main_ddShem",0)->innertext;
    $data['yeshuv'] = $htmlParser->find("#ctl00_Main_ddYeshuv",0)->innertext; 
    if($data['name'] != "")   scraperwiki::save_sqlite(array('id'),$data);   
}

?>

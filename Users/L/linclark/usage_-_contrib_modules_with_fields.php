<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$modules = array('link','addressfield','addthis','title_image','asin','anonymous_posting_field','audiofield','availability_calendar','availability_calendar_booking_formlet','awesomerelationship','addressfield','commerce_customer','commerce_line_item','commerce_price','commerce_product_reference','backgroundfield','location_cck','barcode','bd_video','bible_field','biblio','birthdays','blob','blockreference','boolean','brightcove_field','button_field','buzzthis','cck_debug','cck_ipaddr','cck_list','cck_phone','cck_redirection','redirection','cck_table','cck_time','chatroom','civicrm_user_reference','cjunction_fields','cmis_field','codes','combo_box','commentfield','commentreference','commerce_customer','commerce_line_item','commerce_price','commerce_product_reference','commerce_coupon','commerce_file','commerce_installments','commerce_option_set_reference','commerce_order_reference','commerce_price_history','commerce_price_table','compass_rose','computed_field','content_approval_field','context_field','countries','ctr_field','d2c_core','danger_rose','addressfield','computed_field','date','field_collection','geofield','i18n_field_i18n','link','ogdi_field','node_reference','user_reference','udid','datastore_field','datastore_field_datastore','date','date_time_field','deviantart_embed','dnd_fields','double_field','download','drealty_image','dynamic_formatters','ecard','email','encset','entityreference','field_example','faqfield','field_collection','field_form','field_ipaddress','field_nif','field_reference','field_views','file','fivestar','fixed_field','flag_entity','flashcard','flattr','flickrfield','font_reference','formatter_field','formatter_reference','freeform','forms_attach_field','geofield','geolocation','geshifield','getlocations_fields','gm3_field','gm3_region_field','gmap_cck','google_weather','googleplus','graphviz_noderef_field','hms_field','hotfolder_action_config','i18n_field_i18n','iframe','imagefield_crop','integerdate','interval','is_useful','itoggle_field','jquery_colorpicker','jsmap','field_kaltura','languagefield','link','location_cck','machine_name','makemeeting','markup','mediafield','menu_link','metatags_quick','mm_cck','date','link','metatags_quick','i18n_field_i18n','multiple_email','mcapi','myepisodes','mytinytodo','name','namecards_address_field','namecards_fax_field','namecards_phone_field','nlmfield','nodeaccess_password','nodereference_count','nodereferrer','notes_path_info','npr_fields','numeric_interval','office_hours','og_role_field','ogdi_field','ooyala','ooyala_markers','openlayers_field','opentok','partial_date','party_hat','pdf_to_image','percentage','phone','physical','piwik_stats','pollfield','choices','postal_field','postgis','profile2_privacy','properties','quizzler_multi_quizzler','radioactivity','node_reference','user_reference','registration','relation_dummy_field','relation_endpoint','relation_select','relevant_content','reply','resource_booking','revisionreference','role_field','rolereference','rooms_availability_reference','safeword','sarnia','serial','sheetnode','signaturefield','socialshareprivacy','soundcloudfield','sparql_views_related_resource','spotifyfield','starrating','storypal','submit_field','survey_builder','tablefield','temperature','template_field','term_level','textintegerfield','textintegerfieldx2url','timefield','token_field','transliteration_title','tweetbutton','twitter_username','tzfield','urlcontentfield','viddler','video','video_embed_field','video_filter_field','video_upload','viewfield','viewreference','vimeo','vud_field','webcam','rsapublickey','website_screenshot','youtube');

foreach ($modules as $module) {
    $uri = "http://drupal.org/project/usage/" . $module;
    $content = scraperwiki::scrape($uri); 
    $dom->load($content);

    $thead = $dom->find('#project-usage-project-api thead tr', 0);
    $row = $dom->find('#project-usage-project-api tbody tr.odd', 0);
    if (!empty($row)) {
        $headers = $thead->find('th');
        foreach ($headers as $index => $header) {
            if ($header->innertext == '7.x') {
                $index_7 = $index;
            }
            if ($header->innertext == 'Total') {
                $index_total = $index;
            }
        }
        $usage = $row->find('td');
        $count = count($usage);
        $version_total = $usage[$index_total];
        $version_7 = $usage[$index_7];

        $record = array(
            'module' => $module,
            'total' => $version_total->innertext,
            'seven' => $version_7->innertext,
        );

        scraperwiki::save(array('module'), $record);
    }
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

$modules = array('link','addressfield','addthis','title_image','asin','anonymous_posting_field','audiofield','availability_calendar','availability_calendar_booking_formlet','awesomerelationship','addressfield','commerce_customer','commerce_line_item','commerce_price','commerce_product_reference','backgroundfield','location_cck','barcode','bd_video','bible_field','biblio','birthdays','blob','blockreference','boolean','brightcove_field','button_field','buzzthis','cck_debug','cck_ipaddr','cck_list','cck_phone','cck_redirection','redirection','cck_table','cck_time','chatroom','civicrm_user_reference','cjunction_fields','cmis_field','codes','combo_box','commentfield','commentreference','commerce_customer','commerce_line_item','commerce_price','commerce_product_reference','commerce_coupon','commerce_file','commerce_installments','commerce_option_set_reference','commerce_order_reference','commerce_price_history','commerce_price_table','compass_rose','computed_field','content_approval_field','context_field','countries','ctr_field','d2c_core','danger_rose','addressfield','computed_field','date','field_collection','geofield','i18n_field_i18n','link','ogdi_field','node_reference','user_reference','udid','datastore_field','datastore_field_datastore','date','date_time_field','deviantart_embed','dnd_fields','double_field','download','drealty_image','dynamic_formatters','ecard','email','encset','entityreference','field_example','faqfield','field_collection','field_form','field_ipaddress','field_nif','field_reference','field_views','file','fivestar','fixed_field','flag_entity','flashcard','flattr','flickrfield','font_reference','formatter_field','formatter_reference','freeform','forms_attach_field','geofield','geolocation','geshifield','getlocations_fields','gm3_field','gm3_region_field','gmap_cck','google_weather','googleplus','graphviz_noderef_field','hms_field','hotfolder_action_config','i18n_field_i18n','iframe','imagefield_crop','integerdate','interval','is_useful','itoggle_field','jquery_colorpicker','jsmap','field_kaltura','languagefield','link','location_cck','machine_name','makemeeting','markup','mediafield','menu_link','metatags_quick','mm_cck','date','link','metatags_quick','i18n_field_i18n','multiple_email','mcapi','myepisodes','mytinytodo','name','namecards_address_field','namecards_fax_field','namecards_phone_field','nlmfield','nodeaccess_password','nodereference_count','nodereferrer','notes_path_info','npr_fields','numeric_interval','office_hours','og_role_field','ogdi_field','ooyala','ooyala_markers','openlayers_field','opentok','partial_date','party_hat','pdf_to_image','percentage','phone','physical','piwik_stats','pollfield','choices','postal_field','postgis','profile2_privacy','properties','quizzler_multi_quizzler','radioactivity','node_reference','user_reference','registration','relation_dummy_field','relation_endpoint','relation_select','relevant_content','reply','resource_booking','revisionreference','role_field','rolereference','rooms_availability_reference','safeword','sarnia','serial','sheetnode','signaturefield','socialshareprivacy','soundcloudfield','sparql_views_related_resource','spotifyfield','starrating','storypal','submit_field','survey_builder','tablefield','temperature','template_field','term_level','textintegerfield','textintegerfieldx2url','timefield','token_field','transliteration_title','tweetbutton','twitter_username','tzfield','urlcontentfield','viddler','video','video_embed_field','video_filter_field','video_upload','viewfield','viewreference','vimeo','vud_field','webcam','rsapublickey','website_screenshot','youtube');

foreach ($modules as $module) {
    $uri = "http://drupal.org/project/usage/" . $module;
    $content = scraperwiki::scrape($uri); 
    $dom->load($content);

    $thead = $dom->find('#project-usage-project-api thead tr', 0);
    $row = $dom->find('#project-usage-project-api tbody tr.odd', 0);
    if (!empty($row)) {
        $headers = $thead->find('th');
        foreach ($headers as $index => $header) {
            if ($header->innertext == '7.x') {
                $index_7 = $index;
            }
            if ($header->innertext == 'Total') {
                $index_total = $index;
            }
        }
        $usage = $row->find('td');
        $count = count($usage);
        $version_total = $usage[$index_total];
        $version_7 = $usage[$index_7];

        $record = array(
            'module' => $module,
            'total' => $version_total->innertext,
            'seven' => $version_7->innertext,
        );

        scraperwiki::save(array('module'), $record);
    }
}
?>

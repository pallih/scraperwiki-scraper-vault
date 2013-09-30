<?php

require 'scraperwiki/simple_html_dom.php'; 
    
$data = json_decode(scraperwiki::scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=mediaqueries&query=select%20*%20from%20swdata'));
//$data = json_decode(scraperwiki::scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=mediaqueries&query=select%20*%20from%20swdata%20limit%205'));

$pagesThatThrowsError = array("http://www.sony.com/index.php", "http://acescholarships.org/", "http://yiibu.com/", "http://citycrawlers.eu/berlin/");

//Convert data into strings and urls
foreach ($data as $object) {

    $site=array();
    
    foreach($object as $member=>$data)
    {
        $site[$member]=$data;
    }   

    if ($site["a_pagenumber"] >= 1 && !in_array($site["a_url"], $pagesThatThrowsError) ) {
        print $site["a_pagenumber"] . " " . $site["a_url"] . "\n";         

        $html_content = scraperwiki::scrape($site["a_url"]);
        $html = str_get_html($html_content);

        // Get the doctype
        foreach ($html->find("unknown") as $unknownEL) {
            if ($unknownEL->parent()->tag == 'root') {
                $site["b_doctype"] = strtoupper($unknownEL);
            }
        }
        
    
    // ===========================================================
    // Find html5 elements
    // ===========================================================
    
        // Header
        $headerCount = 0;
        foreach ($html->find("header") as $header) {
            $headerCount += 1;
            if ($headerCount <= 9) {
                $site["c$headerCount_headerTypet"] = "header";
                $site["c$headerCount_headerRole"] = $header->getAttribute("role");
                $site["c$headerCount_headerClass"] = $header->getAttribute("class");
                $site["c$headerCount_headerID"] = $header->getAttribute("id");
            }
        }
        $site["ca_headerCount"] = $headerCount;
        
        // Footer
        $footerCount = 0;
        foreach ($html->find("footer") as $footer) {
            $footerCount += 1;
            if ($footerCount <= 9) {
                $site["d$footerCount_footerTypet"] = "footer";
                $site["d$footerCount_footerRole"] = $footer->getAttribute("role");
                $site["d$footerCount_footerClass"] = $footer->getAttribute("class");
                $site["d$footerCount_footerID"] = $footer->getAttribute("id");
            }
        }
        $site["da_footerCount"] = $footerCount;
    
        // Aside
        $asideCount = 0;
        foreach ($html->find("aside") as $aside) {
            $asideCount += 1;
            if ($asideCount <= 9) {
                $site["e$asideCount_asideTypet"] = "aside";
                $site["e$asideCount_asideRole"] = $aside->getAttribute("role");
                $site["e$asideCount_asideClass"] = $aside->getAttribute("class");
                $site["e$asideCount_asideID"] = $aside->getAttribute("id");
            }
        }
        $site["ea_asideCount"] = $asideCount;

        // Nav
        $navCount = 0;
        foreach ($html->find("nav") as $nav) {
            $navCount += 1;
            if ($navCount <= 9) {
                $site["f$navCount_navTypet"] = "nav";
                $site["f$navCount_navRole"] = $nav->getAttribute("role");
                $site["f$navCount_navClass"] = $nav->getAttribute("class");
                $site["f$navCount_navID"] = $nav->getAttribute("id");
            }
        }
        $site["fa_navCount"] = $navCount;
    
        // Articles
        $articleCout = 0;
        foreach ($html->find("article") as $article) {
            $articleCout += 1;
        }
        
        $site["g_articleCount"] = $articleCout;
     
        // Section
        $sectionCount = 0;
        foreach ($html->find("section") as $section) {
            $sectionCount += 1;
        }
        
        $site["h_sectionCount"] = $sectionCount; 
        
    
    // ===========================================================
    // !END --- Find html5 elements
    // ===========================================================
    
        $allClasses = array();
        $allIDs = array();   
    
        $mainCount = 0;

        foreach ($html->find("div") as $div) {
           
            // ===========================================================
            // Find roles that are not tied to specific elements
            // ===========================================================
            
            // role="main"
            $opservedNames = array("main", "maincol", "primary-content", "maincontent", "primaryContent", "main-row");
            if ($div->getAttribute("role") == "main" || in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                $mainCount += 1;
                if ($mainCount <= 9) {
                    $site["i$mainCount_mainType"] = "div";
                    $site["i$mainCount_mainRole"] = $div->getAttribute("role");
                    $site["i$mainCount_mainClass"] = $div->getAttribute("class");
                    $site["i$mainCount_mainID"] = $div->getAttribute("id");
                }
            }
    
            // Header
            if (!$html->find("header")) {
                $opservedNames = array("header", "masthead");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $headerCount += 1;
                    if ($headerCount <= 9) {
                        $site["c$headerCount_headerType"] = "div";
                        $site["c$headerCount_headerRole"] = $div->getAttribute("role");
                        $site["c$headerCount_headerClass"] = $div->getAttribute("class");
                        $site["c$headerCount_headerID"] = $div->getAttribute("id");
                    }
                }
            }
            
            // Footer
            if (!$html->find("footer")) {
                $opservedNames = array("footer");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $footerCount += 1;
                    if ($headerCount <= 9) {
                        $site["d$footerCount_footerType"] = "div";
                        $site["d$footerCount_footerRole"] = $div->getAttribute("role");
                        $site["d$footerCount_footerClass"] = $div->getAttribute("class");
                        $site["d$footerCount_footerID"] = $div->getAttribute("id");
                    }
                }
            }

            // Nav
            if (!$html->find("nav")) {
                $opservedNames = array("nav", "globalnav", "navigation", "navbar", "navcontainer", "navwrapper");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $navCount += 1;
                    if ($navCount <= 9) {
                        $site["e$navCount_navType"] = "div";
                        $site["e$navCount_navRole"] = $div->getAttribute("role");
                        $site["e$navCount_navClass"] = $div->getAttribute("class");
                        $site["e$navCount_navID"] = $div->getAttribute("id");
                    }
                }
            }
            
            // Make a list of all classes and one of all ids
            $allClasses[] = $div->getAttribute("class");
            $allIDs[] = $div->getAttribute("id");       
        }

        $site["i_mainCount"] = $mainCount;
        $site["c_headerCount"] = $headerCount;
        $site["d_footerCount"] = $footerCount;
        $site["e_navCount"] = $navCount;
    
        // Delete dublicates in allClasses and allIDs
        $allClassesResult = array_unique($allClasses);
        $allIDsResult = array_unique($allIDs);
    
        // Implode allClassesResult and allIDsResult to comma seperated string and save to side
        $site["allClasses"] = implode(", ",$allClassesResult);
        $site["allIDs"] = implode(", ",$allIDsResult);
    
    
        // Save data
        scraperwiki::save_sqlite(array("a_name"),$site);
    }
}


?>
<?php

require 'scraperwiki/simple_html_dom.php'; 
    
$data = json_decode(scraperwiki::scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=mediaqueries&query=select%20*%20from%20swdata'));
//$data = json_decode(scraperwiki::scrape('https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=mediaqueries&query=select%20*%20from%20swdata%20limit%205'));

$pagesThatThrowsError = array("http://www.sony.com/index.php", "http://acescholarships.org/", "http://yiibu.com/", "http://citycrawlers.eu/berlin/");

//Convert data into strings and urls
foreach ($data as $object) {

    $site=array();
    
    foreach($object as $member=>$data)
    {
        $site[$member]=$data;
    }   

    if ($site["a_pagenumber"] >= 1 && !in_array($site["a_url"], $pagesThatThrowsError) ) {
        print $site["a_pagenumber"] . " " . $site["a_url"] . "\n";         

        $html_content = scraperwiki::scrape($site["a_url"]);
        $html = str_get_html($html_content);

        // Get the doctype
        foreach ($html->find("unknown") as $unknownEL) {
            if ($unknownEL->parent()->tag == 'root') {
                $site["b_doctype"] = strtoupper($unknownEL);
            }
        }
        
    
    // ===========================================================
    // Find html5 elements
    // ===========================================================
    
        // Header
        $headerCount = 0;
        foreach ($html->find("header") as $header) {
            $headerCount += 1;
            if ($headerCount <= 9) {
                $site["c$headerCount_headerTypet"] = "header";
                $site["c$headerCount_headerRole"] = $header->getAttribute("role");
                $site["c$headerCount_headerClass"] = $header->getAttribute("class");
                $site["c$headerCount_headerID"] = $header->getAttribute("id");
            }
        }
        $site["ca_headerCount"] = $headerCount;
        
        // Footer
        $footerCount = 0;
        foreach ($html->find("footer") as $footer) {
            $footerCount += 1;
            if ($footerCount <= 9) {
                $site["d$footerCount_footerTypet"] = "footer";
                $site["d$footerCount_footerRole"] = $footer->getAttribute("role");
                $site["d$footerCount_footerClass"] = $footer->getAttribute("class");
                $site["d$footerCount_footerID"] = $footer->getAttribute("id");
            }
        }
        $site["da_footerCount"] = $footerCount;
    
        // Aside
        $asideCount = 0;
        foreach ($html->find("aside") as $aside) {
            $asideCount += 1;
            if ($asideCount <= 9) {
                $site["e$asideCount_asideTypet"] = "aside";
                $site["e$asideCount_asideRole"] = $aside->getAttribute("role");
                $site["e$asideCount_asideClass"] = $aside->getAttribute("class");
                $site["e$asideCount_asideID"] = $aside->getAttribute("id");
            }
        }
        $site["ea_asideCount"] = $asideCount;

        // Nav
        $navCount = 0;
        foreach ($html->find("nav") as $nav) {
            $navCount += 1;
            if ($navCount <= 9) {
                $site["f$navCount_navTypet"] = "nav";
                $site["f$navCount_navRole"] = $nav->getAttribute("role");
                $site["f$navCount_navClass"] = $nav->getAttribute("class");
                $site["f$navCount_navID"] = $nav->getAttribute("id");
            }
        }
        $site["fa_navCount"] = $navCount;
    
        // Articles
        $articleCout = 0;
        foreach ($html->find("article") as $article) {
            $articleCout += 1;
        }
        
        $site["g_articleCount"] = $articleCout;
     
        // Section
        $sectionCount = 0;
        foreach ($html->find("section") as $section) {
            $sectionCount += 1;
        }
        
        $site["h_sectionCount"] = $sectionCount; 
        
    
    // ===========================================================
    // !END --- Find html5 elements
    // ===========================================================
    
        $allClasses = array();
        $allIDs = array();   
    
        $mainCount = 0;

        foreach ($html->find("div") as $div) {
           
            // ===========================================================
            // Find roles that are not tied to specific elements
            // ===========================================================
            
            // role="main"
            $opservedNames = array("main", "maincol", "primary-content", "maincontent", "primaryContent", "main-row");
            if ($div->getAttribute("role") == "main" || in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                $mainCount += 1;
                if ($mainCount <= 9) {
                    $site["i$mainCount_mainType"] = "div";
                    $site["i$mainCount_mainRole"] = $div->getAttribute("role");
                    $site["i$mainCount_mainClass"] = $div->getAttribute("class");
                    $site["i$mainCount_mainID"] = $div->getAttribute("id");
                }
            }
    
            // Header
            if (!$html->find("header")) {
                $opservedNames = array("header", "masthead");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $headerCount += 1;
                    if ($headerCount <= 9) {
                        $site["c$headerCount_headerType"] = "div";
                        $site["c$headerCount_headerRole"] = $div->getAttribute("role");
                        $site["c$headerCount_headerClass"] = $div->getAttribute("class");
                        $site["c$headerCount_headerID"] = $div->getAttribute("id");
                    }
                }
            }
            
            // Footer
            if (!$html->find("footer")) {
                $opservedNames = array("footer");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $footerCount += 1;
                    if ($headerCount <= 9) {
                        $site["d$footerCount_footerType"] = "div";
                        $site["d$footerCount_footerRole"] = $div->getAttribute("role");
                        $site["d$footerCount_footerClass"] = $div->getAttribute("class");
                        $site["d$footerCount_footerID"] = $div->getAttribute("id");
                    }
                }
            }

            // Nav
            if (!$html->find("nav")) {
                $opservedNames = array("nav", "globalnav", "navigation", "navbar", "navcontainer", "navwrapper");
                if (in_array($div->getAttribute("class"), $opservedNames) || in_array($div->getAttribute("id"), $opservedNames)) {
                    $navCount += 1;
                    if ($navCount <= 9) {
                        $site["e$navCount_navType"] = "div";
                        $site["e$navCount_navRole"] = $div->getAttribute("role");
                        $site["e$navCount_navClass"] = $div->getAttribute("class");
                        $site["e$navCount_navID"] = $div->getAttribute("id");
                    }
                }
            }
            
            // Make a list of all classes and one of all ids
            $allClasses[] = $div->getAttribute("class");
            $allIDs[] = $div->getAttribute("id");       
        }

        $site["i_mainCount"] = $mainCount;
        $site["c_headerCount"] = $headerCount;
        $site["d_footerCount"] = $footerCount;
        $site["e_navCount"] = $navCount;
    
        // Delete dublicates in allClasses and allIDs
        $allClassesResult = array_unique($allClasses);
        $allIDsResult = array_unique($allIDs);
    
        // Implode allClassesResult and allIDsResult to comma seperated string and save to side
        $site["allClasses"] = implode(", ",$allClassesResult);
        $site["allIDs"] = implode(", ",$allIDsResult);
    
    
        // Save data
        scraperwiki::save_sqlite(array("a_name"),$site);
    }
}


?>

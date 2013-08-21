<?php
/*

  ###      ###
 #   ######   #
 #            #
 #   ######   #
 #            #
 #            #
#   #      #   #
#   #      #   #
#      ##      #
 ##    ##    ##
   ##########

Code by @ColinWren
*/

//Variables to make it easier to make your own
$postcode = "hu1"; // Enter any valid UK postcode. Be sure to remove any spaces
$apikey = "SGKFVWMW"; // Enter your API Key you'll need to get this from NHS Choices
$radius = "50"; //This can be any value between 0 and 100 (in km)
$orgType = "gppractices"; //Enter a CSV list of values you can choose from [ambulancetrusts][gppractices][hospitals][dentists][acutetrusts][primarycaretrusts][caretrusts][mentalhealthtrusts][independentsectororganisations][pharmacies][opticians]
        
//Now lets grab them datas
//Make sure that the values in the list are actually the right ones

//Setup the XML document we're going to read
$domdoc = new DOMDocument(); //New DOM doc for parsing the XML
$xmlurl = "http://v1.syndication.nhschoices.nhs.uk/organisations/".$orgType."/postcode/".$postcode.".xml?apikey=".$apikey."&range=".$radius; //The URL for XML
$replaceurl = "http://v1.syndication.nhschoices.nhs.uk/organisations/".$orgType."/postcode/".$postcode."?apikey=".$apikey."&range=".$radius; //The replacement URL for some reason NHS Choices doesn't return a datatype for pages
$domdoc->load($xmlurl); // Load the XML

//See how many data there is
$pages = 0; //Set up pages variable
$linknodes = $domdoc->getElementsByTagName("link"); // The number of pages for a search is stored in a bunch of link nodes
foreach($linknodes as $linknode){ // Go through said link nodes
    if($linknode->getAttribute("rel") == "last"){ // The number of pages is stored in the node with the last attribute
        $pages = substr($linknode->getAttribute("href"),strlen($replaceurl."&page=")); // grab the last page which we'll use to determine the number of pages
    }
}

//Load the information from this first page of the search results
$entrynodes = $domdoc->getElementsByTagName("entry"); // Each search result is stored in the entry node
foreach($entrynodes as $entrynode){ // Go through all these entry nodes
    //Grab the title for the entry
    $titles = $entrynode->getElementsByTagName("title");
    $title = $titles->item(0)->nodeValue; // The title is stored in the title node [crazy eh?]

    //Grab the NHS Choices link & the profile data link
    $entrylinknodes = $entrynode->getElementsByTagName("link"); //There are a bunch of link nodes we want the one with the alternate rel attribute
    $nhschoiceslink = ""; //A placeholder for the link
    $ratingslink = ""; //A placeholder for the link
    foreach($entrylinknodes as $entrylinknode){ //Go through the link nodes
        if($entrylinknode->getAttribute("rel") == "alternate"){ //Find the alternate node which containts the nhs choices link
            $nhschoiceslink = $entrylinknode->getAttribute("href"); //Get the value
        }
        if($entrylinknode->getAttribute("rel") == "self"){ //Find the self node which contains the link to the data version of the profile
            $ratingslink = $entrylinknode->getAttribute("href"); //Get the value
        }
    }

    //Grab the Address
    $contentnode = $entrynode->getElementsByTagName("content")->item(0); //The address is stored in the content node
    $addressnode = $contentnode->getElementsByTagName("address")->item(0); //The address lines and postcode are stored in this node
    $addressLineNodes = $addressnode->getElementsByTagName("addressLine"); // There are multiple address lines so need to go through them
    $address = ""; // Place holder for final address
    foreach($addressLineNodes as $addressLine){ // Go through the address
        $address = $address.$addressLine->nodeValue.", "; // Change this to change how it displays I like this style
    }
    $postcodenode = $addressnode->getElementsByTagName("postcode"); // The postcode is in a different node 
    $address = $address.$postcodenode->item(0)->nodeValue; // grab it's value

    //Grab the contact details
    $contactnode = $contentnode->getElementsByTagName("contact")->item(0);
    $telephone = $contactnode->getElementsByTagName("telephone")->item(0)->nodeValue;
    
    //Now for the fun bit, grabbing the data that tells us the score for the GP surgery
    $ratingsDomDoc = new DOMDocument();
    $ratingslink = str_replace("?apikey=",".xml?apikey=",$ratingslink);
    $ratingsDomDoc->load($ratingslink);
    
    //Grab the overall ratings
    $overallratingnode = $ratingsDomDoc->getElementsByTagName("OverallRating")->item(0);
    $percentwouldrecommend = "No data available";
    $ratings = "No data available";
    $recommendations = "No data available";
    if($overallratingnode->hasChildNodes()){
        $percentwouldrecommend = $overallratingnode->getElementsByTagName("PercentWouldRecommend")->item(0)->nodeValue;
        $ratings = $overallratingnode->getElementsByTagName("Ratings")->item(0)->nodeValue;
        $recommendations = $overallratingnode->getElementsByTagName("Recommendations")->item(0)->nodeValue;
    }

    //Grab the in-depth ratings - currently issues with this due to crap data from API
   
    /*$ratingsarray = "";
    $ratingsnode = $ratingsDomDoc->getElementsByTagName("Ratings")->item(0);
    if(!($ratingsnode->getAttribute("i:nil") == "true")){
        $ratingnodes = $ratingsnode->getElementsByTagName("rating");
        foreach($ratingnodes as $ratingnode){
            $ratingTitle = $ratingnode->getElementsByTagName("questionText")->item(0)->nodeValue;
            $ratingText = $ratingnode->getElementsByTagName("answerText")->item(0)->nodeValue;
            $ratingValue = $ratingnode->getElementsByTagName("answerMetric")->item(0)->getAttribute("value");
            $ratingMax = $ratingnode->getElementsByTagName("answerMetric")->item(0)->getAttribute("maxValue");
            $numberOfRatings = $ratingnode->getElementsByTagName("answerMetric")->item(0)->getAttribute("numberOfRatings");
            $ratingsarray = $ratingsarray."[".$ratingTitle.", ".$ratingText.", ".$ratingValue.", ".$ratingMax.", ".$numberOfRatings."]";
        }
    }else{
         $ratingsarray = $ratingsarray."[No data available]";
    }
    
     echo($ratingsarray);*/

    //Save to the scraper wiki datastore thing
    $result = array("title" => $title, "link" => $nhschoiceslink, "address" => $address, "telephone" => $telephone, "percentwouldrecommend" => $percentwouldrecommend, "ratings" => $ratings, "recommendations" => $recommendations, "postcode" => $postcodenode->item(0)->nodeValue); //Setting up a basic array
    scraperwiki::save_sqlite(array("title"),$result);
}
if($pages > 1){
    for($j = 2; $j<($pages + 1); $j++){
        $pagesDomDoc = new DOMDocument();
        $pagesURL = "http://v1.syndication.nhschoices.nhs.uk/organisations/".$orgType."/postcode/".$postcode.".xml?apikey=".$apikey."&range=".$radius."&page=".$j;
        echo("page".$j);
        $pagesDomDoc->load($pagesURL);
        $entrynodes = $pagesDomDoc->getElementsByTagName("entry");
        foreach($entrynodes as $entrynode){
            $titles = $entrynode->getElementsByTagName("title");
            $title = $titles->item(0)->nodeValue; // The title is stored in the title node [crazy eh?]
            
            $entrylinknodes = $entrynode->getElementsByTagName("link"); 
            $nhschoiceslink = ""; 
            $ratingslink = ""; 
            foreach($entrylinknodes as $entrylinknode){ //Go through the link nodes
                if($entrylinknode->getAttribute("rel") == "alternate"){ //Find the alternate node which containts the nhs choices link
                    $nhschoiceslink = $entrylinknode->getAttribute("href"); //Get the value
                }
                if($entrylinknode->getAttribute("rel") == "self"){ //Find the self node which contains the link to the data version of the profile
                    $ratingslink = $entrylinknode->getAttribute("href"); //Get the value
                }
            }
            $contentnode = $entrynode->getElementsByTagName("content")->item(0); //The address is stored in the content node
            $addressnode = $contentnode->getElementsByTagName("address")->item(0); //The address lines and postcode are stored in this node
            $addressLineNodes = $addressnode->getElementsByTagName("addressLine"); // There are multiple address lines so need to go through them
            $address = ""; // Place holder for final address
            foreach($addressLineNodes as $addressLine){ // Go through the address
                $address = $address.$addressLine->nodeValue.", "; // Change this to change how it displays I like this style
            }
            $postcodenode = $addressnode->getElementsByTagName("postcode"); // The postcode is in a different node 
            $address = $address.$postcodenode->item(0)->nodeValue; // grab it's value

            //Grab the contact details
            $contactnode = $contentnode->getElementsByTagName("contact")->item(0);
            $telephone = $contactnode->getElementsByTagName("telephone")->item(0)->nodeValue;
    
            $ratingsDomDoc = new DOMDocument();
            $ratingslink = str_replace("?apikey=",".xml?apikey=",$ratingslink);
            $ratingsDomDoc->load($ratingslink);
    
            //Grab the overall ratings
            $overallratingnode = $ratingsDomDoc->getElementsByTagName("OverallRating")->item(0);
            $percentwouldrecommend = "No data available";
            $ratings = "No data available";
            $recommendations = "No data available";
            if($overallratingnode->hasChildNodes()){
                $percentwouldrecommend = $overallratingnode->getElementsByTagName("PercentWouldRecommend")->item(0)->nodeValue;
                $ratings = $overallratingnode->getElementsByTagName("Ratings")->item(0)->nodeValue;
                $recommendations = $overallratingnode->getElementsByTagName("Recommendations")->item(0)->nodeValue;
            }

            $resulta = array("title" => $title, "link" => $nhschoiceslink, "address" => $address, "telephone" => $telephone, "percentwouldrecommend" => $percentwouldrecommend, "ratings" => $ratings, "recommendations" => $recommendations, "postcode" => $postcodenode->item(0)->nodeValue); //Setting up a basic array
            scraperwiki::save_sqlite(array("postcode"),$resulta);


        }
    }
}
?>

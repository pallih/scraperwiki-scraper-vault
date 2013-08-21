<?php

// ALEX MULCHINOCK
// CIRRUS IT SOLUTIONS LIMITED

require_once 'scraperwiki/simple_html_dom.php'; // PULLS SCRAPEWIKI STUFF

$scrape_save = scraperwiki::get_var('last_scrape');

if (!isset($scrape_save)) {
$numrows = 0;
}
else ($numrows = $scrape_save);

if ($numrows < 1) {
$i = 1;
}
else {$i = $numrows+1;};

while ( $i <=99999999 )
{
//////////////////////////////////// EDIT BELOW HERE:
$xml_content = scraperwiki::scrape("http://data.companieshouse.gov.uk/doc/company/".$i.".xml"); // THE PAGE WE'RE SCRAPING
//////////////////////////////////// EDIT ABOVE HERE:

$xml = str_get_html($xml_content); // CREATING A HANDY VARIABLE TO USE LATER.

foreach ($xml->find("CompanyName") as $companyname) { //DEFINING THE COMPANY NAME.           
    $name_data = $companyname->innertext; //GET THE TEXT FROM THE COMPANY NAME.
};

  // echo "Getting company name" . "\n"; // ECHO OUT FIELD 1 (COMPANY NAME)

foreach ($xml->find("CompanyNumber") as $companynumber) { //DEFINING THE COMPANY NUMBER.
    $number_data = $companynumber->innertext; //GET THE TEXT FROM THE COMPANY NUMBER.
};

  //  echo "Grabbing company number" . "\n"; //ECHO OUT FIELD 2 (COMPANY NUMBER)

foreach ($xml->find("RegAddress Careof") as $regaddress0) { //DEFINING THE REGISTERED ADDRESS - CAREOF.
$regaddress_data[0] = $regaddress0->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

//   echo "Getting" . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress POBox") as $regaddress1) { //DEFINING THE REGISTERED ADDRESS - PO BOX.
$regaddress_data[1] = $regaddress1->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

 //   echo "registered" . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress AddressLine1") as $regaddress2) { //DEFINING THE REGISTERED ADDRESS - ADDRESS LINE 1.
$regaddress_data[2] = $regaddress2->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

  //  echo "address" . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress AddressLine2") as $regaddress3) { //DEFINING THE REGISTERED ADDRESS - ADDRESS LINE 2.
$regaddress_data[3] = $regaddress3->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

  //  echo "details" . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress PostTown") as $regaddress4) { //DEFINING THE REGISTERED ADDRESS - TOWN.
$regaddress_data[4] = $regaddress4->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

  //  echo "..." . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress County") as $regaddress5) { //DEFINING THE REGISTERED ADDRESS - COUNTY.
$regaddress_data[5] = $regaddress5->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

  //  echo "..." . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress Country") as $regaddress6) { //DEFINING THE REGISTERED ADDRESS - COUNTRY.
$regaddress_data[6] = $regaddress6->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

//    echo "..." . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("RegAddress PostCode") as $regaddress7) { //DEFINING THE REGISTERED ADDRESS - POST CODE.
$regaddress_data[7] = $regaddress7->innertext; //GET THE TEXT FROM THE REGISTERED ADDRESS.
};

   // echo "FINALLY! Right, next...." . "\n"; //ECHO OUT FIELD 3 (REG ADDRESS)

foreach ($xml->find("CompanyCategory") as $CompanyCategory) { //DEFINING THE COMPANY CATEGORY.
$CompanyCategory_data = $CompanyCategory->innertext; //GET THE TEXT FROM THE COMPANY CATEGORY.
};

  // echo "Hold on, getting information about legal entity..." . "\n"; //ECHO OUT FIELD 4 (COMPANY CATEGORY)

foreach ($xml->find("CompanyStatus") as $CompanyStatus) { //DEFINING THE COMPANY STATUS.
$CompanyStatus_data = $CompanyStatus->innertext; //GET THE TEXT FROM THE COMPANY STATUS.
};

   // echo "Finding out if the company is still trading (or not)."."\n"; //ECHO OUT FIELD 5 (COMPANY STATUS)

foreach ($xml->find("CountryofOrigin") as $CountryofOrigin) { //DEFINING THE COUNTRY OF ORIGIN.
$CountryofOrigin_data = $CountryofOrigin->innertext; //GET THE TEXT FROM THE COUNTRY OF ORIGIN.
};

 //   echo "This company is from: ".$CountryofOrigin_data."\n"; // ECHO OUT FIELD 6 (COUNTRY OF ORIGIN)

foreach ($xml->find("IncorporationDate") as $IncorporationDate) { //DEFINING THE INCORPORATION DATE.
$IncorporationDate_data = $IncorporationDate->innertext; //GET THE TEXT FROM THE INCORPORATION DATE.
};

  //  echo "Incorporation date information found"."\n"; //ECHO OUT FIELD 7 (INCORPORATION DATE)

foreach ($xml->find ("RegistrationDate") as $RegistrationDate) { //DEFINING THE REGISTRATION DATE.
$RegistrationDate_data = $RegistrationDate->innertext; //GET THE TEXT FROM THE REGISTRATION DATE.
};

   // echo "Registration date information found"."\n"; //ECHO OUT FIELD 8 (REGISTRATION DATE)

foreach ($xml->find ("SICCodes") as $SICCodes) { //DEFINING THE SIC CODES.
$SICCodes_data = $SICCodes->innertext; //GET THE TEXT FROM THE SIC CODES.

$SICText = str_replace('<sictext>', '', $SICCodes_data);
$SICText_data = str_replace('</sictext>', "\n", $SICText);

};

   // echo $SICText_data;


//TELLING THE SCRAPER WHAT TO DO IF IT CAN'T FIND THE INFORMATION IT NEEDS
if (!isset($name_data)) {
    $name_data = 'N/A'; //COMPANY NAME
};
if (!isset($number_data)) {
    $number_data = $i; //COMPANY NUMBER
};
if (!isset($regaddress_data[0])) {
    $regaddress_data[0] = ''; //ADDRESS CAREOF
};
if (!isset($regaddress_data[1])) {
    $regaddress_data[1] = ''; //ADDRESS PO BOX
};
if (!isset($regaddress_data[2])) {
    $regaddress_data[2] = ''; //ADDRESS LINE 1
};
if (!isset($regaddress_data[3])) {
    $regaddress_data[3] = ''; //ADDRESS LINE 2
};
if (!isset($regaddress_data[4])) {
    $regaddress_data[4] = ''; //ADDRESS TOWN
};
if (!isset($regaddress_data[5])) {
    $regaddress_data[5] = ''; //ADDRESS COUNTY
};
if (!isset($regaddress_data[6])) {
    $regaddress_data[6] = ''; //ADDRESS COUNTRY
};
if (!isset($regaddress_data[7])) {
    $regaddress_data[7] = ''; //ADDRESS POST CODE
};
if (!isset($companycategory_data)) {
    $CompanyCategory_data = 'N/A'; //COMPANY CATEGORY
};
if (!isset($CompanyStatus_data)) {
    $CompanyStatus_data = 'N/A'; //COMPANY STATUS
};
if (!isset($CountryofOrigin_data)) {
    $CountryofOrigin_data = 'N/A'; //COUNTRY OF ORIGIN
};
if (!isset($IncorporationDate_data)) {
    $IncorporationDate_data = 'N/A'; //INCORPORATION DATE
};
if (!isset($RegistrationDate_data)) {
    $RegistrationDate_data = 'N/A'; //REGISTRATION DATE
};
if (!isset($$SICText_data)) {
    $SICText_data = 'N/A'; //SIC CODES
};

//SAVING THE DATA TO A ROW IN THE DATABASE
    $record = array (
        'company_number' => $i,
        'company_name' => $name_data,
        'company_regaddress' => $regaddress_data[0]."\n".
                                $regaddress_data[1]."\n".
                                $regaddress_data[2]."\n".
                                $regaddress_data[3]."\n".
                                $regaddress_data[4]."\n".
                                $regaddress_data[5]."\n".
                                $regaddress_data[6]."\n".
                                $regaddress_data[7],
        'company_category' => $CompanyCategory_data,
        'company_status' => $CompanyStatus_data,
        'country_of_origin' => $CountryofOrigin_data,
        'incorporation_date' => $IncorporationDate_data,
        'registration_date' => $RegistrationDate_data,
        'sic_codes' => $SICText_data,
    );

scraperwiki::save(array('company_number','company_name','company_regaddress','company_category','company_status','country_of_origin','incorporation_date','registration_date','sic_codes'), $record); //STORE DATA IN DATABASE
scraperwiki::save_var('last_scrape', $i);
echo "Finished! All company information for ".$name_data." has been saved."."\n"."Moving onto next company....";

$i++;
}


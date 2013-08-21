<?php

require 'scraperwiki/simple_html_dom.php';

$urls = array(
    'https://insure.aussie.com.au/life-insurance-request-call-thank-you.aspx',
'https://insure.aussie.com.au/life-insurance-request-info-pack-thank-you.aspx',
'https://insure.aussie.com.au/life-insurance-request-quote-thank-you.aspx',
'https://insure.aussie.com.au/life-insurance-cover.aspx',
'http://pet.choosi.com.au/compare-insurance',
'http://health.choosi.com.au/compare-health-insurance.aspx',
'http://www.choosi.com.au/life-insurance/',
'http://www.choosi.com.au/health-insurance/',
'http://www.choosi.com.au/pet-insurance/',
'http://www.choosi.com.au/income-protection-insurance/',
'http://www.choosi.com.au/funeral-insurance/',
'https://www.choosi.com.au/pet-insurance/receive-quote/',
'https://www.choosi.com.au/life-insurance/receive-quote/',
'https://www.choosi.com.au/funeral-insurance/receive-quote/',
'https://www.choosi.com.au/income-protection-insurance/receive-quote/',
'https://www.choosi.com.au/health-insurance/receive-quote/',
'https://pet.choosi.com.au/choosi-application',
' https://health.choosi.com.au/account/choosi-application.aspx',
'https://pet.choosi.com.au/congratulations',
'https://health.choosi.com.au/congratulations.aspx',
'http://www.choosi.com.au/compare/health/about-you.aspx',
'https://www.choosi.com.au/compare/health/account/choosi-application.aspx',
'http://www.choosi.com.au/life-insurance/compare-quotes-0811',
'http://www.choosi.com.au/funeral-insurance/compare-quotes-0811',
'http://www.choosi.com.au/income-protection-insurance/compare-quotes-0811',
'http://www.choosi.com.au/health-insurance/',
'http://www.choosi.com.au/life-insurance/compare-choose-apply-life-0112/',
'http://www.choosi.com.au/funeral-insurance/compare-funeral-quotes-0112/',
'http://www.choosi.com.au/income-protection-insurance/compare-insurance-quotes-0112/',
'http://www.choosi.com.au/pet-insurance/',
'http://www.choosi.com.au/life-insurance/compare-quotes/',
'http://www.choosi.com.au/funeral-insurance/compare-quotes/',
'http://www.choosi.com.au/income-protection-insurance/compare-quotes/ ',
'https://www.choosi.com.au/insurance-quote/?Insurance=Life',
'https://www.choosi.com.au/insurance-quote/?Insurance=funeral',
'http://health.choosi.com.au/about-you.aspx',
'https://www.choosi.com.au/insurance-quote/?Insurance=income',
'http://pet.choosi.com.au/about-your-pet',
'http://lifecover.guardianinsurance.com.au/infopack/life-insurance-call-me-now-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/income-protection-call-me-now-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/funeral-insurance-call-me-now-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/accident-insurance-call-me-now-thank-you.aspx',
'http://www.guardianinsurance.com.au/Pet-insurance-call-me-now-thank-you.aspx',
'https://service.securequote.com.au/pet/guardian/getaquote.aspx',
'http://lifecover.guardianinsurance.com.au/games/a/life-quote-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/games/a/funeral-quote-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/games/a/income-quote-thank-you.aspx',
'http://lifecover.guardianinsurance.com.au/games/a/accident-quote-thank-you.aspx',
'https://service.securequote.com.au/pet/guardian/QuoteSummary.aspx?',
'http://lifecover.guardianinsurance.com.au/infopack/life-insurance-thank-you-infopack.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/funeral-insurance-thank-you-infopack.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/income-protection-thank-you-infopack.aspx',
'http://lifecover.guardianinsurance.com.au/infopack/accident-insurance-thank-you-infopack.aspx',
'http://www.guardianinsurance.com.au/Pet-InfoPack-Thankyou.aspx',
'https://secureapp.guardianinsurance.com.au/STPApplication/AccidentApplication/Payment.aspx',
'https://secureapp.guardianinsurance.com.au/STPApplication/FuneralApplication/Payment.aspx',
'https://securequote.uat.hollardfs.com.au/pet/guardian/ConfirmationThankYou.aspx',
'https://secureapp.guardianinsurance.com.au/STPApplication/AccidentApplication/Quote.aspx',
'https://secureapp.guardianinsurance.com.au/STPApplication/FuneralApplication/Quote.aspx',
'https://service.securequote.com.au/pet/guardian/PetDetails.aspx?',
'http://www.lifecover.guardianinsurance.com.au/infopack/life-insurance.aspx?Product=Life',
'http://www.lifecover.guardianinsurance.com.au/infopack/income-protection.aspx?Product=IncomeProtection',
'http://www.lifecover.guardianinsurance.com.au/infopack/funeral-insurance.aspx?Product=Funeral',
'http://www.lifecover.guardianinsurance.com.au/infopack/accident-insurance.aspx?Product=Accidental',
'http://www.lifecover.guardianinsurance.com.au/games/a/life-insurance.aspx',
'http://www.lifecover.guardianinsurance.com.au/games/a/income-protection.aspx?Product=IncomeProtection',
'http://www.lifecover.guardianinsurance.com.au/games/a/funeral-insurance.aspx?Product=Funeral',
'http://www.guardianinsurance.com.au/',
'http://www.guardianinsurance.com.au/Life-Insurance.aspx',
'http://www.guardianinsurance.com.au/Income-Protection-Insurance.aspx',
'http://www.guardianinsurance.com.au/Funeral-Insurance.aspx',
'http://www.guardianinsurance.com.au/Accident-Insurance.aspx',
'http://www.guardianinsurance.com.au/Pet-Insurance.aspx',
'https://service.securequote.com.au/pet/guardian/getaquote.aspx',
'http://www.guardianinsurance.com.au/Life-Insurance-Quote.aspx',
'http://www.guardianinsurance.com.au/Income-Protection-Insurance-Quote.aspx',
'http://www.guardianinsurance.com.au/Funeral-Insurance-Quote.aspx',
'http://www.guardianinsurance.com.au/Accident-Insurance-Quote.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/life-insurance-quote.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/income-protection-quote.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/funeral-insurance-quote.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/accident-insurance-quote.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/accident-insurance-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/income-protection-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/funeral-insurance-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/infopack/accident-insurance-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/games/a/life-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/games/a/income-call-me-now.aspx',
'http://www.lifecover.guardianinsurance.com.au/games/a/funeral-call-me-now.aspx',
'http://www.guardianinsurance.com.au/life-insurance-call-me-now.aspx',
'http://www.guardianinsurance.com.au/income-protection-insurance-call-me-now.aspx',
'http://www.guardianinsurance.com.au/funeral-insurance-call-me-now.aspx',
'http://www.guardianinsurance.com.au/accident-insurance-call-me-now.aspx',
'http://www.guardianinsurance.com.au/pet-insurance-call-me-now.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/call-back-thank-you.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/call-back-thank-you.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-cover/call-back-thank-you.aspx',
'https://service.securequote.com.au/pet/real/GetAQuote.aspx?',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/call-back-thank-you.aspx',
'http://www.realinsurance.com.au/Car-Insurance/Call-Me-Back/Thank-You',
'http://www.realinsurance.com.au/Home-Insurance/Call-Me-Back/Thank-You',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/Quote-Result.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/QuoteResult.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-cover/Quote-Result.aspx',
'https://service.securequote.com.au/pet/real/QuoteSummary.aspx?',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/Quote-Result.aspx',
'https://quote.realinsurance.com.au/quotelines/Car/YourQuote/',
'https://quote.realinsurance.com.au/quotelines/Home/YourQuote/',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/info-pack-thank-you.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/info-pack-thank-you.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-cover/info-pack-thank-you.aspx',
'http://www.pet.realinsurance.com.au/Pet_InfoPack_Thankyou.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/info-pack-thank-you.aspx',
'http://quote.realinsurance.com.au/quotelines/car/yourquote',
'http://quote.realinsurance.com.au/quotelines/home/yourquote',
'https://quote.realinsurance.com.au/quotelines/Car/Thanks/',
'http://quote.realinsurance.com.au/quotelines/home/thanks',
'https://service.securequote.com.au/pet/real/PaymentDetailsCombined.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-cover/',
'http://www.pet.realinsurance.com.au/Pet.aspx',
'http://www.realinsurance.com.au/Car-Insurance ',
'http://www.realinsurance.com.au/Home-Insurance/Contents-Insurance ',
'https://service.securequote.com.au/pet/real/getaquote.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/call-me-back.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/funeral-expenses-cover/instant-quote-form.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/call-me-back.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/bill-cover/instant-quote-form.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/call-me-back.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/family-life-cover/instant-quote-form.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-call-me-back.aspx',
'http://www.lifecover.realinsurance.com.au/siteb-request-quote/income-protection-cover/instant-quote-form.aspx',
'http://www.rspcapetinsurance.org.au/call-thankyou.aspx?',
'https://service.securequote.com.au/pet/rspca/getaquote.aspx',
'http://www.rspcapetinsurance.org.au/info-thankyou.aspx',
'https://service.securequote.com.au/pet/rspca/QuoteSummary.aspx?PetQuoteID=335487',
'https://service.securequote.com.au/pet/rspca/ConfirmationThankYou.aspx',
'https://service.securequote.com.au/pet/rspca/PetDetails.aspx?',
'https://service.securequote.com.au/pet/rspca/VerifyDetails.aspx'
);

$search_terms = array(
    array('s.clicktale.net'.'ClickTale'),
    array('tracker.marinsm.com','Marin'),
    array('tealium.hs.llnwd.net','Tealium'),
    array('google-analytics.com','Google Analytics'),
    array('www.googleadservices.com','DoubleClick'),
    array('visualwebsiteoptimizer.com','Visual Web Optimizer')
);

foreach($urls as $url) {
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("script") as $script){
        // Find each script tag
        foreach($search_terms as $search_term) {
            // Loop through search terms
            if( $script->src != false ) {
                // Check if there is a src attribute
                if( stristr( $script->src, $search_term[0] ) != false ) {
                    // If the src contains a match, save the URL and our friendly name
                    $record = array(
                        'url' => $url, 
                        'src' => $search_term[1]
                    );
                    // Save the record to our dataset
                    scraperwiki::save(array('url','src'), $record);
                }
            } else if( strlen($script->innertext) > 0 ) {
                // Verify the element is not empty
                if( stristr( $script->innertext, $search_term[0] ) != false ) {
                    // If the text contains a match, save the URL and our friendly name
                    $record = array(
                        'url' => $url, 
                        'src' => $search_term[1]
                    );
                    // Save the record to our dataset
                    scraperwiki::save(array('url','src'), $record);
                }
            }
        }
    }
    print "Done with $url";
}
?>

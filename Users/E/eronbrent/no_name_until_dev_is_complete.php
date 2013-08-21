<?php

//Get Federal Reserve Rates & Put in a database. 
//RSS link pulled from http://www.federalreserve.gov/feeds/h15_data.htm

require 'scraperwiki/simple_html_dom.php';

//Globals
$unique_keys = array( "rate_name", "rate_value", "rate_date", "rate_reference_link", "latest", "timestamp", "category", "short_name" );           

//Grab RSS
$rss_content = scraperwiki::scrape("http://www.federalreserve.gov/feeds/Data/H15_H15.XML");
$xml = str_get_html($rss_content);

$var_count = 0; $updates = 0;

//scraperwiki::sqliteexecute("delete from swdata;");
//scraperwiki::sqlitecommit();

//Loop through rates
foreach ($xml->find("item") as $el) {  
    
    $rate_reference_link = $el->find("link", 0)->innertext;
    $rate_name = urlencode($el->find("description", 0)->innertext );
    $item_details = $el->find("cb:otherStatistic", 0);
    $rate_value = $item_details->find("cb:value", 0)->innertext;
    $rate_date = $item_details->find("cb:observationPeriod", 0)->innertext;

    $result = scraperwiki::select("* from swdata where rate_name='".$rate_name."' and rate_date='".$rate_date."';");

    if( !isset($result[0]) )
    {

        $info = lookup_category_and_short_name( $rate_name );

        scraperwiki::sqliteexecute("update swdata set latest='0' where rate_name='".$rate_name."';");
        scraperwiki::sqlitecommit();
    
        $data = array("rate_name" => $rate_name,"rate_value" => $rate_value,  "rate_date" => $rate_date, "rate_reference_link"=>$rate_reference_link, "latest" => "1", "timestamp" => time(), "category" => $info['category'], "short_name" => $info['short_name'] );
        scraperwiki::save_sqlite($unique_keys, $data, $table_name="swdata", $verbose=2 );
        
        $updates++;
    }

    $var_count++;
}

print "var_count=".$var_count." updates=".$updates."\n";

$xml->__destruct();

function lookup_category_and_short_name( $rate_name )
{

    $result['category'] = ""; $result['short_name'] = "";

    if( $rate_name == "Federal+funds+effective+rate" ) { $result['category'] = "Federal Funds Effective Rate"; $result['short_name'] = "Federal Funds Effective Rate"; }
    else if( $rate_name == "30-Day+AA+Nonfinancial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "Nonfinancial Commercial Paper"; $result['short_name'] = "30 Day";  } 
    else if( $rate_name == "60-Day+AA+Nonfinancial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "Nonfinancial Commercial Paper"; $result['short_name'] = "60 Day";  }
    else if( $rate_name == "90-Day+AA+Nonfinancial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "ANonfinancial Commercial Paper"; $result['short_name'] = "90 Day";  }
    else if( $rate_name == "30-Day+AA+Financial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "30 Day";  }
    else if( $rate_name == "60-Day+AA+Financial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "60 Day";  }
    else if( $rate_name == "90-Day+AA+Financial+Commercial+Paper+Interest+Rate" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "90 Day";  } 
    else if( $rate_name == "Average+rate+on+1-month+neogtiable+++certificates+of+deposit+%28secondary+market%29%2C+++quoted+on+an+investment+basis" ) { $result['category'] = "Certificates of Deposit (CD)"; $result['short_name'] = "1 month";  }
    else if( $rate_name == "Average+rate+on+3-month+neogtiable+++certificates+of+deposit+%28secondary+market%29%2C+++quoted+on+an+investment+basis" ) { $result['category'] = "Certificates of Deposit (CD)"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "Average+rate+on+6-month+neogtiable+++certificates+of+deposit+%28secondary+market%29%2C+++quoted+on+an+investment+basis" ) { $result['category'] = "Certificates of Deposit (CD)"; $result['short_name'] = "6 month";  }
    else if( $rate_name == "U.S.+--+SHORT-TERM+INTEREST+RATES%3A+DAILY+1-MONTH+EURO-DOLLAR+DEPOSIT+RATE+" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "1 month eurodollar deposit rate";  }
    else if( $rate_name == "U.S.+--+SHORT-TERM+INTEREST+RATES%3A+DAILY+3-MONTH+EURO-DOLLAR+DEPOSIT+RATE+" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "3 month eurodollar deposit rate";  } 
    else if( $rate_name == "U.S.+--+SHORT-TERM+INTEREST+RATES%3A+DAILY+6-MONTH+EURO-DOLLAR+DEPOSIT+RATE+" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "6 month eurodollar deposit rate";  }
    else if( $rate_name == "Average+majority+prime+rate+charged+by+banks+++on+short-term+loans+to+business%2C+++quoted+on+an+investment+basis" ) { $result['category'] = "Prime Rate"; $result['short_name'] = "average prime rate";  }
    else if( $rate_name == "The+rate+charged+for+primary+credit+under+++amendment+to+the+Board%27s+Regulation+A" ) { $result['category'] = ""; $result['short_name'] = "";  }
    else if( $rate_name == "4-week+Treasury+bill+secondary+market+rate+++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "4 week";  }
    else if( $rate_name == "3-week+Treasury+bill+secondary+market+rate+++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "3 week";  } 
    else if( $rate_name == "6-week+Treasury+bill+secondary+market+rate+++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "6 week";  }
    else if( $rate_name == "1-year+Treasury+bill+secondary+market+rate%5E++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "1 year";  }
    else if( $rate_name == "3-month+Treasury+bill+secondary+market+rate+++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "6-month+Treasury+bill+secondary+market+rate+++discount+basis" ) { $result['category'] = "Treasury Bill (T-Bill)"; $result['short_name'] = "6 month";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+1-month+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+3-month+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+6-month+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  } 
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+1-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+2-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+3-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+5-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+7-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  } 
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+10-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+20-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+30-year+++constant+maturity%2C+quoted+on+investment+basis" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+5-year+++constant+maturity%2C+quoted+on+investment+basis%2C+++inflation-indexed" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+7-year+++constant+maturity%2C+quoted+on+investment+basis%2C+++inflation-indexed" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+10-year+++constant+maturity%2C+quoted+on+investment+basis%2C+++inflation-indexed" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+20-year+++constant+maturity%2C+quoted+on+investment+basis%2C+++inflation-indexed" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "";  } 
    else if( $rate_name == "Market+yield+on+U.S.+Treasury+securities+at+30-year+++constant+maturity%2C+quoted+on+investment+basis%2C+++inflation-indexed" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "";  }
    else if( $rate_name == "Treasury+long-term+average+%28over+10+years%29" ) { $result['category'] = ""; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+one+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+two+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+three+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  } 
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+four+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+five+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+seven+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+ten+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "Rate+paid+by+fixed-rate+payer+on+an+interest+rate+swap+with++++maturity+of+thirty+year." ) { $result['category'] = "Swap Rate"; $result['short_name'] = "";  }
    else if( $rate_name == "MOODY%27S+YIELD+ON+SEASONED+CORPORATE+BONDS+-+ALL+INDUSTRIES%2C+AAA" ) { $result['category'] = "Moodys"; $result['short_name'] = "Yield on Seasoned Corp Bonds AAA";  }
    else if( $rate_name == "MOODY%27S+YIELD+ON+SEASONED+CORPORATE+BONDS+-+ALL+INDUSTRIES%2C+BAA" ) { $result['category'] = "Moodys"; $result['short_name'] = "Yield on Seasoned Corp Bonds BAA";  }
    else if( $rate_name == "Federal+funds" ) { $result['category'] = "Federal Funds"; $result['short_name'] = "Federal Funds";  } 
    else if( $rate_name == "1-month+nonfinancial+commercial+paper" ) { $result['category'] = "Nonfinancial Commercial Paper"; $result['short_name'] = "1 month";  }
    else if( $rate_name == "2-month+nonfinancial+commercial+paper" ) { $result['category'] = "Nonfinancial Commercial Paper"; $result['short_name'] = "2 month";  }
    else if( $rate_name == "3-month+nonfinancial+commercial+paper" ) { $result['category'] = "Nonfinancial Commercial Paper"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "1-month+financial+commercial+paper" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "1 month";  }
    else if( $rate_name == "2-month+financial+commercial+paper" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "2 month";  }
    else if( $rate_name == "3-month+financial+commercial+paper" ) { $result['category'] = "Financial Commercial Paper"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "1-month+CD" ) { $result['category'] = "CD"; $result['short_name'] = "1 month";  } 
    else if( $rate_name == "3-month+CD" ) { $result['category'] = "CD"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "6-month+CD" ) { $result['category'] = "CD"; $result['short_name'] = "6 month";  }
    else if( $rate_name == "1-month+eurodollar+deposit+rate" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "1 month";  }
    else if( $rate_name == "3-month+eurodollar+deposit+rate" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "6-month+eurodollar+deposit+rate" ) { $result['category'] = "Eurodollar Deposit Rate"; $result['short_name'] = "6 month";  }
    else if( $rate_name == "Prime+rate" ) { $result['category'] = "Prime Rate"; $result['short_name'] = "Prime Rate";  }
    else if( $rate_name == "Discount+rate" ) { $result['category'] = "Discount Rate"; $result['short_name'] = "Discount Rate";  }
    else if( $rate_name == "4-week+Treasury+bill" ) { $result['category'] = "Treasury Bill"; $result['short_name'] = "4 week";  } 
    else if( $rate_name == "3-week+Treasury+bill" ) { $result['category'] = "Treasury Bill"; $result['short_name'] = "3 week";  }
    else if( $rate_name == "6-week+Treasury+bill" ) { $result['category'] = "Treasury Bill"; $result['short_name'] = "6 week";  }
    else if( $rate_name == "1-year+Treasury+bill" ) { $result['category'] = "Treasury Bill"; $result['short_name'] = "1 year";  }
    else if( $rate_name == "1-month+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "1 month";  }
    else if( $rate_name == "3-month+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "3 month";  }
    else if( $rate_name == "6-month+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "6 month";  }
    else if( $rate_name == "1-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "1 year";  } 
    else if( $rate_name == "2-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "2 year";  }
    else if( $rate_name == "3-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "3 year";  }
    else if( $rate_name == "5-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "5 year";  }
    else if( $rate_name == "7-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "7 year";  }
    else if( $rate_name == "10-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "10 year";  }
    else if( $rate_name == "20-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "20 year";  }
    else if( $rate_name == "30-year+Treasury+constant+maturity" ) { $result['category'] = "Treasury Constant Maturity"; $result['short_name'] = "30 year";  }
    else if( $rate_name == "5-year+inflation+indexed+Treasury+constant+maturity" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "5 year";  } 
    else if( $rate_name == "7-year+inflation+indexed+Treasury+constant+maturity" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "7 year";  }
    else if( $rate_name == "10-year+inflation+indexed+Treasury+constant+maturity" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "10 year";  }
    else if( $rate_name == "20-year+inflation+indexed+Treasury+constant+maturity" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "20 year";  }
    else if( $rate_name == "30-year+inflation+indexed+Treasury+constant+maturity" ) { $result['category'] = "Inflation Indexed Treasury Constant Maturity"; $result['short_name'] = "30 year";  }
    else if( $rate_name == "Inflation+indexed+long-term+average" ) { $result['category'] = "Inflation Indexed Long-term Average"; $result['short_name'] = "Inflation Indexed Long-term Average";  }
    else if( $rate_name == "1-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "1 year";  }
    else if( $rate_name == "2-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "2 year";  } 
    else if( $rate_name == "3-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "3 year";  }
    else if( $rate_name == "4-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "4 year";  }
    else if( $rate_name == "5-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "5 year";  }
    else if( $rate_name == "7-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "7 year";  }
    else if( $rate_name == "10-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "10 year ";  }
    else if( $rate_name == "30-year+swap+rate" ) { $result['category'] = "Swap Rate"; $result['short_name'] = "30 year";  }
    else if( $rate_name == "Moody%27s+Aaa" ) { $result['category'] = "Moodys"; $result['short_name'] = "Moodys Aaa";  } 
    else if( $rate_name == "Moody%27s+Baa" ) { $result['category'] = "Moodys"; $result['short_name'] = "Moody Baa";  }
 
    return $result;
}

?>

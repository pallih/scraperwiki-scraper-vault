#########################################################################
# Description:                                                          #
#                                                                       #
# This uses the StackExchangeAPI (http://api.stackexchange.com/docs)    #
# to scrape data from stackoverflow                                     #
# Something similar is available here:                                  #
#  http://hewgill.com/~greg/stackoverflow/stack_overflow/tags/          #
# Inspired by ideas from:                                               #
#  https://scraperwiki.com/scrapers/so_tag_counter/                     #
#########################################################################

import scraperwiki
import json
import sys
import gzip
import StringIO
from datetime import datetime

# clear console output
stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

#########################################################################
# class definition(s)                                                   #
#########################################################################


#########################################################################
# site/api configuration                                                #
#########################################################################

site = "stackoverflow"
se_api_version = "2.1";
se_api_base = "https://api.stackexchange.com/";
url_base = se_api_base + se_api_version;
url_tag_total_count = url_base + "/tags/{tag}/info?site=" + site;

# Apply filters to url(s) to reduce data sent back
url_tag_total_count += "&filter=!6UYUIjApbXLdx"; #  Only return count

#########################################################################
# scraper configuration (which tags should be scraped)                  #
#########################################################################
tags = ["c", "java", "ruby", "python", "haskell"];
data = {
            "timestamp":datetime.now(), "property":"total count"
}

#########################################################################
# main                                                                  #
#########################################################################
sys.stdout.write("Starting to scrape data from " + site + "\n");

for tag in tags:
    sys.stdout.write("Getting total count for tag: " + tag + "\n");
    url = url_tag_total_count.replace("{tag}", tag);
    gzipResponse = StringIO.StringIO(scraperwiki.scrape(url));
    gzipper = gzip.GzipFile(fileobj=gzipResponse);
    textResponse = gzipper.read();
    responseData = json.loads(textResponse);
    items = responseData["items"];
    count = items[0]["count"];
    sys.stdout.write(" - result: ");
    sys.stdout.write(count);
    sys.stdout.write("\n");
    data[tag]=count;


# columns will extend automatically here
sys.stdout.write("Saving data in sqlite database\n");
scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data)
#########################################################################
# Description:                                                          #
#                                                                       #
# This uses the StackExchangeAPI (http://api.stackexchange.com/docs)    #
# to scrape data from stackoverflow                                     #
# Something similar is available here:                                  #
#  http://hewgill.com/~greg/stackoverflow/stack_overflow/tags/          #
# Inspired by ideas from:                                               #
#  https://scraperwiki.com/scrapers/so_tag_counter/                     #
#########################################################################

import scraperwiki
import json
import sys
import gzip
import StringIO
from datetime import datetime

# clear console output
stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

#########################################################################
# class definition(s)                                                   #
#########################################################################


#########################################################################
# site/api configuration                                                #
#########################################################################

site = "stackoverflow"
se_api_version = "2.1";
se_api_base = "https://api.stackexchange.com/";
url_base = se_api_base + se_api_version;
url_tag_total_count = url_base + "/tags/{tag}/info?site=" + site;

# Apply filters to url(s) to reduce data sent back
url_tag_total_count += "&filter=!6UYUIjApbXLdx"; #  Only return count

#########################################################################
# scraper configuration (which tags should be scraped)                  #
#########################################################################
tags = ["c", "java", "ruby", "python", "haskell"];
data = {
            "timestamp":datetime.now(), "property":"total count"
}

#########################################################################
# main                                                                  #
#########################################################################
sys.stdout.write("Starting to scrape data from " + site + "\n");

for tag in tags:
    sys.stdout.write("Getting total count for tag: " + tag + "\n");
    url = url_tag_total_count.replace("{tag}", tag);
    gzipResponse = StringIO.StringIO(scraperwiki.scrape(url));
    gzipper = gzip.GzipFile(fileobj=gzipResponse);
    textResponse = gzipper.read();
    responseData = json.loads(textResponse);
    items = responseData["items"];
    count = items[0]["count"];
    sys.stdout.write(" - result: ");
    sys.stdout.write(count);
    sys.stdout.write("\n");
    data[tag]=count;


# columns will extend automatically here
sys.stdout.write("Saving data in sqlite database\n");
scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data)

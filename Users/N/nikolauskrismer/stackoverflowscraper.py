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
import urllib
import gzip
import StringIO
import time
from datetime import datetime

# clear console output
stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

#########################################################################
# scraper configuration (which tags should be scraped)                  #
#########################################################################

useTagSynonyms = 0;
useOAuth = 1; # be sure to take care about a valid accessToken when enabling this
tags = ["c", "c#", "c++", "haskell", "java", "php", "python", "ruby"];

#########################################################################
# site/api configuration                                                #
#########################################################################

site = "stackoverflow";
seApiVersion = "2.1";
seApiBase = "https://api.stackexchange.com/";
urlBase = seApiBase + seApiVersion;
urlTagTotalCount = urlBase + "/tags/{tag}/info?site=" + site;
urlTagSynonyms = urlBase + "/tags/{tag}/synonyms?site=" + site;
urlQuestionsMaxScore = urlBase + "/questions?site=" + site + "&tagged={tag}&pagesize=1&order=desc&sort=votes";
urlQuestionsTotal = urlBase + "/questions?site=" + site + "&tagged={tag}";
urlQuestionsUnanswered = urlBase + "/questions/unanswered?site=" + site + "&tagged={tag}";

# Apply fromdate
fromDateToday = str((int) (time.time() / 86400) * 86400);
urlQuestionsMaxScore += "&fromdate=" + fromDateToday;
urlQuestionsTotal += "&fromdate=" + fromDateToday;
urlQuestionsUnanswered += "&fromdate=" + fromDateToday;

# Apply filters to url(s) to reduce data sent back
urlTagTotalCount += "&filter=!)O0_7chyAVK";
urlTagSynonyms += "&filter=!)7qLtJOp0*)";
urlQuestionsMaxScore += "&filter=!C7Uj0172K0";
urlQuestionsTotal += "&filter=total";
urlQuestionsUnanswered += "&filter=total";

# Apply accessToken
if useOAuth != 0:
    #https://stackexchange.com/oauth/dialog?client_id=1573&scope=no_expiry&redirect_uri=https%3a%2f%2fstackexchange.com%2foauth%2flogin_success;
    accessToken="jNKSHepA7NWkeBNCaUusbw))"; # This will NOT expire (since created with scope "no_expiry")
    accessKey="fLxoquAIlYYrr1NsciVaRw((";
    accessParams="&key=" + accessKey + "&access_token="  +accessToken;
    urlTagTotalCount += accessParams;
    urlTagSynonyms += accessParams;
    urlQuestionsMaxScore += accessParams;
    urlQuestionsTotal += accessParams;
    urlQuestionsUnanswered += accessParams;

#########################################################################
# Global variables                                                      #
#########################################################################

synonyms = {}
currentTimestamp = datetime.now();

#########################################################################
# Functions                                                             #
#########################################################################

def createDataObject(propertyName):
    return {
        "property": propertyName,
        "timestamp": currentTimestamp
    };

def getAjaxResponse(url):
    resp = scraperwiki.scrape(url);
    gzipResponse = StringIO.StringIO(resp);
    gzipper = gzip.GzipFile(fileobj=gzipResponse);
    textResponse = gzipper.read();
    return json.loads(textResponse);

def callQuestionApi(tag):
    return getAjaxResponse(urlQuestionsTotal.replace("{tag}", urllib.quote_plus(tag)));

def callQuestionUnansweredApi(tag):
    return getAjaxResponse(urlQuestionsUnanswered.replace("{tag}", urllib.quote_plus(tag)));

def callQuestionMaxScoreApi(tag):
    return getAjaxResponse(urlQuestionsMaxScore.replace("{tag}", urllib.quote_plus(tag)));

def callSynonymApi(tag):
    return getAjaxResponse(urlTagSynonyms.replace("{tag}", urllib.quote_plus(tag)));

def callTagApi(tag):
    return getAjaxResponse(urlTagTotalCount.replace("{tag}", urllib.quote_plus(tag)));

def escapeKey(key):
    # using encoded tag to enable storing in sqlite db (e.g: c#)
    keyString = key.replace('#', 'sharp');
    keyString = keyString.replace('+', 'plus');
    return keyString;

def saveDataObject():
    scraperwiki.sqlite.save(
        unique_keys = ['property', 'timestamp'],
        data = data
    );

#########################################################################
# main                                                                  #
#########################################################################
sys.stdout.write("Starting to scrape data from " + site + "\n");

# Build synonyms
if useTagSynonyms != 0:
    for tag in tags:
        sys.stdout.write("Gettings synonyms for tag: " + tag + "\n");
        responseData = callSynonymApi(tag);
        items = responseData["items"];
        total = responseData["total"];
        if (total <= 0):
            continue;
        synonymList = [];
        for item in items:
            synonymList.append(item["from_tag"]);
        synonyms[tag] = synonymList;

# Get property "total count"
data = createDataObject("totalCount");
for tag in tags:
    sys.stdout.write("Getting total count for tag: " + tag + "\n");
    responseData = callTagApi(tag);
    items = responseData["items"];
    total = responseData["total"];
    count = 0 if total <= 0 else items[0]["count"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding total count for synonym '" + synonym + "': ");
            synResponseData = callTagApi(synonym);
            synItems = synResponseData["items"];
            synTotal = synResponseData["total"];
            synCount = 0 if synTotal <= 0 else synItems[0]["count"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            count += synCount;
    sys.stdout.write(" - result: " + str(count) + "\n");
    data[escapeKey(tag)] = count;

# Get property "question count"
saveDataObject();
data = createDataObject("questionCount");
for tag in tags:
    sys.stdout.write("Getting question count for tag: " + tag + "\n");
    responseData = callQuestionApi(tag);
    total = responseData["total"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding question count for synonym '" + synonym + "': ");
            synResponseData = callQuestionApi(synonym);
            synTotal = synResponseData["total"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            total += synTotal;
    sys.stdout.write(" - result: " + str(total) + "\n");
    data[escapeKey(tag)] = total;

# Get property "question unanswered count"
saveDataObject();
data = createDataObject("questionUnansweredCount");
for tag in tags:
    sys.stdout.write("Getting question unanswered count for tag: " + tag + "\n");
    responseData = callQuestionUnansweredApi(tag);
    total = responseData["total"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding question unanswered count for synonym '" + synonym + "': ");
            synResponseData = callQuestionUnansweredApi(synonym);
            synTotal = synResponseData["total"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            total += synTotal;
    sys.stdout.write(" - result: " + str(total) + "\n");
    data[escapeKey(tag)] = total;

# Get property "question max score"
saveDataObject();
data = createDataObject("questionMaxScore");
for tag in tags:
    sys.stdout.write("Getting question with maximal score for tag: " + tag + "\n");
    responseData = callQuestionMaxScoreApi(tag);
    total = responseData["total"]
    items = responseData["items"]
    score = 0 if total <= 0 else items[0]["score"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - taking care of maximal questions score for synonym '" + synonym + "': ");
            synResponseData = callQuestionMaxScoreApi(synonym);
            synTotal = synResponseData["total"]
            synItems = synResponseData["items"]
            synScore = 0 if synTotal <= 0 else synItems[0]["score"];
            sys.stdout.write(synScore);
            sys.stdout.write("\n");
            if (synScore > score):
                score = synScore;
    sys.stdout.write(" - result: " + str(score) + "\n");
    data[escapeKey(tag)] = score;

saveDataObject();#########################################################################
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
import urllib
import gzip
import StringIO
import time
from datetime import datetime

# clear console output
stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

#########################################################################
# scraper configuration (which tags should be scraped)                  #
#########################################################################

useTagSynonyms = 0;
useOAuth = 1; # be sure to take care about a valid accessToken when enabling this
tags = ["c", "c#", "c++", "haskell", "java", "php", "python", "ruby"];

#########################################################################
# site/api configuration                                                #
#########################################################################

site = "stackoverflow";
seApiVersion = "2.1";
seApiBase = "https://api.stackexchange.com/";
urlBase = seApiBase + seApiVersion;
urlTagTotalCount = urlBase + "/tags/{tag}/info?site=" + site;
urlTagSynonyms = urlBase + "/tags/{tag}/synonyms?site=" + site;
urlQuestionsMaxScore = urlBase + "/questions?site=" + site + "&tagged={tag}&pagesize=1&order=desc&sort=votes";
urlQuestionsTotal = urlBase + "/questions?site=" + site + "&tagged={tag}";
urlQuestionsUnanswered = urlBase + "/questions/unanswered?site=" + site + "&tagged={tag}";

# Apply fromdate
fromDateToday = str((int) (time.time() / 86400) * 86400);
urlQuestionsMaxScore += "&fromdate=" + fromDateToday;
urlQuestionsTotal += "&fromdate=" + fromDateToday;
urlQuestionsUnanswered += "&fromdate=" + fromDateToday;

# Apply filters to url(s) to reduce data sent back
urlTagTotalCount += "&filter=!)O0_7chyAVK";
urlTagSynonyms += "&filter=!)7qLtJOp0*)";
urlQuestionsMaxScore += "&filter=!C7Uj0172K0";
urlQuestionsTotal += "&filter=total";
urlQuestionsUnanswered += "&filter=total";

# Apply accessToken
if useOAuth != 0:
    #https://stackexchange.com/oauth/dialog?client_id=1573&scope=no_expiry&redirect_uri=https%3a%2f%2fstackexchange.com%2foauth%2flogin_success;
    accessToken="jNKSHepA7NWkeBNCaUusbw))"; # This will NOT expire (since created with scope "no_expiry")
    accessKey="fLxoquAIlYYrr1NsciVaRw((";
    accessParams="&key=" + accessKey + "&access_token="  +accessToken;
    urlTagTotalCount += accessParams;
    urlTagSynonyms += accessParams;
    urlQuestionsMaxScore += accessParams;
    urlQuestionsTotal += accessParams;
    urlQuestionsUnanswered += accessParams;

#########################################################################
# Global variables                                                      #
#########################################################################

synonyms = {}
currentTimestamp = datetime.now();

#########################################################################
# Functions                                                             #
#########################################################################

def createDataObject(propertyName):
    return {
        "property": propertyName,
        "timestamp": currentTimestamp
    };

def getAjaxResponse(url):
    resp = scraperwiki.scrape(url);
    gzipResponse = StringIO.StringIO(resp);
    gzipper = gzip.GzipFile(fileobj=gzipResponse);
    textResponse = gzipper.read();
    return json.loads(textResponse);

def callQuestionApi(tag):
    return getAjaxResponse(urlQuestionsTotal.replace("{tag}", urllib.quote_plus(tag)));

def callQuestionUnansweredApi(tag):
    return getAjaxResponse(urlQuestionsUnanswered.replace("{tag}", urllib.quote_plus(tag)));

def callQuestionMaxScoreApi(tag):
    return getAjaxResponse(urlQuestionsMaxScore.replace("{tag}", urllib.quote_plus(tag)));

def callSynonymApi(tag):
    return getAjaxResponse(urlTagSynonyms.replace("{tag}", urllib.quote_plus(tag)));

def callTagApi(tag):
    return getAjaxResponse(urlTagTotalCount.replace("{tag}", urllib.quote_plus(tag)));

def escapeKey(key):
    # using encoded tag to enable storing in sqlite db (e.g: c#)
    keyString = key.replace('#', 'sharp');
    keyString = keyString.replace('+', 'plus');
    return keyString;

def saveDataObject():
    scraperwiki.sqlite.save(
        unique_keys = ['property', 'timestamp'],
        data = data
    );

#########################################################################
# main                                                                  #
#########################################################################
sys.stdout.write("Starting to scrape data from " + site + "\n");

# Build synonyms
if useTagSynonyms != 0:
    for tag in tags:
        sys.stdout.write("Gettings synonyms for tag: " + tag + "\n");
        responseData = callSynonymApi(tag);
        items = responseData["items"];
        total = responseData["total"];
        if (total <= 0):
            continue;
        synonymList = [];
        for item in items:
            synonymList.append(item["from_tag"]);
        synonyms[tag] = synonymList;

# Get property "total count"
data = createDataObject("totalCount");
for tag in tags:
    sys.stdout.write("Getting total count for tag: " + tag + "\n");
    responseData = callTagApi(tag);
    items = responseData["items"];
    total = responseData["total"];
    count = 0 if total <= 0 else items[0]["count"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding total count for synonym '" + synonym + "': ");
            synResponseData = callTagApi(synonym);
            synItems = synResponseData["items"];
            synTotal = synResponseData["total"];
            synCount = 0 if synTotal <= 0 else synItems[0]["count"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            count += synCount;
    sys.stdout.write(" - result: " + str(count) + "\n");
    data[escapeKey(tag)] = count;

# Get property "question count"
saveDataObject();
data = createDataObject("questionCount");
for tag in tags:
    sys.stdout.write("Getting question count for tag: " + tag + "\n");
    responseData = callQuestionApi(tag);
    total = responseData["total"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding question count for synonym '" + synonym + "': ");
            synResponseData = callQuestionApi(synonym);
            synTotal = synResponseData["total"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            total += synTotal;
    sys.stdout.write(" - result: " + str(total) + "\n");
    data[escapeKey(tag)] = total;

# Get property "question unanswered count"
saveDataObject();
data = createDataObject("questionUnansweredCount");
for tag in tags:
    sys.stdout.write("Getting question unanswered count for tag: " + tag + "\n");
    responseData = callQuestionUnansweredApi(tag);
    total = responseData["total"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - adding question unanswered count for synonym '" + synonym + "': ");
            synResponseData = callQuestionUnansweredApi(synonym);
            synTotal = synResponseData["total"];
            sys.stdout.write(synCount);
            sys.stdout.write("\n");
            total += synTotal;
    sys.stdout.write(" - result: " + str(total) + "\n");
    data[escapeKey(tag)] = total;

# Get property "question max score"
saveDataObject();
data = createDataObject("questionMaxScore");
for tag in tags:
    sys.stdout.write("Getting question with maximal score for tag: " + tag + "\n");
    responseData = callQuestionMaxScoreApi(tag);
    total = responseData["total"]
    items = responseData["items"]
    score = 0 if total <= 0 else items[0]["score"];
    if useTagSynonyms != 0:
        for synonym in synonyms[tag]:
            sys.stdout.write("  - taking care of maximal questions score for synonym '" + synonym + "': ");
            synResponseData = callQuestionMaxScoreApi(synonym);
            synTotal = synResponseData["total"]
            synItems = synResponseData["items"]
            synScore = 0 if synTotal <= 0 else synItems[0]["score"];
            sys.stdout.write(synScore);
            sys.stdout.write("\n");
            if (synScore > score):
                score = synScore;
    sys.stdout.write(" - result: " + str(score) + "\n");
    data[escapeKey(tag)] = score;

saveDataObject();
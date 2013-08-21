# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)
# WARNING: This code is broken and out-of-date
# A pure Django version can be found at http://github.com/dj-foxxy/smsmuster

import json
import math
import os
import urllib
import urlparse

import scraperwiki

# The following scraper takes a text message that contains the name of the
# street the sender is current on or the postal code the sender is currently in
# and replies with the location of the most sensible evacuation point /muster
# point/safe house to go to.
#
# Usage:
# 
# http://scraperwikiviews.com/run/mustersm?phonenumber=[NUMBER]&message=[MESSAGE]
# 
# [NUMBER]  The number from which [MESSAGE] was received including the country
#           code.
#
# [MESSAGE] The message received from [NUMBER].
#
#
# The scraper also executes at administrative commands. To execute and
# administrative command your number must be included in the ADMIN_NUMBERS set.
#
# Commands:
#
# commands
#     List the available commands and how to use them.
#
# listmusters [NUMBER]
#     Lists the given number of closest muster points and their IDs.
#
# getstatus [ID]
#     Returns the status of the muster point (open/closed/out) and a message
#     about it, if one exists.
#
# setstatus [ID] [STATE] {MESSAGE}
#     Sets the status of a muster point (open/closed/out) and optional provide
#     a message describing the situation at the muster point.
#
# Currently the scraper is using places in Birmingham but it can easily be loads
# with place from other areas.
#
# Authors: 
#     Julian Todd
#     Peter Sutton (suttonp8@cs.man.ac.uk)


# =============================================================================
# = Constants                                                                 =
# =============================================================================

# The phone numbers that are allowed to execute administrative command.
# At the moment, the system does not understand the structure of phone numbers.
# Therefore, always include the country code.
ADMIN_NUMBERS = frozenset()

# The error messages returned to the requester when a phonenumber parameter is
# not given in the query string or it is empty.
ERROR_MESSAGE_NO_NUMBER = (
    "No phone number.Always supply a phonenumber value in the query string.")

# The error message returned to the sender when a message parameter is not
# given in the query string or it is empty.
ERROR_MESSAGE_BLANK_MESSAGE = (
    "Message empty. Reply with your current street name or post code.")

# The error message returned to the
ERROR_MESSAGE_COULD_NOT_LOCATION = (
    "Your location could not be found. Reply with your current street name "
    "or post code.")

# The error message returned when the location given in the listmusters command
# could not be found.
ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION = (
    "Could not find location. Ensure street name or postal code is correct.")

# The message that should be sent to every non-admin to inform them of the
# situation.
GLOBAL_MESSAGE = (
    "Fiveways Railway Station chemical spillage")

# The instructions returned by the "commands" admin command.
HANDLER_COMMANDS = (
    "listmusters [num] [location]| getstatus [id] | setstatus [id] [status] "
    "[message]")

# The error message returned if the listmusters command is invoked without a
# valid number as the first argument.
HANDLER_LISTMUSTERS_NUM_ERROR = (
    "1st argument must be a number. Please retry.")

# The latitude and longitude of the location of the incident. This is used
# when deciding where to send people (always away from this).
INCIDENT_LATLNG = scraperwiki.geo.gb_postcode_to_latlng("B15 2BJ")

# The maximum number of characters allowed in a message.
MAX_MESSAGE_LENGTH = 150

# The token used to separate messages in the reply
MESSAGE_SEPARATOR_TOKEN = "#"

# The string added to end of the Google Maps query. Use this for ensuring
# results are from the correct area.
QUERY_SUFFIX = " birmingham"

# If true, all phone number will be allowed to execute admin commands.
TEST_EVERYONE_IS_ADMIN = True

# The phone number from which the test text message was sent.
TEST_PHONE = "+445555555555"

# The test text message
TEST_MESSAGE = "Oval road"

# If true, the test phone number and message will be used.
TEST_USE_TEST_DATA = False

# =============================================================================


class TextMessage(object):
    def __init__(self, number, message):
        self.number = number.strip()
        self.message = message.strip().lower()
        self.tokens = self.message.split()
        self.latlng = get_latlng(self.message)
        self.directed_to = None

    def is_admin(self):
        return TEST_EVERYONE_IS_ADMIN or self.number in ADMIN_NUMBERS

    def is_command(self):
        return self.tokens[0] in HANDLER_MAP


# =============================================================================
# = Geographical Functions                                                    =
# =============================================================================

def get_distance(latlng_1, latlng_2):
    delta_lat = latlng_1[0] - latlng_2[0]
    delta_lon = latlng_1[1] - latlng_2[1]
    return math.sqrt(delta_lat * delta_lat + delta_lon * delta_lon)

def get_weighted_distance(p, m):
    i = INCIDENT_LATLNG
    v = m[0] - p[0], m[1] - p[1]
    d = i[0] - p[0], i[1] - p[1]
    vsq = v[0] * v[0] + v[1] * v[1] + 0.00001
    vlen = math.sqrt(vsq)
    a = abs((v[1] * d[0] - v[0] * d[1]) / vlen + 0.000001)
    x1 = (d[0] * v[0] + d[1] * v[1]) / vlen
    x2 = ((d[0] - v[0]) * v[0] + (d[1] - v[1]) * v[1]) / vlen
    ix1 = math.log((x1 + math.sqrt(x1 * x1 + a * a)) / a)
    ix2 = math.log((x2 + math.sqrt(x2 * x2 + a * a)) / a)
    r = abs(ix2 - ix1) * 0.1
    return r

def get_latlng(location_description, query_suffix=True):
    if query_suffix:
        location_description += QUERY_SUFFIX

    location_info = json.loads(urllib.urlopen(
        "http://maps.google.com/maps/geo?q=%s"
        % urllib.quote(location_description)).read())

    if "Placemark" not in location_info:
        return None

    # WARNING: We get LNG LAT...not LAT LNG as we use everywhere else. So it
    # needs reversing. And it's got a weird zero we don't need.

    return location_info["Placemark"][0]["Point"]["coordinates"][1::-1]

def get_muster_map():
    return dict((muster["id"], muster) for muster in
        scraperwiki.datastore.getData("birmingham-leisure-centres"))
# Maps muster ids to muster records.
MUSTER_MAP = get_muster_map()

def list_musters(latlng, open_only=False, weighted_distance=False):
    if weighted_distance:
        distance_measure = get_weighted_distance
    else:
        distance_measure = get_distance
    muster_statuses = dict((item["musterid"], item["status"]) 
        for item in scraperwiki.datastore.getData("mustersms") 
        if "musterid" in item)

    muster_distances = []
    for muster in scraperwiki.datastore.getData("birmingham-leisure-centres"):
        if "latlng" not in muster:
            continue
        if not open_only or muster_statuses.get(muster["id"]) == "open":
            muster_distances.append((
                distance_measure(latlng, muster["latlng"]), muster))
    muster_distances.sort(key=lambda x: x[0])
    return muster_distances

# =============================================================================


# =============================================================================
# = Command Handlers                                                          =
# =============================================================================

def handler_commands(text):
    return HANDLER_COMMANDS

def handler_listmusters(text):
    try:
        num = int(text.tokens[1])
    except (ValueError, IndexError):
        return HANDLER_LISTMUSTERS_NUM_ERROR

    latlng = get_latlng(" ".join(text.tokens[1:]))

    if latlng is None:
        return ERROR_MESSAGE_LISTERMUSTERS_COULD_NOT_FIND_LOCATION

    return " | ".join(["%s %s" % (muster["id"], muster["shortname"])
        for _distance, muster in list_musters(latlng)[:num]])


def handler_getstatus(text):
    for data in scraperwiki.datastore.getData("mustersms"):
        if data.get("musterid") == text.tokens[1]:
            return "%s %s %s" % (text.tokens[1], data.get("status"),
                data.get("message"))
    return "ERROR %s not found" % text.tokens[1]

def handler_setstatus(text):
    scraperwiki.datastore.save(unique_keys=["musterid"],
        data={"musterid":text.tokens[1], "status":text.tokens[2],
            "message":" ".join(text.tokens[3:])})
    return "Status set for %s" % text.tokens[1]

HANDLER_MAP = {
    "commands": handler_commands,
    "listmusters": handler_listmusters,
    "getstatus": handler_getstatus,
    "setstatus": handler_setstatus}

# =============================================================================


# =============================================================================
# = Request Handling                                                          =
# =============================================================================

# = Helpers ===================================================================
def log_text(text):
    scraperwiki.datastore.save(unique_keys=["phonenumber"],
        data={"phonenumber":text.number, "mid":text.directed_to},
        latlng=text.latlng)

def process_query_string(query_string):
    def get_value(key):
        if key in items and items[key] and items[key][0].strip():
            return items[key][0]
        return None
    items = urlparse.parse_qs(query_string)
    return (get_value("phonenumber"), get_value("message"))
# =============================================================================

def handle_text_message(text):
    reply_messages = []

    def add_reply(send_to, message):
        message = "%s %s" % (send_to, message[:MAX_MESSAGE_LENGTH])
        reply_messages.append(message)

    if text.is_admin() and text.is_command():
        # This is an admin trying to execute a command. Attempt to do their
        # bidding.
        add_reply(text.number, HANDLER_MAP[text.tokens[0]](text))

    else:
        # This is not an admin. Attempt to send them to a muster point.
        add_reply(text.number, GLOBAL_MESSAGE)

        if text.latlng is None:
            add_reply(text.number, ERROR_MESSAGE_COULD_NOT_LOCATION)
        else:
            closest_muster = list_musters(text.latlng, open_only=True,
                weighted_distance=True)[1][1]

            add_reply(text.number,
                "Safe place: %s, %s, %s"
                % (closest_muster["shortname"], 
                   closest_muster["street-address"],
                   closest_muster["telephone"]))

            text.directed_to = closest_muster["id"]

        log_text(text)

    return MESSAGE_SEPARATOR_TOKEN.join(reply_messages)

def main(use_test_data=False):
    if use_test_data:
        query_string = urllib.urlencode({"phonenumber": TEST_PHONE,
            "message": TEST_MESSAGE})
    else:
        query_string = os.getenv("URLQUERY")

    number, message = process_query_string(query_string)

    if number:
        print handle_text_message(TextMessage(number, message))
    else:
        print ERROR_MESSAGE_NO_NUMBER

# =============================================================================

# WARNING: If you get text messages going to the wrong phone or other weird
# behaviour, it is probably because you have forgotten to stop using the test
# data.
#main(use_test_data=TEST_USE_TEST_DATA)

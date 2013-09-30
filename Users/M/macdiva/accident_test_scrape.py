"""
import lxml.html

html = scraperwiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=50070")

parsed_html = lxml.html.document_fromstring(html)

for each_element in parsed_html:
    print lxml.html.tostring(each_element[0])

print parsed_html.get_element_by_id("table")

print root.xpath("/html/body/form/div/table[3]/tbody/tr[2]").text()
"""

import sys, os
import errno
import re
import string
import unicodedata

import scraperwiki

from BeautifulSoup import BeautifulSoup


# Do all pages
page_start_id = 29734

#page_last_id = 58660
page_last_id = 29738

column_name = None
not_letters_or_digits = u"`~!@#$%^*&()-_=+[]{}\|;:<>,./?'"


while (page_start_id <= page_last_id):
    # Fetch the page
    html = scraperwiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=" + str(page_start_id))

    html = "".join([line.strip() for line in html.split("\n")])

    # Create the soup object from the HTML data
    soup = BeautifulSoup(html)

    # Find the proper tag
    location_table = soup.findAll("table")[1]
    unit_table = soup.findAll("table")[2]
    environment_table = soup.findAll("table")[3]
    narrative_table = soup.findAll("table")[5]

    location_dict = {}
    unit_dict = {}
    environment_dict = {}
    narrative_dict = {}

    location_rows = location_table("tr")
    unit_rows = unit_table("tr")
    environment_rows = environment_table("tr")
    narrative_rows = narrative_table("tr")

    location_dict[u"page_id"] = unicode(page_start_id)
    unit_dict[u"page_id"] = unicode(page_start_id)
    environment_dict[u"page_id"] = unicode(page_start_id)
    narrative_dict[u"page_id"] = unicode(page_start_id)

    for each_row in location_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    location_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=location_dict)

    for each_row in unit_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    unit_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=unit_dict)

    for each_row in environment_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    environment_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=environment_dict)

    for each_row in narrative_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    narrative_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=narrative_dict)

    page_start_id += 1"""
import lxml.html

html = scraperwiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=50070")

parsed_html = lxml.html.document_fromstring(html)

for each_element in parsed_html:
    print lxml.html.tostring(each_element[0])

print parsed_html.get_element_by_id("table")

print root.xpath("/html/body/form/div/table[3]/tbody/tr[2]").text()
"""

import sys, os
import errno
import re
import string
import unicodedata

import scraperwiki

from BeautifulSoup import BeautifulSoup


# Do all pages
page_start_id = 29734

#page_last_id = 58660
page_last_id = 29738

column_name = None
not_letters_or_digits = u"`~!@#$%^*&()-_=+[]{}\|;:<>,./?'"


while (page_start_id <= page_last_id):
    # Fetch the page
    html = scraperwiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=" + str(page_start_id))

    html = "".join([line.strip() for line in html.split("\n")])

    # Create the soup object from the HTML data
    soup = BeautifulSoup(html)

    # Find the proper tag
    location_table = soup.findAll("table")[1]
    unit_table = soup.findAll("table")[2]
    environment_table = soup.findAll("table")[3]
    narrative_table = soup.findAll("table")[5]

    location_dict = {}
    unit_dict = {}
    environment_dict = {}
    narrative_dict = {}

    location_rows = location_table("tr")
    unit_rows = unit_table("tr")
    environment_rows = environment_table("tr")
    narrative_rows = narrative_table("tr")

    location_dict[u"page_id"] = unicode(page_start_id)
    unit_dict[u"page_id"] = unicode(page_start_id)
    environment_dict[u"page_id"] = unicode(page_start_id)
    narrative_dict[u"page_id"] = unicode(page_start_id)

    for each_row in location_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    location_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=location_dict)

    for each_row in unit_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    unit_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=unit_dict)

    for each_row in environment_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    environment_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=environment_dict)

    for each_row in narrative_rows:
        for each_col in each_row("td"):
            column_text = unicode(each_col.find("small", text=True))
            column_text = column_text.strip()

            if (column_text):
                column_text_final = ""
                column_text_list = []
                this_word = ""

                # Clean out any non alphanumeric character
                translate_to = u" "

                translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)

                column_text = column_text.translate(translate_table)

                # Tokenize the name, split on spaces
                column_text_list = column_text.split()

                # Capitalize each token
                for each_word in column_text_list:
                    this_word = each_word.capitalize()

                    # Concatenate all the names back together
                    column_text_final += this_word

                if (each_col.span):
                    column_value = each_col.span

                    narrative_dict[column_text_final] = column_value.string

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], data=narrative_dict)

    page_start_id += 1
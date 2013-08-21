import sys, os
import string

import scraperwiki

from BeautifulSoup import BeautifulSoup


# Do all pages
page_start_id_list = scraperwiki.sqlite.select("max(page_id) from location")
page_start_id = int(page_start_id_list[0]["max(page_id)"]) + 1
page_last_id = 58660
page_counter = page_start_id

column_name = None
not_letters_or_digits = u"`~!@#$%^*&()-_=+[]{}\|;:<>,./?'"

while (page_counter <= page_last_id):
    # Fetch the page
    html = scraperwiki.scrape("http://accidentreports.iowa.gov/index.php?pgname=IDOT_IOR_MV_Accident_details&id=" + str(page_counter))

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

    location_dict[u"page_id"] = unicode(page_counter)
    unit_dict[u"page_id"] = unicode(page_counter)
    environment_dict[u"page_id"] = unicode(page_counter)
    narrative_dict[u"page_id"] = unicode(page_counter)

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

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], table_name="location", data=location_dict)

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

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], table_name="unit", data=unit_dict)

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

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], table_name="environment", data=environment_dict)

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

    scraperwiki.sqlite.save(unique_keys=[u"page_id"], table_name="narrative", data=narrative_dict)

    page_counter += 1
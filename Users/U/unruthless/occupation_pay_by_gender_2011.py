# #############################################################################
# LIBRARIES

import scraperwiki
import urllib
import lxml.html

# #############################################################################
# DATA SOURCE
# http://www.bls.gov/cps/cpsaat39.htm

source = "http://www.bls.gov/cps/cpsaat39.htm"

# #############################################################################
# SCRAPE HTML

html = urllib.urlopen(source).read()

# #############################################################################
# PARSE HTML

root = lxml.html.fromstring(html);

rows = root.cssselect("table#cps_eeann_mwe_ft_det_occu tbody tr")

subs = []

ldata = []

for row in rows[1:]:

    # Skip separator rows and last row of table
    if row.cssselect("tr.sep") or row.cssselect("tr.endnotes"):
        continue

    # Get the content of each item as string, as a list
    vals = [item.text_content() for item in row]

    assert row.cssselect("th p"), lxml.html.tostring(row)

    sub = row.cssselect("th p")[0].attrib.get("class")

    assert sub[:3] == "sub"

    isub = int(sub[3:])

    del subs[isub:]

    subs.append((isub,vals[0]))

    # Build data 
    data = {}

    data["occupation"] = vals[0].lower()

    for i,s in subs:
        data["level_%d" % i] = s

    fields = ["t_number_of_workers",
              "t_median_weekly_earnings",
              "m_number_of_workers",
              "m_median_weekly_earnings",
              "w_number_of_workers",
              "w_median_weekly_earnings"]

    for field,val in zip(fields,vals[1:]):
        if val != "-":
            data[field] = int(val.replace(",",""))

    if vals[4] != "-" and vals[6] != "-":
        
        # For clarity. This can probably be made more efficient.
        t_median_weekly_earnings = int(vals[2].replace(",",""))
        m_median_weekly_earnings = int(vals[4].replace(",",""))
        w_median_weekly_earnings = int(vals[6].replace(",",""))
        pay_gap_weekly = m_median_weekly_earnings - w_median_weekly_earnings

        data["pay_gap_weekly"] = pay_gap_weekly
        data["is_pay_gap"] = "y" if pay_gap_weekly > 0 else "n"
        data["pay_gap_yearly"] = 52 * pay_gap_weekly
        data["cents_on_the_dollar"] = int( 100 * ( ( float(m_median_weekly_earnings) - float(pay_gap_weekly) ) / float(m_median_weekly_earnings) ) )
    
    ldata.append(data)

# #############################################################################
# WRITE TO DATABASE

scraperwiki.sqlite.execute("""
DROP TABLE IF EXISTS occ_pay_by_gender
""")

scraperwiki.sqlite.execute("""
CREATE TABLE `occ_pay_by_gender`
(
    `occupation` text,
    `level_0` text,
    `level_1` text,
    `level_2` text,
    `level_3` text,
    `w_number_of_workers` integer,
    `w_median_weekly_earnings` integer,
    `m_number_of_workers` integer,
    `m_median_weekly_earnings` integer,
    `t_number_of_workers` integer,
    `t_median_weekly_earnings` integer,
    `is_pay_gap` boolean,
    `cents_on_the_dollar` integer,
    `pay_gap_weekly` integer,
    `pay_gap_yearly` integer
)
""")

scraperwiki.sqlite.save(["occupation"],ldata,"occ_pay_by_gender")

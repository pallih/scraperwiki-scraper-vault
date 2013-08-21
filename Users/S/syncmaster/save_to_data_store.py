import scraperwiki

# Blank Python
title = "drupal"
app_url = "http://stackoverflow.com/questions/9013485/c-how-to-merge-sorted-vectors-into-a-sorted-vector-pop-the-least-element-fro/9048857#9048857"
app_desc = "Since our launch, we have seen over 958,997 page views, acquired over 985 members organically and consistently growing; we continue to acquire new members using the latest emarketing tools and techniques. Also, we have access to a complete directory of over 500,000+ businesses and government agency contact details and we plan to fully utilize this directory by executing targeted marketing campaigns to keep PWAPN members fully engaged within the public works industry. While we are enhancing our services, we will also continue to make our Business and Government profile services FREE of charge so that organizations who provide services and solutions to the Public Works Industry can have the all the tools necessary to promote their professional capabilities to key contacts."

print title
print app_url
print app_desc
scraperwiki.sqlite.save(unique_keys=["url"], data={"name":title, "url":app_url, "description":app_desc}, table_name = "army_ants_civic_commons_apps")

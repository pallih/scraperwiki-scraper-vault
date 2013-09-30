import scraperwiki

# import numpy as np
# import matplotlib.pyplot as plt

scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")

scraperwiki.sqlite.execute("""
CREATE VIEW monthly_lottery_funding AS
  SELECT `Local authority`, strftime("%Y",`Grant date`) AS `Grant year`, strftime("%M",`Grant date`) AS `Grant month`, SUM(`Grant amount`) AS amount
    FROM uk_lottery_scrapedownload_1.swdata
    GROUP BY `Local authority`, strftime("%Y",`Grant date`), strftime("%M",`Grant date`);
""")

scraperwiki.sqlite.execute("""
CREATE VIEW quarterly_lottery_funding AS
  SELECT `Local authority`, `Grant year`, `Grant month` / 3, SUM(amount) AS amount
    FROM monthly_lottery_funding
    GROUP BY `Local authority`, `Grant year`, `Grant month`;
""")

# scraperwiki.sqli

def quarterly_lottery_funding(local_authority):
    pass


    
import scraperwiki

# import numpy as np
# import matplotlib.pyplot as plt

scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")

scraperwiki.sqlite.execute("""
CREATE VIEW monthly_lottery_funding AS
  SELECT `Local authority`, strftime("%Y",`Grant date`) AS `Grant year`, strftime("%M",`Grant date`) AS `Grant month`, SUM(`Grant amount`) AS amount
    FROM uk_lottery_scrapedownload_1.swdata
    GROUP BY `Local authority`, strftime("%Y",`Grant date`), strftime("%M",`Grant date`);
""")

scraperwiki.sqlite.execute("""
CREATE VIEW quarterly_lottery_funding AS
  SELECT `Local authority`, `Grant year`, `Grant month` / 3, SUM(amount) AS amount
    FROM monthly_lottery_funding
    GROUP BY `Local authority`, `Grant year`, `Grant month`;
""")

# scraperwiki.sqli

def quarterly_lottery_funding(local_authority):
    pass


    

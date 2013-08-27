"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.irishstatutebook.ie/2010/en/si/0001.html
http://www.irishstatutebook.ie/2010/en/si/0002.html
http://www.irishstatutebook.ie/2010/en/si/0003.html
http://www.irishstatutebook.ie/2010/en/si/0004.html
http://www.irishstatutebook.ie/2010/en/si/0005.html
http://www.irishstatutebook.ie/2010/en/si/0006.html
http://www.irishstatutebook.ie/2010/en/si/0007.html
http://www.irishstatutebook.ie/2010/en/si/0008.html
http://www.irishstatutebook.ie/2010/en/si/0009.html
http://www.irishstatutebook.ie/2010/en/si/0010.html
http://www.irishstatutebook.ie/2010/en/si/0011.html
http://www.irishstatutebook.ie/2010/en/si/0012.html
http://www.irishstatutebook.ie/2010/en/si/0013.html
http://www.irishstatutebook.ie/2010/en/si/0014.html
http://www.irishstatutebook.ie/2010/en/si/0015.html
http://www.irishstatutebook.ie/2010/en/si/0016.html
http://www.irishstatutebook.ie/2010/en/si/0017.html
http://www.irishstatutebook.ie/2010/en/si/0018.html
http://www.irishstatutebook.ie/2010/en/si/0019.html
http://www.irishstatutebook.ie/2010/en/si/0020.html
http://www.irishstatutebook.ie/2010/en/si/0021.html
http://www.irishstatutebook.ie/2010/en/si/0022.html
http://www.irishstatutebook.ie/2010/en/si/0023.html
http://www.irishstatutebook.ie/2010/en/si/0024.html
http://www.irishstatutebook.ie/2010/en/si/0025.html
http://www.irishstatutebook.ie/2010/en/si/0026.html
http://www.irishstatutebook.ie/2010/en/si/0027.html
http://www.irishstatutebook.ie/2010/en/si/0028.html
http://www.irishstatutebook.ie/2010/en/si/0029.html
http://www.irishstatutebook.ie/2010/en/si/0030.html
http://www.irishstatutebook.ie/2010/en/si/0031.html
http://www.irishstatutebook.ie/2010/en/si/0032.html
http://www.irishstatutebook.ie/2010/en/si/0033.html
http://www.irishstatutebook.ie/2010/en/si/0034.html
http://www.irishstatutebook.ie/2010/en/si/0035.html
http://www.irishstatutebook.ie/2010/en/si/0036.html
http://www.irishstatutebook.ie/2010/en/si/0037.html
http://www.irishstatutebook.ie/2010/en/si/0038.html
http://www.irishstatutebook.ie/2010/en/si/0039.html
http://www.irishstatutebook.ie/2010/en/si/0040.html
http://www.irishstatutebook.ie/2010/en/si/0041.html
http://www.irishstatutebook.ie/2010/en/si/0042.html
http://www.irishstatutebook.ie/2010/en/si/0043.html
http://www.irishstatutebook.ie/2010/en/si/0044.html
http://www.irishstatutebook.ie/2010/en/si/0045.html
http://www.irishstatutebook.ie/2010/en/si/0046.html
http://www.irishstatutebook.ie/2010/en/si/0047.html
http://www.irishstatutebook.ie/2010/en/si/0048.html
http://www.irishstatutebook.ie/2010/en/si/0049.html
http://www.irishstatutebook.ie/2010/en/si/0050.html
http://www.irishstatutebook.ie/2010/en/si/0051.html
http://www.irishstatutebook.ie/2010/en/si/0052.html
http://www.irishstatutebook.ie/2010/en/si/0053.html
http://www.irishstatutebook.ie/2010/en/si/0054.html
http://www.irishstatutebook.ie/2010/en/si/0055.html
http://www.irishstatutebook.ie/2010/en/si/0056.html
http://www.irishstatutebook.ie/2010/en/si/0057.html
http://www.irishstatutebook.ie/2010/en/si/0058.html
http://www.irishstatutebook.ie/2010/en/si/0059.html
http://www.irishstatutebook.ie/2010/en/si/0060.html
http://www.irishstatutebook.ie/2010/en/si/0061.html
http://www.irishstatutebook.ie/2010/en/si/0062.html
http://www.irishstatutebook.ie/2010/en/si/0063.html
http://www.irishstatutebook.ie/2010/en/si/0064.html
http://www.irishstatutebook.ie/2010/en/si/0065.html
http://www.irishstatutebook.ie/2010/en/si/0066.html
http://www.irishstatutebook.ie/2010/en/si/0067.html
http://www.irishstatutebook.ie/2010/en/si/0068.html
http://www.irishstatutebook.ie/2010/en/si/0069.html
http://www.irishstatutebook.ie/2010/en/si/0070.html
http://www.irishstatutebook.ie/2010/en/si/0071.html
http://www.irishstatutebook.ie/2010/en/si/0072.html
http://www.irishstatutebook.ie/2010/en/si/0073.html
http://www.irishstatutebook.ie/2010/en/si/0074.html
http://www.irishstatutebook.ie/2010/en/si/0075.html
http://www.irishstatutebook.ie/2010/en/si/0076.html
http://www.irishstatutebook.ie/2010/en/si/0077.html
http://www.irishstatutebook.ie/2010/en/si/0078.html
http://www.irishstatutebook.ie/2010/en/si/0079.html
http://www.irishstatutebook.ie/2010/en/si/0080.html
http://www.irishstatutebook.ie/2010/en/si/0081.html
http://www.irishstatutebook.ie/2010/en/si/0082.html
http://www.irishstatutebook.ie/2010/en/si/0083.html
http://www.irishstatutebook.ie/2010/en/si/0084.html
http://www.irishstatutebook.ie/2010/en/si/0085.html
http://www.irishstatutebook.ie/2010/en/si/0086.html
http://www.irishstatutebook.ie/2010/en/si/0087.html
http://www.irishstatutebook.ie/2010/en/si/0088.html
http://www.irishstatutebook.ie/2010/en/si/0089.html
http://www.irishstatutebook.ie/2010/en/si/0090.html
http://www.irishstatutebook.ie/2010/en/si/0091.html
http://www.irishstatutebook.ie/2010/en/si/0092.html
http://www.irishstatutebook.ie/2010/en/si/0093.html
http://www.irishstatutebook.ie/2010/en/si/0094.html
http://www.irishstatutebook.ie/2010/en/si/0095.html
http://www.irishstatutebook.ie/2010/en/si/0096.html
http://www.irishstatutebook.ie/2010/en/si/0097.html
http://www.irishstatutebook.ie/2010/en/si/0098.html
http://www.irishstatutebook.ie/2010/en/si/0099.html
http://www.irishstatutebook.ie/2010/en/si/0100.html
http://www.irishstatutebook.ie/2010/en/si/0101.html
http://www.irishstatutebook.ie/2010/en/si/0102.html
http://www.irishstatutebook.ie/2010/en/si/0103.html
http://www.irishstatutebook.ie/2010/en/si/0104.html
http://www.irishstatutebook.ie/2010/en/si/0105.html
http://www.irishstatutebook.ie/2010/en/si/0106.html
http://www.irishstatutebook.ie/2010/en/si/0107.html
http://www.irishstatutebook.ie/2010/en/si/0108.html
http://www.irishstatutebook.ie/2010/en/si/0109.html
http://www.irishstatutebook.ie/2010/en/si/0110.html
http://www.irishstatutebook.ie/2010/en/si/0111.html
http://www.irishstatutebook.ie/2010/en/si/0112.html
http://www.irishstatutebook.ie/2010/en/si/0113.html
http://www.irishstatutebook.ie/2010/en/si/0114.html
http://www.irishstatutebook.ie/2010/en/si/0115.html
http://www.irishstatutebook.ie/2010/en/si/0116.html
http://www.irishstatutebook.ie/2010/en/si/0117.html
http://www.irishstatutebook.ie/2010/en/si/0118.html
http://www.irishstatutebook.ie/2010/en/si/0119.html
http://www.irishstatutebook.ie/2010/en/si/0120.html
http://www.irishstatutebook.ie/2010/en/si/0121.html
http://www.irishstatutebook.ie/2010/en/si/0122.html
http://www.irishstatutebook.ie/2010/en/si/0123.html
http://www.irishstatutebook.ie/2010/en/si/0124.html
http://www.irishstatutebook.ie/2010/en/si/0125.html
http://www.irishstatutebook.ie/2010/en/si/0126.html
http://www.irishstatutebook.ie/2010/en/si/0127.html
http://www.irishstatutebook.ie/2010/en/si/0128.html
http://www.irishstatutebook.ie/2010/en/si/0129.html
http://www.irishstatutebook.ie/2010/en/si/0130.html
http://www.irishstatutebook.ie/2010/en/si/0131.html
http://www.irishstatutebook.ie/2010/en/si/0132.html
http://www.irishstatutebook.ie/2010/en/si/0133.html
http://www.irishstatutebook.ie/2010/en/si/0134.html
http://www.irishstatutebook.ie/2010/en/si/0135.html
http://www.irishstatutebook.ie/2010/en/si/0136.html
http://www.irishstatutebook.ie/2010/en/si/0137.html
http://www.irishstatutebook.ie/2010/en/si/0138.html
http://www.irishstatutebook.ie/2010/en/si/0139.html
http://www.irishstatutebook.ie/2010/en/si/0140.html
http://www.irishstatutebook.ie/2010/en/si/0141.html
http://www.irishstatutebook.ie/2010/en/si/0142.html
http://www.irishstatutebook.ie/2010/en/si/0143.html
http://www.irishstatutebook.ie/2010/en/si/0144.html
http://www.irishstatutebook.ie/2010/en/si/0145.html
http://www.irishstatutebook.ie/2010/en/si/0146.html
http://www.irishstatutebook.ie/2010/en/si/0147.html
http://www.irishstatutebook.ie/2010/en/si/0148.html
http://www.irishstatutebook.ie/2010/en/si/0149.html
http://www.irishstatutebook.ie/2010/en/si/0150.html
http://www.irishstatutebook.ie/2010/en/si/0151.html
http://www.irishstatutebook.ie/2010/en/si/0152.html
http://www.irishstatutebook.ie/2010/en/si/0153.html
http://www.irishstatutebook.ie/2010/en/si/0154.html
http://www.irishstatutebook.ie/2010/en/si/0155.html
http://www.irishstatutebook.ie/2010/en/si/0156.html
http://www.irishstatutebook.ie/2010/en/si/0157.html
http://www.irishstatutebook.ie/2010/en/si/0158.html
http://www.irishstatutebook.ie/2010/en/si/0159.html
http://www.irishstatutebook.ie/2010/en/si/0160.html
http://www.irishstatutebook.ie/2010/en/si/0161.html
http://www.irishstatutebook.ie/2010/en/si/0162.html
http://www.irishstatutebook.ie/2010/en/si/0163.html
http://www.irishstatutebook.ie/2010/en/si/0164.html
http://www.irishstatutebook.ie/2010/en/si/0165.html
http://www.irishstatutebook.ie/2010/en/si/0166.html
http://www.irishstatutebook.ie/2010/en/si/0167.html
http://www.irishstatutebook.ie/2010/en/si/0168.html
http://www.irishstatutebook.ie/2010/en/si/0169.html
http://www.irishstatutebook.ie/2010/en/si/0170.html
http://www.irishstatutebook.ie/2010/en/si/0171.html
http://www.irishstatutebook.ie/2010/en/si/0172.html
http://www.irishstatutebook.ie/2010/en/si/0173.html
http://www.irishstatutebook.ie/2010/en/si/0174.html
http://www.irishstatutebook.ie/2010/en/si/0175.html
http://www.irishstatutebook.ie/2010/en/si/0176.html
http://www.irishstatutebook.ie/2010/en/si/0177.html
http://www.irishstatutebook.ie/2010/en/si/0178.html
http://www.irishstatutebook.ie/2010/en/si/0179.html
http://www.irishstatutebook.ie/2010/en/si/0180.html
http://www.irishstatutebook.ie/2010/en/si/0181.html
http://www.irishstatutebook.ie/2010/en/si/0182.html
http://www.irishstatutebook.ie/2010/en/si/0183.html
http://www.irishstatutebook.ie/2010/en/si/0184.html
http://www.irishstatutebook.ie/2010/en/si/0185.html
http://www.irishstatutebook.ie/2010/en/si/0186.html
http://www.irishstatutebook.ie/2010/en/si/0187.html
http://www.irishstatutebook.ie/2010/en/si/0188.html
http://www.irishstatutebook.ie/2010/en/si/0189.html
http://www.irishstatutebook.ie/2010/en/si/0190.html
http://www.irishstatutebook.ie/2010/en/si/0191.html
http://www.irishstatutebook.ie/2010/en/si/0192.html
http://www.irishstatutebook.ie/2010/en/si/0193.html
http://www.irishstatutebook.ie/2010/en/si/0194.html
http://www.irishstatutebook.ie/2010/en/si/0195.html
http://www.irishstatutebook.ie/2010/en/si/0196.html
http://www.irishstatutebook.ie/2010/en/si/0197.html
http://www.irishstatutebook.ie/2010/en/si/0198.html
http://www.irishstatutebook.ie/2010/en/si/0199.html
http://www.irishstatutebook.ie/2010/en/si/0200.html
http://www.irishstatutebook.ie/2010/en/si/0201.html
http://www.irishstatutebook.ie/2010/en/si/0202.html
http://www.irishstatutebook.ie/2010/en/si/0203.html
http://www.irishstatutebook.ie/2010/en/si/0204.html
http://www.irishstatutebook.ie/2010/en/si/0205.html
http://www.irishstatutebook.ie/2010/en/si/0206.html
http://www.irishstatutebook.ie/2010/en/si/0207.html
http://www.irishstatutebook.ie/2010/en/si/0208.html
http://www.irishstatutebook.ie/2010/en/si/0209.html
http://www.irishstatutebook.ie/2010/en/si/0210.html
http://www.irishstatutebook.ie/2010/en/si/0211.html
http://www.irishstatutebook.ie/2010/en/si/0212.html
http://www.irishstatutebook.ie/2010/en/si/0213.html
http://www.irishstatutebook.ie/2010/en/si/0214.html
http://www.irishstatutebook.ie/2010/en/si/0215.html
http://www.irishstatutebook.ie/2010/en/si/0216.html
http://www.irishstatutebook.ie/2010/en/si/0217.html
http://www.irishstatutebook.ie/2010/en/si/0218.html
http://www.irishstatutebook.ie/2010/en/si/0219.html
http://www.irishstatutebook.ie/2010/en/si/0220.html
http://www.irishstatutebook.ie/2010/en/si/0221.html
http://www.irishstatutebook.ie/2010/en/si/0222.html
http://www.irishstatutebook.ie/2010/en/si/0223.html
http://www.irishstatutebook.ie/2010/en/si/0224.html
http://www.irishstatutebook.ie/2010/en/si/0225.html
http://www.irishstatutebook.ie/2010/en/si/0226.html
http://www.irishstatutebook.ie/2010/en/si/0227.html
http://www.irishstatutebook.ie/2010/en/si/0228.html
http://www.irishstatutebook.ie/2010/en/si/0229.html
http://www.irishstatutebook.ie/2010/en/si/0230.html
http://www.irishstatutebook.ie/2010/en/si/0231.html
http://www.irishstatutebook.ie/2010/en/si/0232.html
http://www.irishstatutebook.ie/2010/en/si/0233.html
http://www.irishstatutebook.ie/2010/en/si/0234.html
http://www.irishstatutebook.ie/2010/en/si/0235.html
http://www.irishstatutebook.ie/2010/en/si/0236.html
http://www.irishstatutebook.ie/2010/en/si/0237.html
http://www.irishstatutebook.ie/2010/en/si/0238.html
http://www.irishstatutebook.ie/2010/en/si/0239.html
http://www.irishstatutebook.ie/2010/en/si/0240.html
http://www.irishstatutebook.ie/2010/en/si/0241.html
http://www.irishstatutebook.ie/2010/en/si/0242.html
http://www.irishstatutebook.ie/2010/en/si/0243.html
http://www.irishstatutebook.ie/2010/en/si/0244.html
http://www.irishstatutebook.ie/2010/en/si/0245.html
http://www.irishstatutebook.ie/2010/en/si/0246.html
http://www.irishstatutebook.ie/2010/en/si/0247.html
http://www.irishstatutebook.ie/2010/en/si/0248.html
http://www.irishstatutebook.ie/2010/en/si/0249.html
http://www.irishstatutebook.ie/2010/en/si/0250.html
http://www.irishstatutebook.ie/2010/en/si/0251.html
http://www.irishstatutebook.ie/2010/en/si/0252.html
http://www.irishstatutebook.ie/2010/en/si/0253.html
http://www.irishstatutebook.ie/2010/en/si/0254.html
http://www.irishstatutebook.ie/2010/en/si/0255.html
http://www.irishstatutebook.ie/2010/en/si/0256.html
http://www.irishstatutebook.ie/2010/en/si/0257.html
http://www.irishstatutebook.ie/2010/en/si/0258.html
http://www.irishstatutebook.ie/2010/en/si/0259.html
http://www.irishstatutebook.ie/2010/en/si/0260.html
http://www.irishstatutebook.ie/2010/en/si/0261.html
http://www.irishstatutebook.ie/2010/en/si/0262.html
http://www.irishstatutebook.ie/2010/en/si/0263.html
http://www.irishstatutebook.ie/2010/en/si/0264.html
http://www.irishstatutebook.ie/2010/en/si/0265.html
http://www.irishstatutebook.ie/2010/en/si/0266.html
http://www.irishstatutebook.ie/2010/en/si/0267.html
http://www.irishstatutebook.ie/2010/en/si/0268.html
http://www.irishstatutebook.ie/2010/en/si/0269.html
http://www.irishstatutebook.ie/2010/en/si/0270.html
http://www.irishstatutebook.ie/2010/en/si/0271.html
http://www.irishstatutebook.ie/2010/en/si/0272.html
http://www.irishstatutebook.ie/2010/en/si/0273.html
http://www.irishstatutebook.ie/2010/en/si/0274.html
http://www.irishstatutebook.ie/2010/en/si/0275.html
http://www.irishstatutebook.ie/2010/en/si/0276.html
http://www.irishstatutebook.ie/2010/en/si/0277.html
http://www.irishstatutebook.ie/2010/en/si/0278.html
http://www.irishstatutebook.ie/2010/en/si/0279.html
http://www.irishstatutebook.ie/2010/en/si/0280.html
http://www.irishstatutebook.ie/2010/en/si/0281.html
http://www.irishstatutebook.ie/2010/en/si/0282.html
http://www.irishstatutebook.ie/2010/en/si/0283.html
http://www.irishstatutebook.ie/2010/en/si/0284.html
http://www.irishstatutebook.ie/2010/en/si/0285.html
http://www.irishstatutebook.ie/2010/en/si/0286.html
http://www.irishstatutebook.ie/2010/en/si/0287.html
http://www.irishstatutebook.ie/2010/en/si/0288.html
http://www.irishstatutebook.ie/2010/en/si/0289.html
http://www.irishstatutebook.ie/2010/en/si/0290.html
http://www.irishstatutebook.ie/2010/en/si/0291.html
http://www.irishstatutebook.ie/2010/en/si/0292.html
http://www.irishstatutebook.ie/2010/en/si/0293.html
http://www.irishstatutebook.ie/2010/en/si/0294.html
http://www.irishstatutebook.ie/2010/en/si/0295.html
http://www.irishstatutebook.ie/2010/en/si/0296.html
http://www.irishstatutebook.ie/2010/en/si/0297.html
http://www.irishstatutebook.ie/2010/en/si/0298.html
http://www.irishstatutebook.ie/2010/en/si/0299.html
http://www.irishstatutebook.ie/2010/en/si/0300.html
http://www.irishstatutebook.ie/2010/en/si/0301.html
http://www.irishstatutebook.ie/2010/en/si/0302.html
http://www.irishstatutebook.ie/2010/en/si/0303.html
http://www.irishstatutebook.ie/2010/en/si/0304.html
http://www.irishstatutebook.ie/2010/en/si/0305.html
http://www.irishstatutebook.ie/2010/en/si/0306.html
http://www.irishstatutebook.ie/2010/en/si/0307.html
http://www.irishstatutebook.ie/2010/en/si/0308.html
http://www.irishstatutebook.ie/2010/en/si/0309.html
http://www.irishstatutebook.ie/2010/en/si/0310.html
http://www.irishstatutebook.ie/2010/en/si/0311.html
http://www.irishstatutebook.ie/2010/en/si/0312.html
http://www.irishstatutebook.ie/2010/en/si/0313.html
http://www.irishstatutebook.ie/2010/en/si/0314.html
http://www.irishstatutebook.ie/2010/en/si/0315.html
http://www.irishstatutebook.ie/2010/en/si/0316.html
http://www.irishstatutebook.ie/2010/en/si/0317.html
http://www.irishstatutebook.ie/2010/en/si/0318.html
http://www.irishstatutebook.ie/2010/en/si/0319.html
http://www.irishstatutebook.ie/2010/en/si/0320.html
http://www.irishstatutebook.ie/2010/en/si/0321.html
http://www.irishstatutebook.ie/2010/en/si/0322.html
http://www.irishstatutebook.ie/2010/en/si/0323.html
http://www.irishstatutebook.ie/2010/en/si/0324.html
http://www.irishstatutebook.ie/2010/en/si/0325.html
http://www.irishstatutebook.ie/2010/en/si/0326.html
http://www.irishstatutebook.ie/2010/en/si/0327.html
http://www.irishstatutebook.ie/2010/en/si/0328.html
http://www.irishstatutebook.ie/2010/en/si/0329.html
http://www.irishstatutebook.ie/2010/en/si/0330.html
http://www.irishstatutebook.ie/2010/en/si/0331.html
http://www.irishstatutebook.ie/2010/en/si/0332.html
http://www.irishstatutebook.ie/2010/en/si/0333.html
http://www.irishstatutebook.ie/2010/en/si/0334.html
http://www.irishstatutebook.ie/2010/en/si/0335.html
http://www.irishstatutebook.ie/2010/en/si/0336.html
http://www.irishstatutebook.ie/2010/en/si/0337.html
http://www.irishstatutebook.ie/2010/en/si/0338.html
http://www.irishstatutebook.ie/2010/en/si/0339.html
http://www.irishstatutebook.ie/2010/en/si/0340.html
http://www.irishstatutebook.ie/2010/en/si/0341.html
http://www.irishstatutebook.ie/2010/en/si/0342.html
http://www.irishstatutebook.ie/2010/en/si/0343.html
http://www.irishstatutebook.ie/2010/en/si/0344.html
http://www.irishstatutebook.ie/2010/en/si/0345.html
http://www.irishstatutebook.ie/2010/en/si/0346.html
http://www.irishstatutebook.ie/2010/en/si/0347.html
http://www.irishstatutebook.ie/2010/en/si/0348.html
http://www.irishstatutebook.ie/2010/en/si/0349.html
http://www.irishstatutebook.ie/2010/en/si/0350.html
http://www.irishstatutebook.ie/2010/en/si/0351.html
http://www.irishstatutebook.ie/2010/en/si/0352.html
http://www.irishstatutebook.ie/2010/en/si/0353.html
http://www.irishstatutebook.ie/2010/en/si/0354.html
http://www.irishstatutebook.ie/2010/en/si/0355.html
http://www.irishstatutebook.ie/2010/en/si/0356.html
http://www.irishstatutebook.ie/2010/en/si/0357.html
http://www.irishstatutebook.ie/2010/en/si/0358.html
http://www.irishstatutebook.ie/2010/en/si/0359.html
http://www.irishstatutebook.ie/2010/en/si/0360.html
http://www.irishstatutebook.ie/2010/en/si/0361.html
http://www.irishstatutebook.ie/2010/en/si/0362.html
http://www.irishstatutebook.ie/2010/en/si/0363.html
http://www.irishstatutebook.ie/2010/en/si/0364.html
http://www.irishstatutebook.ie/2010/en/si/0365.html
http://www.irishstatutebook.ie/2010/en/si/0366.html
http://www.irishstatutebook.ie/2010/en/si/0367.html
http://www.irishstatutebook.ie/2010/en/si/0368.html
http://www.irishstatutebook.ie/2010/en/si/0369.html
http://www.irishstatutebook.ie/2010/en/si/0370.html
http://www.irishstatutebook.ie/2010/en/si/0371.html
http://www.irishstatutebook.ie/2010/en/si/0372.html
http://www.irishstatutebook.ie/2010/en/si/0373.html
http://www.irishstatutebook.ie/2010/en/si/0374.html
http://www.irishstatutebook.ie/2010/en/si/0375.html
http://www.irishstatutebook.ie/2010/en/si/0376.html
http://www.irishstatutebook.ie/2010/en/si/0377.html
http://www.irishstatutebook.ie/2010/en/si/0378.html
http://www.irishstatutebook.ie/2010/en/si/0379.html
http://www.irishstatutebook.ie/2010/en/si/0380.html
http://www.irishstatutebook.ie/2010/en/si/0381.html
http://www.irishstatutebook.ie/2010/en/si/0382.html
http://www.irishstatutebook.ie/2010/en/si/0383.html
http://www.irishstatutebook.ie/2010/en/si/0384.html
http://www.irishstatutebook.ie/2010/en/si/0385.html
http://www.irishstatutebook.ie/2010/en/si/0386.html
http://www.irishstatutebook.ie/2010/en/si/0387.html
http://www.irishstatutebook.ie/2010/en/si/0388.html
http://www.irishstatutebook.ie/2010/en/si/0389.html
http://www.irishstatutebook.ie/2010/en/si/0390.html
http://www.irishstatutebook.ie/2010/en/si/0391.html
http://www.irishstatutebook.ie/2010/en/si/0392.html
http://www.irishstatutebook.ie/2010/en/si/0393.html
http://www.irishstatutebook.ie/2010/en/si/0394.html
http://www.irishstatutebook.ie/2010/en/si/0395.html
http://www.irishstatutebook.ie/2010/en/si/0396.html
http://www.irishstatutebook.ie/2010/en/si/0397.html
http://www.irishstatutebook.ie/2010/en/si/0398.html
http://www.irishstatutebook.ie/2010/en/si/0399.html
http://www.irishstatutebook.ie/2010/en/si/0400.html
http://www.irishstatutebook.ie/2010/en/si/0401.html
http://www.irishstatutebook.ie/2010/en/si/0402.html
http://www.irishstatutebook.ie/2010/en/si/0403.html
http://www.irishstatutebook.ie/2010/en/si/0404.html
http://www.irishstatutebook.ie/2010/en/si/0405.html
http://www.irishstatutebook.ie/2010/en/si/0406.html
http://www.irishstatutebook.ie/2010/en/si/0407.html
http://www.irishstatutebook.ie/2010/en/si/0408.html
http://www.irishstatutebook.ie/2010/en/si/0409.html
http://www.irishstatutebook.ie/2010/en/si/0410.html
http://www.irishstatutebook.ie/2010/en/si/0411.html
http://www.irishstatutebook.ie/2010/en/si/0412.html
http://www.irishstatutebook.ie/2010/en/si/0413.html
http://www.irishstatutebook.ie/2010/en/si/0414.html
http://www.irishstatutebook.ie/2010/en/si/0415.html
http://www.irishstatutebook.ie/2010/en/si/0416.html
http://www.irishstatutebook.ie/2010/en/si/0417.html
http://www.irishstatutebook.ie/2010/en/si/0418.html
http://www.irishstatutebook.ie/2010/en/si/0419.html
http://www.irishstatutebook.ie/2010/en/si/0420.html
http://www.irishstatutebook.ie/2010/en/si/0421.html
http://www.irishstatutebook.ie/2010/en/si/0422.html
http://www.irishstatutebook.ie/2010/en/si/0423.html
http://www.irishstatutebook.ie/2010/en/si/0424.html
http://www.irishstatutebook.ie/2010/en/si/0425.html
http://www.irishstatutebook.ie/2010/en/si/0426.html
http://www.irishstatutebook.ie/2010/en/si/0427.html
http://www.irishstatutebook.ie/2010/en/si/0428.html
http://www.irishstatutebook.ie/2010/en/si/0429.html
http://www.irishstatutebook.ie/2010/en/si/0430.html
http://www.irishstatutebook.ie/2010/en/si/0431.html
http://www.irishstatutebook.ie/2010/en/si/0432.html
http://www.irishstatutebook.ie/2010/en/si/0433.html
http://www.irishstatutebook.ie/2010/en/si/0434.html
http://www.irishstatutebook.ie/2010/en/si/0435.html
http://www.irishstatutebook.ie/2010/en/si/0436.html
http://www.irishstatutebook.ie/2010/en/si/0437.html
http://www.irishstatutebook.ie/2010/en/si/0438.html
http://www.irishstatutebook.ie/2010/en/si/0439.html
http://www.irishstatutebook.ie/2010/en/si/0440.html
http://www.irishstatutebook.ie/2010/en/si/0441.html
http://www.irishstatutebook.ie/2010/en/si/0442.html
http://www.irishstatutebook.ie/2010/en/si/0443.html
http://www.irishstatutebook.ie/2010/en/si/0444.html
http://www.irishstatutebook.ie/2010/en/si/0445.html
http://www.irishstatutebook.ie/2010/en/si/0446.html
http://www.irishstatutebook.ie/2010/en/si/0447.html
http://www.irishstatutebook.ie/2010/en/si/0448.html
http://www.irishstatutebook.ie/2010/en/si/0449.html
http://www.irishstatutebook.ie/2010/en/si/0450.html
http://www.irishstatutebook.ie/2010/en/si/0451.html
http://www.irishstatutebook.ie/2010/en/si/0452.html
http://www.irishstatutebook.ie/2010/en/si/0453.html
http://www.irishstatutebook.ie/2010/en/si/0454.html
http://www.irishstatutebook.ie/2010/en/si/0455.html
http://www.irishstatutebook.ie/2010/en/si/0456.html
http://www.irishstatutebook.ie/2010/en/si/0457.html
http://www.irishstatutebook.ie/2010/en/si/0458.html
http://www.irishstatutebook.ie/2010/en/si/0459.html
http://www.irishstatutebook.ie/2010/en/si/0460.html
http://www.irishstatutebook.ie/2010/en/si/0461.html
http://www.irishstatutebook.ie/2010/en/si/0462.html
http://www.irishstatutebook.ie/2010/en/si/0463.html
http://www.irishstatutebook.ie/2010/en/si/0464.html
http://www.irishstatutebook.ie/2010/en/si/0465.html
""".strip()

urls = urls.splitlines()




# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
#    date = re.findall("\” of</i> (.*?)</p>", page, re.DOTALL)  
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None  
    mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)
    dept = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts
       # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
# data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
    scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.irishstatutebook.ie/2010/en/si/0001.html
http://www.irishstatutebook.ie/2010/en/si/0002.html
http://www.irishstatutebook.ie/2010/en/si/0003.html
http://www.irishstatutebook.ie/2010/en/si/0004.html
http://www.irishstatutebook.ie/2010/en/si/0005.html
http://www.irishstatutebook.ie/2010/en/si/0006.html
http://www.irishstatutebook.ie/2010/en/si/0007.html
http://www.irishstatutebook.ie/2010/en/si/0008.html
http://www.irishstatutebook.ie/2010/en/si/0009.html
http://www.irishstatutebook.ie/2010/en/si/0010.html
http://www.irishstatutebook.ie/2010/en/si/0011.html
http://www.irishstatutebook.ie/2010/en/si/0012.html
http://www.irishstatutebook.ie/2010/en/si/0013.html
http://www.irishstatutebook.ie/2010/en/si/0014.html
http://www.irishstatutebook.ie/2010/en/si/0015.html
http://www.irishstatutebook.ie/2010/en/si/0016.html
http://www.irishstatutebook.ie/2010/en/si/0017.html
http://www.irishstatutebook.ie/2010/en/si/0018.html
http://www.irishstatutebook.ie/2010/en/si/0019.html
http://www.irishstatutebook.ie/2010/en/si/0020.html
http://www.irishstatutebook.ie/2010/en/si/0021.html
http://www.irishstatutebook.ie/2010/en/si/0022.html
http://www.irishstatutebook.ie/2010/en/si/0023.html
http://www.irishstatutebook.ie/2010/en/si/0024.html
http://www.irishstatutebook.ie/2010/en/si/0025.html
http://www.irishstatutebook.ie/2010/en/si/0026.html
http://www.irishstatutebook.ie/2010/en/si/0027.html
http://www.irishstatutebook.ie/2010/en/si/0028.html
http://www.irishstatutebook.ie/2010/en/si/0029.html
http://www.irishstatutebook.ie/2010/en/si/0030.html
http://www.irishstatutebook.ie/2010/en/si/0031.html
http://www.irishstatutebook.ie/2010/en/si/0032.html
http://www.irishstatutebook.ie/2010/en/si/0033.html
http://www.irishstatutebook.ie/2010/en/si/0034.html
http://www.irishstatutebook.ie/2010/en/si/0035.html
http://www.irishstatutebook.ie/2010/en/si/0036.html
http://www.irishstatutebook.ie/2010/en/si/0037.html
http://www.irishstatutebook.ie/2010/en/si/0038.html
http://www.irishstatutebook.ie/2010/en/si/0039.html
http://www.irishstatutebook.ie/2010/en/si/0040.html
http://www.irishstatutebook.ie/2010/en/si/0041.html
http://www.irishstatutebook.ie/2010/en/si/0042.html
http://www.irishstatutebook.ie/2010/en/si/0043.html
http://www.irishstatutebook.ie/2010/en/si/0044.html
http://www.irishstatutebook.ie/2010/en/si/0045.html
http://www.irishstatutebook.ie/2010/en/si/0046.html
http://www.irishstatutebook.ie/2010/en/si/0047.html
http://www.irishstatutebook.ie/2010/en/si/0048.html
http://www.irishstatutebook.ie/2010/en/si/0049.html
http://www.irishstatutebook.ie/2010/en/si/0050.html
http://www.irishstatutebook.ie/2010/en/si/0051.html
http://www.irishstatutebook.ie/2010/en/si/0052.html
http://www.irishstatutebook.ie/2010/en/si/0053.html
http://www.irishstatutebook.ie/2010/en/si/0054.html
http://www.irishstatutebook.ie/2010/en/si/0055.html
http://www.irishstatutebook.ie/2010/en/si/0056.html
http://www.irishstatutebook.ie/2010/en/si/0057.html
http://www.irishstatutebook.ie/2010/en/si/0058.html
http://www.irishstatutebook.ie/2010/en/si/0059.html
http://www.irishstatutebook.ie/2010/en/si/0060.html
http://www.irishstatutebook.ie/2010/en/si/0061.html
http://www.irishstatutebook.ie/2010/en/si/0062.html
http://www.irishstatutebook.ie/2010/en/si/0063.html
http://www.irishstatutebook.ie/2010/en/si/0064.html
http://www.irishstatutebook.ie/2010/en/si/0065.html
http://www.irishstatutebook.ie/2010/en/si/0066.html
http://www.irishstatutebook.ie/2010/en/si/0067.html
http://www.irishstatutebook.ie/2010/en/si/0068.html
http://www.irishstatutebook.ie/2010/en/si/0069.html
http://www.irishstatutebook.ie/2010/en/si/0070.html
http://www.irishstatutebook.ie/2010/en/si/0071.html
http://www.irishstatutebook.ie/2010/en/si/0072.html
http://www.irishstatutebook.ie/2010/en/si/0073.html
http://www.irishstatutebook.ie/2010/en/si/0074.html
http://www.irishstatutebook.ie/2010/en/si/0075.html
http://www.irishstatutebook.ie/2010/en/si/0076.html
http://www.irishstatutebook.ie/2010/en/si/0077.html
http://www.irishstatutebook.ie/2010/en/si/0078.html
http://www.irishstatutebook.ie/2010/en/si/0079.html
http://www.irishstatutebook.ie/2010/en/si/0080.html
http://www.irishstatutebook.ie/2010/en/si/0081.html
http://www.irishstatutebook.ie/2010/en/si/0082.html
http://www.irishstatutebook.ie/2010/en/si/0083.html
http://www.irishstatutebook.ie/2010/en/si/0084.html
http://www.irishstatutebook.ie/2010/en/si/0085.html
http://www.irishstatutebook.ie/2010/en/si/0086.html
http://www.irishstatutebook.ie/2010/en/si/0087.html
http://www.irishstatutebook.ie/2010/en/si/0088.html
http://www.irishstatutebook.ie/2010/en/si/0089.html
http://www.irishstatutebook.ie/2010/en/si/0090.html
http://www.irishstatutebook.ie/2010/en/si/0091.html
http://www.irishstatutebook.ie/2010/en/si/0092.html
http://www.irishstatutebook.ie/2010/en/si/0093.html
http://www.irishstatutebook.ie/2010/en/si/0094.html
http://www.irishstatutebook.ie/2010/en/si/0095.html
http://www.irishstatutebook.ie/2010/en/si/0096.html
http://www.irishstatutebook.ie/2010/en/si/0097.html
http://www.irishstatutebook.ie/2010/en/si/0098.html
http://www.irishstatutebook.ie/2010/en/si/0099.html
http://www.irishstatutebook.ie/2010/en/si/0100.html
http://www.irishstatutebook.ie/2010/en/si/0101.html
http://www.irishstatutebook.ie/2010/en/si/0102.html
http://www.irishstatutebook.ie/2010/en/si/0103.html
http://www.irishstatutebook.ie/2010/en/si/0104.html
http://www.irishstatutebook.ie/2010/en/si/0105.html
http://www.irishstatutebook.ie/2010/en/si/0106.html
http://www.irishstatutebook.ie/2010/en/si/0107.html
http://www.irishstatutebook.ie/2010/en/si/0108.html
http://www.irishstatutebook.ie/2010/en/si/0109.html
http://www.irishstatutebook.ie/2010/en/si/0110.html
http://www.irishstatutebook.ie/2010/en/si/0111.html
http://www.irishstatutebook.ie/2010/en/si/0112.html
http://www.irishstatutebook.ie/2010/en/si/0113.html
http://www.irishstatutebook.ie/2010/en/si/0114.html
http://www.irishstatutebook.ie/2010/en/si/0115.html
http://www.irishstatutebook.ie/2010/en/si/0116.html
http://www.irishstatutebook.ie/2010/en/si/0117.html
http://www.irishstatutebook.ie/2010/en/si/0118.html
http://www.irishstatutebook.ie/2010/en/si/0119.html
http://www.irishstatutebook.ie/2010/en/si/0120.html
http://www.irishstatutebook.ie/2010/en/si/0121.html
http://www.irishstatutebook.ie/2010/en/si/0122.html
http://www.irishstatutebook.ie/2010/en/si/0123.html
http://www.irishstatutebook.ie/2010/en/si/0124.html
http://www.irishstatutebook.ie/2010/en/si/0125.html
http://www.irishstatutebook.ie/2010/en/si/0126.html
http://www.irishstatutebook.ie/2010/en/si/0127.html
http://www.irishstatutebook.ie/2010/en/si/0128.html
http://www.irishstatutebook.ie/2010/en/si/0129.html
http://www.irishstatutebook.ie/2010/en/si/0130.html
http://www.irishstatutebook.ie/2010/en/si/0131.html
http://www.irishstatutebook.ie/2010/en/si/0132.html
http://www.irishstatutebook.ie/2010/en/si/0133.html
http://www.irishstatutebook.ie/2010/en/si/0134.html
http://www.irishstatutebook.ie/2010/en/si/0135.html
http://www.irishstatutebook.ie/2010/en/si/0136.html
http://www.irishstatutebook.ie/2010/en/si/0137.html
http://www.irishstatutebook.ie/2010/en/si/0138.html
http://www.irishstatutebook.ie/2010/en/si/0139.html
http://www.irishstatutebook.ie/2010/en/si/0140.html
http://www.irishstatutebook.ie/2010/en/si/0141.html
http://www.irishstatutebook.ie/2010/en/si/0142.html
http://www.irishstatutebook.ie/2010/en/si/0143.html
http://www.irishstatutebook.ie/2010/en/si/0144.html
http://www.irishstatutebook.ie/2010/en/si/0145.html
http://www.irishstatutebook.ie/2010/en/si/0146.html
http://www.irishstatutebook.ie/2010/en/si/0147.html
http://www.irishstatutebook.ie/2010/en/si/0148.html
http://www.irishstatutebook.ie/2010/en/si/0149.html
http://www.irishstatutebook.ie/2010/en/si/0150.html
http://www.irishstatutebook.ie/2010/en/si/0151.html
http://www.irishstatutebook.ie/2010/en/si/0152.html
http://www.irishstatutebook.ie/2010/en/si/0153.html
http://www.irishstatutebook.ie/2010/en/si/0154.html
http://www.irishstatutebook.ie/2010/en/si/0155.html
http://www.irishstatutebook.ie/2010/en/si/0156.html
http://www.irishstatutebook.ie/2010/en/si/0157.html
http://www.irishstatutebook.ie/2010/en/si/0158.html
http://www.irishstatutebook.ie/2010/en/si/0159.html
http://www.irishstatutebook.ie/2010/en/si/0160.html
http://www.irishstatutebook.ie/2010/en/si/0161.html
http://www.irishstatutebook.ie/2010/en/si/0162.html
http://www.irishstatutebook.ie/2010/en/si/0163.html
http://www.irishstatutebook.ie/2010/en/si/0164.html
http://www.irishstatutebook.ie/2010/en/si/0165.html
http://www.irishstatutebook.ie/2010/en/si/0166.html
http://www.irishstatutebook.ie/2010/en/si/0167.html
http://www.irishstatutebook.ie/2010/en/si/0168.html
http://www.irishstatutebook.ie/2010/en/si/0169.html
http://www.irishstatutebook.ie/2010/en/si/0170.html
http://www.irishstatutebook.ie/2010/en/si/0171.html
http://www.irishstatutebook.ie/2010/en/si/0172.html
http://www.irishstatutebook.ie/2010/en/si/0173.html
http://www.irishstatutebook.ie/2010/en/si/0174.html
http://www.irishstatutebook.ie/2010/en/si/0175.html
http://www.irishstatutebook.ie/2010/en/si/0176.html
http://www.irishstatutebook.ie/2010/en/si/0177.html
http://www.irishstatutebook.ie/2010/en/si/0178.html
http://www.irishstatutebook.ie/2010/en/si/0179.html
http://www.irishstatutebook.ie/2010/en/si/0180.html
http://www.irishstatutebook.ie/2010/en/si/0181.html
http://www.irishstatutebook.ie/2010/en/si/0182.html
http://www.irishstatutebook.ie/2010/en/si/0183.html
http://www.irishstatutebook.ie/2010/en/si/0184.html
http://www.irishstatutebook.ie/2010/en/si/0185.html
http://www.irishstatutebook.ie/2010/en/si/0186.html
http://www.irishstatutebook.ie/2010/en/si/0187.html
http://www.irishstatutebook.ie/2010/en/si/0188.html
http://www.irishstatutebook.ie/2010/en/si/0189.html
http://www.irishstatutebook.ie/2010/en/si/0190.html
http://www.irishstatutebook.ie/2010/en/si/0191.html
http://www.irishstatutebook.ie/2010/en/si/0192.html
http://www.irishstatutebook.ie/2010/en/si/0193.html
http://www.irishstatutebook.ie/2010/en/si/0194.html
http://www.irishstatutebook.ie/2010/en/si/0195.html
http://www.irishstatutebook.ie/2010/en/si/0196.html
http://www.irishstatutebook.ie/2010/en/si/0197.html
http://www.irishstatutebook.ie/2010/en/si/0198.html
http://www.irishstatutebook.ie/2010/en/si/0199.html
http://www.irishstatutebook.ie/2010/en/si/0200.html
http://www.irishstatutebook.ie/2010/en/si/0201.html
http://www.irishstatutebook.ie/2010/en/si/0202.html
http://www.irishstatutebook.ie/2010/en/si/0203.html
http://www.irishstatutebook.ie/2010/en/si/0204.html
http://www.irishstatutebook.ie/2010/en/si/0205.html
http://www.irishstatutebook.ie/2010/en/si/0206.html
http://www.irishstatutebook.ie/2010/en/si/0207.html
http://www.irishstatutebook.ie/2010/en/si/0208.html
http://www.irishstatutebook.ie/2010/en/si/0209.html
http://www.irishstatutebook.ie/2010/en/si/0210.html
http://www.irishstatutebook.ie/2010/en/si/0211.html
http://www.irishstatutebook.ie/2010/en/si/0212.html
http://www.irishstatutebook.ie/2010/en/si/0213.html
http://www.irishstatutebook.ie/2010/en/si/0214.html
http://www.irishstatutebook.ie/2010/en/si/0215.html
http://www.irishstatutebook.ie/2010/en/si/0216.html
http://www.irishstatutebook.ie/2010/en/si/0217.html
http://www.irishstatutebook.ie/2010/en/si/0218.html
http://www.irishstatutebook.ie/2010/en/si/0219.html
http://www.irishstatutebook.ie/2010/en/si/0220.html
http://www.irishstatutebook.ie/2010/en/si/0221.html
http://www.irishstatutebook.ie/2010/en/si/0222.html
http://www.irishstatutebook.ie/2010/en/si/0223.html
http://www.irishstatutebook.ie/2010/en/si/0224.html
http://www.irishstatutebook.ie/2010/en/si/0225.html
http://www.irishstatutebook.ie/2010/en/si/0226.html
http://www.irishstatutebook.ie/2010/en/si/0227.html
http://www.irishstatutebook.ie/2010/en/si/0228.html
http://www.irishstatutebook.ie/2010/en/si/0229.html
http://www.irishstatutebook.ie/2010/en/si/0230.html
http://www.irishstatutebook.ie/2010/en/si/0231.html
http://www.irishstatutebook.ie/2010/en/si/0232.html
http://www.irishstatutebook.ie/2010/en/si/0233.html
http://www.irishstatutebook.ie/2010/en/si/0234.html
http://www.irishstatutebook.ie/2010/en/si/0235.html
http://www.irishstatutebook.ie/2010/en/si/0236.html
http://www.irishstatutebook.ie/2010/en/si/0237.html
http://www.irishstatutebook.ie/2010/en/si/0238.html
http://www.irishstatutebook.ie/2010/en/si/0239.html
http://www.irishstatutebook.ie/2010/en/si/0240.html
http://www.irishstatutebook.ie/2010/en/si/0241.html
http://www.irishstatutebook.ie/2010/en/si/0242.html
http://www.irishstatutebook.ie/2010/en/si/0243.html
http://www.irishstatutebook.ie/2010/en/si/0244.html
http://www.irishstatutebook.ie/2010/en/si/0245.html
http://www.irishstatutebook.ie/2010/en/si/0246.html
http://www.irishstatutebook.ie/2010/en/si/0247.html
http://www.irishstatutebook.ie/2010/en/si/0248.html
http://www.irishstatutebook.ie/2010/en/si/0249.html
http://www.irishstatutebook.ie/2010/en/si/0250.html
http://www.irishstatutebook.ie/2010/en/si/0251.html
http://www.irishstatutebook.ie/2010/en/si/0252.html
http://www.irishstatutebook.ie/2010/en/si/0253.html
http://www.irishstatutebook.ie/2010/en/si/0254.html
http://www.irishstatutebook.ie/2010/en/si/0255.html
http://www.irishstatutebook.ie/2010/en/si/0256.html
http://www.irishstatutebook.ie/2010/en/si/0257.html
http://www.irishstatutebook.ie/2010/en/si/0258.html
http://www.irishstatutebook.ie/2010/en/si/0259.html
http://www.irishstatutebook.ie/2010/en/si/0260.html
http://www.irishstatutebook.ie/2010/en/si/0261.html
http://www.irishstatutebook.ie/2010/en/si/0262.html
http://www.irishstatutebook.ie/2010/en/si/0263.html
http://www.irishstatutebook.ie/2010/en/si/0264.html
http://www.irishstatutebook.ie/2010/en/si/0265.html
http://www.irishstatutebook.ie/2010/en/si/0266.html
http://www.irishstatutebook.ie/2010/en/si/0267.html
http://www.irishstatutebook.ie/2010/en/si/0268.html
http://www.irishstatutebook.ie/2010/en/si/0269.html
http://www.irishstatutebook.ie/2010/en/si/0270.html
http://www.irishstatutebook.ie/2010/en/si/0271.html
http://www.irishstatutebook.ie/2010/en/si/0272.html
http://www.irishstatutebook.ie/2010/en/si/0273.html
http://www.irishstatutebook.ie/2010/en/si/0274.html
http://www.irishstatutebook.ie/2010/en/si/0275.html
http://www.irishstatutebook.ie/2010/en/si/0276.html
http://www.irishstatutebook.ie/2010/en/si/0277.html
http://www.irishstatutebook.ie/2010/en/si/0278.html
http://www.irishstatutebook.ie/2010/en/si/0279.html
http://www.irishstatutebook.ie/2010/en/si/0280.html
http://www.irishstatutebook.ie/2010/en/si/0281.html
http://www.irishstatutebook.ie/2010/en/si/0282.html
http://www.irishstatutebook.ie/2010/en/si/0283.html
http://www.irishstatutebook.ie/2010/en/si/0284.html
http://www.irishstatutebook.ie/2010/en/si/0285.html
http://www.irishstatutebook.ie/2010/en/si/0286.html
http://www.irishstatutebook.ie/2010/en/si/0287.html
http://www.irishstatutebook.ie/2010/en/si/0288.html
http://www.irishstatutebook.ie/2010/en/si/0289.html
http://www.irishstatutebook.ie/2010/en/si/0290.html
http://www.irishstatutebook.ie/2010/en/si/0291.html
http://www.irishstatutebook.ie/2010/en/si/0292.html
http://www.irishstatutebook.ie/2010/en/si/0293.html
http://www.irishstatutebook.ie/2010/en/si/0294.html
http://www.irishstatutebook.ie/2010/en/si/0295.html
http://www.irishstatutebook.ie/2010/en/si/0296.html
http://www.irishstatutebook.ie/2010/en/si/0297.html
http://www.irishstatutebook.ie/2010/en/si/0298.html
http://www.irishstatutebook.ie/2010/en/si/0299.html
http://www.irishstatutebook.ie/2010/en/si/0300.html
http://www.irishstatutebook.ie/2010/en/si/0301.html
http://www.irishstatutebook.ie/2010/en/si/0302.html
http://www.irishstatutebook.ie/2010/en/si/0303.html
http://www.irishstatutebook.ie/2010/en/si/0304.html
http://www.irishstatutebook.ie/2010/en/si/0305.html
http://www.irishstatutebook.ie/2010/en/si/0306.html
http://www.irishstatutebook.ie/2010/en/si/0307.html
http://www.irishstatutebook.ie/2010/en/si/0308.html
http://www.irishstatutebook.ie/2010/en/si/0309.html
http://www.irishstatutebook.ie/2010/en/si/0310.html
http://www.irishstatutebook.ie/2010/en/si/0311.html
http://www.irishstatutebook.ie/2010/en/si/0312.html
http://www.irishstatutebook.ie/2010/en/si/0313.html
http://www.irishstatutebook.ie/2010/en/si/0314.html
http://www.irishstatutebook.ie/2010/en/si/0315.html
http://www.irishstatutebook.ie/2010/en/si/0316.html
http://www.irishstatutebook.ie/2010/en/si/0317.html
http://www.irishstatutebook.ie/2010/en/si/0318.html
http://www.irishstatutebook.ie/2010/en/si/0319.html
http://www.irishstatutebook.ie/2010/en/si/0320.html
http://www.irishstatutebook.ie/2010/en/si/0321.html
http://www.irishstatutebook.ie/2010/en/si/0322.html
http://www.irishstatutebook.ie/2010/en/si/0323.html
http://www.irishstatutebook.ie/2010/en/si/0324.html
http://www.irishstatutebook.ie/2010/en/si/0325.html
http://www.irishstatutebook.ie/2010/en/si/0326.html
http://www.irishstatutebook.ie/2010/en/si/0327.html
http://www.irishstatutebook.ie/2010/en/si/0328.html
http://www.irishstatutebook.ie/2010/en/si/0329.html
http://www.irishstatutebook.ie/2010/en/si/0330.html
http://www.irishstatutebook.ie/2010/en/si/0331.html
http://www.irishstatutebook.ie/2010/en/si/0332.html
http://www.irishstatutebook.ie/2010/en/si/0333.html
http://www.irishstatutebook.ie/2010/en/si/0334.html
http://www.irishstatutebook.ie/2010/en/si/0335.html
http://www.irishstatutebook.ie/2010/en/si/0336.html
http://www.irishstatutebook.ie/2010/en/si/0337.html
http://www.irishstatutebook.ie/2010/en/si/0338.html
http://www.irishstatutebook.ie/2010/en/si/0339.html
http://www.irishstatutebook.ie/2010/en/si/0340.html
http://www.irishstatutebook.ie/2010/en/si/0341.html
http://www.irishstatutebook.ie/2010/en/si/0342.html
http://www.irishstatutebook.ie/2010/en/si/0343.html
http://www.irishstatutebook.ie/2010/en/si/0344.html
http://www.irishstatutebook.ie/2010/en/si/0345.html
http://www.irishstatutebook.ie/2010/en/si/0346.html
http://www.irishstatutebook.ie/2010/en/si/0347.html
http://www.irishstatutebook.ie/2010/en/si/0348.html
http://www.irishstatutebook.ie/2010/en/si/0349.html
http://www.irishstatutebook.ie/2010/en/si/0350.html
http://www.irishstatutebook.ie/2010/en/si/0351.html
http://www.irishstatutebook.ie/2010/en/si/0352.html
http://www.irishstatutebook.ie/2010/en/si/0353.html
http://www.irishstatutebook.ie/2010/en/si/0354.html
http://www.irishstatutebook.ie/2010/en/si/0355.html
http://www.irishstatutebook.ie/2010/en/si/0356.html
http://www.irishstatutebook.ie/2010/en/si/0357.html
http://www.irishstatutebook.ie/2010/en/si/0358.html
http://www.irishstatutebook.ie/2010/en/si/0359.html
http://www.irishstatutebook.ie/2010/en/si/0360.html
http://www.irishstatutebook.ie/2010/en/si/0361.html
http://www.irishstatutebook.ie/2010/en/si/0362.html
http://www.irishstatutebook.ie/2010/en/si/0363.html
http://www.irishstatutebook.ie/2010/en/si/0364.html
http://www.irishstatutebook.ie/2010/en/si/0365.html
http://www.irishstatutebook.ie/2010/en/si/0366.html
http://www.irishstatutebook.ie/2010/en/si/0367.html
http://www.irishstatutebook.ie/2010/en/si/0368.html
http://www.irishstatutebook.ie/2010/en/si/0369.html
http://www.irishstatutebook.ie/2010/en/si/0370.html
http://www.irishstatutebook.ie/2010/en/si/0371.html
http://www.irishstatutebook.ie/2010/en/si/0372.html
http://www.irishstatutebook.ie/2010/en/si/0373.html
http://www.irishstatutebook.ie/2010/en/si/0374.html
http://www.irishstatutebook.ie/2010/en/si/0375.html
http://www.irishstatutebook.ie/2010/en/si/0376.html
http://www.irishstatutebook.ie/2010/en/si/0377.html
http://www.irishstatutebook.ie/2010/en/si/0378.html
http://www.irishstatutebook.ie/2010/en/si/0379.html
http://www.irishstatutebook.ie/2010/en/si/0380.html
http://www.irishstatutebook.ie/2010/en/si/0381.html
http://www.irishstatutebook.ie/2010/en/si/0382.html
http://www.irishstatutebook.ie/2010/en/si/0383.html
http://www.irishstatutebook.ie/2010/en/si/0384.html
http://www.irishstatutebook.ie/2010/en/si/0385.html
http://www.irishstatutebook.ie/2010/en/si/0386.html
http://www.irishstatutebook.ie/2010/en/si/0387.html
http://www.irishstatutebook.ie/2010/en/si/0388.html
http://www.irishstatutebook.ie/2010/en/si/0389.html
http://www.irishstatutebook.ie/2010/en/si/0390.html
http://www.irishstatutebook.ie/2010/en/si/0391.html
http://www.irishstatutebook.ie/2010/en/si/0392.html
http://www.irishstatutebook.ie/2010/en/si/0393.html
http://www.irishstatutebook.ie/2010/en/si/0394.html
http://www.irishstatutebook.ie/2010/en/si/0395.html
http://www.irishstatutebook.ie/2010/en/si/0396.html
http://www.irishstatutebook.ie/2010/en/si/0397.html
http://www.irishstatutebook.ie/2010/en/si/0398.html
http://www.irishstatutebook.ie/2010/en/si/0399.html
http://www.irishstatutebook.ie/2010/en/si/0400.html
http://www.irishstatutebook.ie/2010/en/si/0401.html
http://www.irishstatutebook.ie/2010/en/si/0402.html
http://www.irishstatutebook.ie/2010/en/si/0403.html
http://www.irishstatutebook.ie/2010/en/si/0404.html
http://www.irishstatutebook.ie/2010/en/si/0405.html
http://www.irishstatutebook.ie/2010/en/si/0406.html
http://www.irishstatutebook.ie/2010/en/si/0407.html
http://www.irishstatutebook.ie/2010/en/si/0408.html
http://www.irishstatutebook.ie/2010/en/si/0409.html
http://www.irishstatutebook.ie/2010/en/si/0410.html
http://www.irishstatutebook.ie/2010/en/si/0411.html
http://www.irishstatutebook.ie/2010/en/si/0412.html
http://www.irishstatutebook.ie/2010/en/si/0413.html
http://www.irishstatutebook.ie/2010/en/si/0414.html
http://www.irishstatutebook.ie/2010/en/si/0415.html
http://www.irishstatutebook.ie/2010/en/si/0416.html
http://www.irishstatutebook.ie/2010/en/si/0417.html
http://www.irishstatutebook.ie/2010/en/si/0418.html
http://www.irishstatutebook.ie/2010/en/si/0419.html
http://www.irishstatutebook.ie/2010/en/si/0420.html
http://www.irishstatutebook.ie/2010/en/si/0421.html
http://www.irishstatutebook.ie/2010/en/si/0422.html
http://www.irishstatutebook.ie/2010/en/si/0423.html
http://www.irishstatutebook.ie/2010/en/si/0424.html
http://www.irishstatutebook.ie/2010/en/si/0425.html
http://www.irishstatutebook.ie/2010/en/si/0426.html
http://www.irishstatutebook.ie/2010/en/si/0427.html
http://www.irishstatutebook.ie/2010/en/si/0428.html
http://www.irishstatutebook.ie/2010/en/si/0429.html
http://www.irishstatutebook.ie/2010/en/si/0430.html
http://www.irishstatutebook.ie/2010/en/si/0431.html
http://www.irishstatutebook.ie/2010/en/si/0432.html
http://www.irishstatutebook.ie/2010/en/si/0433.html
http://www.irishstatutebook.ie/2010/en/si/0434.html
http://www.irishstatutebook.ie/2010/en/si/0435.html
http://www.irishstatutebook.ie/2010/en/si/0436.html
http://www.irishstatutebook.ie/2010/en/si/0437.html
http://www.irishstatutebook.ie/2010/en/si/0438.html
http://www.irishstatutebook.ie/2010/en/si/0439.html
http://www.irishstatutebook.ie/2010/en/si/0440.html
http://www.irishstatutebook.ie/2010/en/si/0441.html
http://www.irishstatutebook.ie/2010/en/si/0442.html
http://www.irishstatutebook.ie/2010/en/si/0443.html
http://www.irishstatutebook.ie/2010/en/si/0444.html
http://www.irishstatutebook.ie/2010/en/si/0445.html
http://www.irishstatutebook.ie/2010/en/si/0446.html
http://www.irishstatutebook.ie/2010/en/si/0447.html
http://www.irishstatutebook.ie/2010/en/si/0448.html
http://www.irishstatutebook.ie/2010/en/si/0449.html
http://www.irishstatutebook.ie/2010/en/si/0450.html
http://www.irishstatutebook.ie/2010/en/si/0451.html
http://www.irishstatutebook.ie/2010/en/si/0452.html
http://www.irishstatutebook.ie/2010/en/si/0453.html
http://www.irishstatutebook.ie/2010/en/si/0454.html
http://www.irishstatutebook.ie/2010/en/si/0455.html
http://www.irishstatutebook.ie/2010/en/si/0456.html
http://www.irishstatutebook.ie/2010/en/si/0457.html
http://www.irishstatutebook.ie/2010/en/si/0458.html
http://www.irishstatutebook.ie/2010/en/si/0459.html
http://www.irishstatutebook.ie/2010/en/si/0460.html
http://www.irishstatutebook.ie/2010/en/si/0461.html
http://www.irishstatutebook.ie/2010/en/si/0462.html
http://www.irishstatutebook.ie/2010/en/si/0463.html
http://www.irishstatutebook.ie/2010/en/si/0464.html
http://www.irishstatutebook.ie/2010/en/si/0465.html
""".strip()

urls = urls.splitlines()




# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
#    date = re.findall("\” of</i> (.*?)</p>", page, re.DOTALL)  
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None  
    mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)
    dept = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts
       # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
# data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
    scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.irishstatutebook.ie/2010/en/si/0001.html
http://www.irishstatutebook.ie/2010/en/si/0002.html
http://www.irishstatutebook.ie/2010/en/si/0003.html
http://www.irishstatutebook.ie/2010/en/si/0004.html
http://www.irishstatutebook.ie/2010/en/si/0005.html
http://www.irishstatutebook.ie/2010/en/si/0006.html
http://www.irishstatutebook.ie/2010/en/si/0007.html
http://www.irishstatutebook.ie/2010/en/si/0008.html
http://www.irishstatutebook.ie/2010/en/si/0009.html
http://www.irishstatutebook.ie/2010/en/si/0010.html
http://www.irishstatutebook.ie/2010/en/si/0011.html
http://www.irishstatutebook.ie/2010/en/si/0012.html
http://www.irishstatutebook.ie/2010/en/si/0013.html
http://www.irishstatutebook.ie/2010/en/si/0014.html
http://www.irishstatutebook.ie/2010/en/si/0015.html
http://www.irishstatutebook.ie/2010/en/si/0016.html
http://www.irishstatutebook.ie/2010/en/si/0017.html
http://www.irishstatutebook.ie/2010/en/si/0018.html
http://www.irishstatutebook.ie/2010/en/si/0019.html
http://www.irishstatutebook.ie/2010/en/si/0020.html
http://www.irishstatutebook.ie/2010/en/si/0021.html
http://www.irishstatutebook.ie/2010/en/si/0022.html
http://www.irishstatutebook.ie/2010/en/si/0023.html
http://www.irishstatutebook.ie/2010/en/si/0024.html
http://www.irishstatutebook.ie/2010/en/si/0025.html
http://www.irishstatutebook.ie/2010/en/si/0026.html
http://www.irishstatutebook.ie/2010/en/si/0027.html
http://www.irishstatutebook.ie/2010/en/si/0028.html
http://www.irishstatutebook.ie/2010/en/si/0029.html
http://www.irishstatutebook.ie/2010/en/si/0030.html
http://www.irishstatutebook.ie/2010/en/si/0031.html
http://www.irishstatutebook.ie/2010/en/si/0032.html
http://www.irishstatutebook.ie/2010/en/si/0033.html
http://www.irishstatutebook.ie/2010/en/si/0034.html
http://www.irishstatutebook.ie/2010/en/si/0035.html
http://www.irishstatutebook.ie/2010/en/si/0036.html
http://www.irishstatutebook.ie/2010/en/si/0037.html
http://www.irishstatutebook.ie/2010/en/si/0038.html
http://www.irishstatutebook.ie/2010/en/si/0039.html
http://www.irishstatutebook.ie/2010/en/si/0040.html
http://www.irishstatutebook.ie/2010/en/si/0041.html
http://www.irishstatutebook.ie/2010/en/si/0042.html
http://www.irishstatutebook.ie/2010/en/si/0043.html
http://www.irishstatutebook.ie/2010/en/si/0044.html
http://www.irishstatutebook.ie/2010/en/si/0045.html
http://www.irishstatutebook.ie/2010/en/si/0046.html
http://www.irishstatutebook.ie/2010/en/si/0047.html
http://www.irishstatutebook.ie/2010/en/si/0048.html
http://www.irishstatutebook.ie/2010/en/si/0049.html
http://www.irishstatutebook.ie/2010/en/si/0050.html
http://www.irishstatutebook.ie/2010/en/si/0051.html
http://www.irishstatutebook.ie/2010/en/si/0052.html
http://www.irishstatutebook.ie/2010/en/si/0053.html
http://www.irishstatutebook.ie/2010/en/si/0054.html
http://www.irishstatutebook.ie/2010/en/si/0055.html
http://www.irishstatutebook.ie/2010/en/si/0056.html
http://www.irishstatutebook.ie/2010/en/si/0057.html
http://www.irishstatutebook.ie/2010/en/si/0058.html
http://www.irishstatutebook.ie/2010/en/si/0059.html
http://www.irishstatutebook.ie/2010/en/si/0060.html
http://www.irishstatutebook.ie/2010/en/si/0061.html
http://www.irishstatutebook.ie/2010/en/si/0062.html
http://www.irishstatutebook.ie/2010/en/si/0063.html
http://www.irishstatutebook.ie/2010/en/si/0064.html
http://www.irishstatutebook.ie/2010/en/si/0065.html
http://www.irishstatutebook.ie/2010/en/si/0066.html
http://www.irishstatutebook.ie/2010/en/si/0067.html
http://www.irishstatutebook.ie/2010/en/si/0068.html
http://www.irishstatutebook.ie/2010/en/si/0069.html
http://www.irishstatutebook.ie/2010/en/si/0070.html
http://www.irishstatutebook.ie/2010/en/si/0071.html
http://www.irishstatutebook.ie/2010/en/si/0072.html
http://www.irishstatutebook.ie/2010/en/si/0073.html
http://www.irishstatutebook.ie/2010/en/si/0074.html
http://www.irishstatutebook.ie/2010/en/si/0075.html
http://www.irishstatutebook.ie/2010/en/si/0076.html
http://www.irishstatutebook.ie/2010/en/si/0077.html
http://www.irishstatutebook.ie/2010/en/si/0078.html
http://www.irishstatutebook.ie/2010/en/si/0079.html
http://www.irishstatutebook.ie/2010/en/si/0080.html
http://www.irishstatutebook.ie/2010/en/si/0081.html
http://www.irishstatutebook.ie/2010/en/si/0082.html
http://www.irishstatutebook.ie/2010/en/si/0083.html
http://www.irishstatutebook.ie/2010/en/si/0084.html
http://www.irishstatutebook.ie/2010/en/si/0085.html
http://www.irishstatutebook.ie/2010/en/si/0086.html
http://www.irishstatutebook.ie/2010/en/si/0087.html
http://www.irishstatutebook.ie/2010/en/si/0088.html
http://www.irishstatutebook.ie/2010/en/si/0089.html
http://www.irishstatutebook.ie/2010/en/si/0090.html
http://www.irishstatutebook.ie/2010/en/si/0091.html
http://www.irishstatutebook.ie/2010/en/si/0092.html
http://www.irishstatutebook.ie/2010/en/si/0093.html
http://www.irishstatutebook.ie/2010/en/si/0094.html
http://www.irishstatutebook.ie/2010/en/si/0095.html
http://www.irishstatutebook.ie/2010/en/si/0096.html
http://www.irishstatutebook.ie/2010/en/si/0097.html
http://www.irishstatutebook.ie/2010/en/si/0098.html
http://www.irishstatutebook.ie/2010/en/si/0099.html
http://www.irishstatutebook.ie/2010/en/si/0100.html
http://www.irishstatutebook.ie/2010/en/si/0101.html
http://www.irishstatutebook.ie/2010/en/si/0102.html
http://www.irishstatutebook.ie/2010/en/si/0103.html
http://www.irishstatutebook.ie/2010/en/si/0104.html
http://www.irishstatutebook.ie/2010/en/si/0105.html
http://www.irishstatutebook.ie/2010/en/si/0106.html
http://www.irishstatutebook.ie/2010/en/si/0107.html
http://www.irishstatutebook.ie/2010/en/si/0108.html
http://www.irishstatutebook.ie/2010/en/si/0109.html
http://www.irishstatutebook.ie/2010/en/si/0110.html
http://www.irishstatutebook.ie/2010/en/si/0111.html
http://www.irishstatutebook.ie/2010/en/si/0112.html
http://www.irishstatutebook.ie/2010/en/si/0113.html
http://www.irishstatutebook.ie/2010/en/si/0114.html
http://www.irishstatutebook.ie/2010/en/si/0115.html
http://www.irishstatutebook.ie/2010/en/si/0116.html
http://www.irishstatutebook.ie/2010/en/si/0117.html
http://www.irishstatutebook.ie/2010/en/si/0118.html
http://www.irishstatutebook.ie/2010/en/si/0119.html
http://www.irishstatutebook.ie/2010/en/si/0120.html
http://www.irishstatutebook.ie/2010/en/si/0121.html
http://www.irishstatutebook.ie/2010/en/si/0122.html
http://www.irishstatutebook.ie/2010/en/si/0123.html
http://www.irishstatutebook.ie/2010/en/si/0124.html
http://www.irishstatutebook.ie/2010/en/si/0125.html
http://www.irishstatutebook.ie/2010/en/si/0126.html
http://www.irishstatutebook.ie/2010/en/si/0127.html
http://www.irishstatutebook.ie/2010/en/si/0128.html
http://www.irishstatutebook.ie/2010/en/si/0129.html
http://www.irishstatutebook.ie/2010/en/si/0130.html
http://www.irishstatutebook.ie/2010/en/si/0131.html
http://www.irishstatutebook.ie/2010/en/si/0132.html
http://www.irishstatutebook.ie/2010/en/si/0133.html
http://www.irishstatutebook.ie/2010/en/si/0134.html
http://www.irishstatutebook.ie/2010/en/si/0135.html
http://www.irishstatutebook.ie/2010/en/si/0136.html
http://www.irishstatutebook.ie/2010/en/si/0137.html
http://www.irishstatutebook.ie/2010/en/si/0138.html
http://www.irishstatutebook.ie/2010/en/si/0139.html
http://www.irishstatutebook.ie/2010/en/si/0140.html
http://www.irishstatutebook.ie/2010/en/si/0141.html
http://www.irishstatutebook.ie/2010/en/si/0142.html
http://www.irishstatutebook.ie/2010/en/si/0143.html
http://www.irishstatutebook.ie/2010/en/si/0144.html
http://www.irishstatutebook.ie/2010/en/si/0145.html
http://www.irishstatutebook.ie/2010/en/si/0146.html
http://www.irishstatutebook.ie/2010/en/si/0147.html
http://www.irishstatutebook.ie/2010/en/si/0148.html
http://www.irishstatutebook.ie/2010/en/si/0149.html
http://www.irishstatutebook.ie/2010/en/si/0150.html
http://www.irishstatutebook.ie/2010/en/si/0151.html
http://www.irishstatutebook.ie/2010/en/si/0152.html
http://www.irishstatutebook.ie/2010/en/si/0153.html
http://www.irishstatutebook.ie/2010/en/si/0154.html
http://www.irishstatutebook.ie/2010/en/si/0155.html
http://www.irishstatutebook.ie/2010/en/si/0156.html
http://www.irishstatutebook.ie/2010/en/si/0157.html
http://www.irishstatutebook.ie/2010/en/si/0158.html
http://www.irishstatutebook.ie/2010/en/si/0159.html
http://www.irishstatutebook.ie/2010/en/si/0160.html
http://www.irishstatutebook.ie/2010/en/si/0161.html
http://www.irishstatutebook.ie/2010/en/si/0162.html
http://www.irishstatutebook.ie/2010/en/si/0163.html
http://www.irishstatutebook.ie/2010/en/si/0164.html
http://www.irishstatutebook.ie/2010/en/si/0165.html
http://www.irishstatutebook.ie/2010/en/si/0166.html
http://www.irishstatutebook.ie/2010/en/si/0167.html
http://www.irishstatutebook.ie/2010/en/si/0168.html
http://www.irishstatutebook.ie/2010/en/si/0169.html
http://www.irishstatutebook.ie/2010/en/si/0170.html
http://www.irishstatutebook.ie/2010/en/si/0171.html
http://www.irishstatutebook.ie/2010/en/si/0172.html
http://www.irishstatutebook.ie/2010/en/si/0173.html
http://www.irishstatutebook.ie/2010/en/si/0174.html
http://www.irishstatutebook.ie/2010/en/si/0175.html
http://www.irishstatutebook.ie/2010/en/si/0176.html
http://www.irishstatutebook.ie/2010/en/si/0177.html
http://www.irishstatutebook.ie/2010/en/si/0178.html
http://www.irishstatutebook.ie/2010/en/si/0179.html
http://www.irishstatutebook.ie/2010/en/si/0180.html
http://www.irishstatutebook.ie/2010/en/si/0181.html
http://www.irishstatutebook.ie/2010/en/si/0182.html
http://www.irishstatutebook.ie/2010/en/si/0183.html
http://www.irishstatutebook.ie/2010/en/si/0184.html
http://www.irishstatutebook.ie/2010/en/si/0185.html
http://www.irishstatutebook.ie/2010/en/si/0186.html
http://www.irishstatutebook.ie/2010/en/si/0187.html
http://www.irishstatutebook.ie/2010/en/si/0188.html
http://www.irishstatutebook.ie/2010/en/si/0189.html
http://www.irishstatutebook.ie/2010/en/si/0190.html
http://www.irishstatutebook.ie/2010/en/si/0191.html
http://www.irishstatutebook.ie/2010/en/si/0192.html
http://www.irishstatutebook.ie/2010/en/si/0193.html
http://www.irishstatutebook.ie/2010/en/si/0194.html
http://www.irishstatutebook.ie/2010/en/si/0195.html
http://www.irishstatutebook.ie/2010/en/si/0196.html
http://www.irishstatutebook.ie/2010/en/si/0197.html
http://www.irishstatutebook.ie/2010/en/si/0198.html
http://www.irishstatutebook.ie/2010/en/si/0199.html
http://www.irishstatutebook.ie/2010/en/si/0200.html
http://www.irishstatutebook.ie/2010/en/si/0201.html
http://www.irishstatutebook.ie/2010/en/si/0202.html
http://www.irishstatutebook.ie/2010/en/si/0203.html
http://www.irishstatutebook.ie/2010/en/si/0204.html
http://www.irishstatutebook.ie/2010/en/si/0205.html
http://www.irishstatutebook.ie/2010/en/si/0206.html
http://www.irishstatutebook.ie/2010/en/si/0207.html
http://www.irishstatutebook.ie/2010/en/si/0208.html
http://www.irishstatutebook.ie/2010/en/si/0209.html
http://www.irishstatutebook.ie/2010/en/si/0210.html
http://www.irishstatutebook.ie/2010/en/si/0211.html
http://www.irishstatutebook.ie/2010/en/si/0212.html
http://www.irishstatutebook.ie/2010/en/si/0213.html
http://www.irishstatutebook.ie/2010/en/si/0214.html
http://www.irishstatutebook.ie/2010/en/si/0215.html
http://www.irishstatutebook.ie/2010/en/si/0216.html
http://www.irishstatutebook.ie/2010/en/si/0217.html
http://www.irishstatutebook.ie/2010/en/si/0218.html
http://www.irishstatutebook.ie/2010/en/si/0219.html
http://www.irishstatutebook.ie/2010/en/si/0220.html
http://www.irishstatutebook.ie/2010/en/si/0221.html
http://www.irishstatutebook.ie/2010/en/si/0222.html
http://www.irishstatutebook.ie/2010/en/si/0223.html
http://www.irishstatutebook.ie/2010/en/si/0224.html
http://www.irishstatutebook.ie/2010/en/si/0225.html
http://www.irishstatutebook.ie/2010/en/si/0226.html
http://www.irishstatutebook.ie/2010/en/si/0227.html
http://www.irishstatutebook.ie/2010/en/si/0228.html
http://www.irishstatutebook.ie/2010/en/si/0229.html
http://www.irishstatutebook.ie/2010/en/si/0230.html
http://www.irishstatutebook.ie/2010/en/si/0231.html
http://www.irishstatutebook.ie/2010/en/si/0232.html
http://www.irishstatutebook.ie/2010/en/si/0233.html
http://www.irishstatutebook.ie/2010/en/si/0234.html
http://www.irishstatutebook.ie/2010/en/si/0235.html
http://www.irishstatutebook.ie/2010/en/si/0236.html
http://www.irishstatutebook.ie/2010/en/si/0237.html
http://www.irishstatutebook.ie/2010/en/si/0238.html
http://www.irishstatutebook.ie/2010/en/si/0239.html
http://www.irishstatutebook.ie/2010/en/si/0240.html
http://www.irishstatutebook.ie/2010/en/si/0241.html
http://www.irishstatutebook.ie/2010/en/si/0242.html
http://www.irishstatutebook.ie/2010/en/si/0243.html
http://www.irishstatutebook.ie/2010/en/si/0244.html
http://www.irishstatutebook.ie/2010/en/si/0245.html
http://www.irishstatutebook.ie/2010/en/si/0246.html
http://www.irishstatutebook.ie/2010/en/si/0247.html
http://www.irishstatutebook.ie/2010/en/si/0248.html
http://www.irishstatutebook.ie/2010/en/si/0249.html
http://www.irishstatutebook.ie/2010/en/si/0250.html
http://www.irishstatutebook.ie/2010/en/si/0251.html
http://www.irishstatutebook.ie/2010/en/si/0252.html
http://www.irishstatutebook.ie/2010/en/si/0253.html
http://www.irishstatutebook.ie/2010/en/si/0254.html
http://www.irishstatutebook.ie/2010/en/si/0255.html
http://www.irishstatutebook.ie/2010/en/si/0256.html
http://www.irishstatutebook.ie/2010/en/si/0257.html
http://www.irishstatutebook.ie/2010/en/si/0258.html
http://www.irishstatutebook.ie/2010/en/si/0259.html
http://www.irishstatutebook.ie/2010/en/si/0260.html
http://www.irishstatutebook.ie/2010/en/si/0261.html
http://www.irishstatutebook.ie/2010/en/si/0262.html
http://www.irishstatutebook.ie/2010/en/si/0263.html
http://www.irishstatutebook.ie/2010/en/si/0264.html
http://www.irishstatutebook.ie/2010/en/si/0265.html
http://www.irishstatutebook.ie/2010/en/si/0266.html
http://www.irishstatutebook.ie/2010/en/si/0267.html
http://www.irishstatutebook.ie/2010/en/si/0268.html
http://www.irishstatutebook.ie/2010/en/si/0269.html
http://www.irishstatutebook.ie/2010/en/si/0270.html
http://www.irishstatutebook.ie/2010/en/si/0271.html
http://www.irishstatutebook.ie/2010/en/si/0272.html
http://www.irishstatutebook.ie/2010/en/si/0273.html
http://www.irishstatutebook.ie/2010/en/si/0274.html
http://www.irishstatutebook.ie/2010/en/si/0275.html
http://www.irishstatutebook.ie/2010/en/si/0276.html
http://www.irishstatutebook.ie/2010/en/si/0277.html
http://www.irishstatutebook.ie/2010/en/si/0278.html
http://www.irishstatutebook.ie/2010/en/si/0279.html
http://www.irishstatutebook.ie/2010/en/si/0280.html
http://www.irishstatutebook.ie/2010/en/si/0281.html
http://www.irishstatutebook.ie/2010/en/si/0282.html
http://www.irishstatutebook.ie/2010/en/si/0283.html
http://www.irishstatutebook.ie/2010/en/si/0284.html
http://www.irishstatutebook.ie/2010/en/si/0285.html
http://www.irishstatutebook.ie/2010/en/si/0286.html
http://www.irishstatutebook.ie/2010/en/si/0287.html
http://www.irishstatutebook.ie/2010/en/si/0288.html
http://www.irishstatutebook.ie/2010/en/si/0289.html
http://www.irishstatutebook.ie/2010/en/si/0290.html
http://www.irishstatutebook.ie/2010/en/si/0291.html
http://www.irishstatutebook.ie/2010/en/si/0292.html
http://www.irishstatutebook.ie/2010/en/si/0293.html
http://www.irishstatutebook.ie/2010/en/si/0294.html
http://www.irishstatutebook.ie/2010/en/si/0295.html
http://www.irishstatutebook.ie/2010/en/si/0296.html
http://www.irishstatutebook.ie/2010/en/si/0297.html
http://www.irishstatutebook.ie/2010/en/si/0298.html
http://www.irishstatutebook.ie/2010/en/si/0299.html
http://www.irishstatutebook.ie/2010/en/si/0300.html
http://www.irishstatutebook.ie/2010/en/si/0301.html
http://www.irishstatutebook.ie/2010/en/si/0302.html
http://www.irishstatutebook.ie/2010/en/si/0303.html
http://www.irishstatutebook.ie/2010/en/si/0304.html
http://www.irishstatutebook.ie/2010/en/si/0305.html
http://www.irishstatutebook.ie/2010/en/si/0306.html
http://www.irishstatutebook.ie/2010/en/si/0307.html
http://www.irishstatutebook.ie/2010/en/si/0308.html
http://www.irishstatutebook.ie/2010/en/si/0309.html
http://www.irishstatutebook.ie/2010/en/si/0310.html
http://www.irishstatutebook.ie/2010/en/si/0311.html
http://www.irishstatutebook.ie/2010/en/si/0312.html
http://www.irishstatutebook.ie/2010/en/si/0313.html
http://www.irishstatutebook.ie/2010/en/si/0314.html
http://www.irishstatutebook.ie/2010/en/si/0315.html
http://www.irishstatutebook.ie/2010/en/si/0316.html
http://www.irishstatutebook.ie/2010/en/si/0317.html
http://www.irishstatutebook.ie/2010/en/si/0318.html
http://www.irishstatutebook.ie/2010/en/si/0319.html
http://www.irishstatutebook.ie/2010/en/si/0320.html
http://www.irishstatutebook.ie/2010/en/si/0321.html
http://www.irishstatutebook.ie/2010/en/si/0322.html
http://www.irishstatutebook.ie/2010/en/si/0323.html
http://www.irishstatutebook.ie/2010/en/si/0324.html
http://www.irishstatutebook.ie/2010/en/si/0325.html
http://www.irishstatutebook.ie/2010/en/si/0326.html
http://www.irishstatutebook.ie/2010/en/si/0327.html
http://www.irishstatutebook.ie/2010/en/si/0328.html
http://www.irishstatutebook.ie/2010/en/si/0329.html
http://www.irishstatutebook.ie/2010/en/si/0330.html
http://www.irishstatutebook.ie/2010/en/si/0331.html
http://www.irishstatutebook.ie/2010/en/si/0332.html
http://www.irishstatutebook.ie/2010/en/si/0333.html
http://www.irishstatutebook.ie/2010/en/si/0334.html
http://www.irishstatutebook.ie/2010/en/si/0335.html
http://www.irishstatutebook.ie/2010/en/si/0336.html
http://www.irishstatutebook.ie/2010/en/si/0337.html
http://www.irishstatutebook.ie/2010/en/si/0338.html
http://www.irishstatutebook.ie/2010/en/si/0339.html
http://www.irishstatutebook.ie/2010/en/si/0340.html
http://www.irishstatutebook.ie/2010/en/si/0341.html
http://www.irishstatutebook.ie/2010/en/si/0342.html
http://www.irishstatutebook.ie/2010/en/si/0343.html
http://www.irishstatutebook.ie/2010/en/si/0344.html
http://www.irishstatutebook.ie/2010/en/si/0345.html
http://www.irishstatutebook.ie/2010/en/si/0346.html
http://www.irishstatutebook.ie/2010/en/si/0347.html
http://www.irishstatutebook.ie/2010/en/si/0348.html
http://www.irishstatutebook.ie/2010/en/si/0349.html
http://www.irishstatutebook.ie/2010/en/si/0350.html
http://www.irishstatutebook.ie/2010/en/si/0351.html
http://www.irishstatutebook.ie/2010/en/si/0352.html
http://www.irishstatutebook.ie/2010/en/si/0353.html
http://www.irishstatutebook.ie/2010/en/si/0354.html
http://www.irishstatutebook.ie/2010/en/si/0355.html
http://www.irishstatutebook.ie/2010/en/si/0356.html
http://www.irishstatutebook.ie/2010/en/si/0357.html
http://www.irishstatutebook.ie/2010/en/si/0358.html
http://www.irishstatutebook.ie/2010/en/si/0359.html
http://www.irishstatutebook.ie/2010/en/si/0360.html
http://www.irishstatutebook.ie/2010/en/si/0361.html
http://www.irishstatutebook.ie/2010/en/si/0362.html
http://www.irishstatutebook.ie/2010/en/si/0363.html
http://www.irishstatutebook.ie/2010/en/si/0364.html
http://www.irishstatutebook.ie/2010/en/si/0365.html
http://www.irishstatutebook.ie/2010/en/si/0366.html
http://www.irishstatutebook.ie/2010/en/si/0367.html
http://www.irishstatutebook.ie/2010/en/si/0368.html
http://www.irishstatutebook.ie/2010/en/si/0369.html
http://www.irishstatutebook.ie/2010/en/si/0370.html
http://www.irishstatutebook.ie/2010/en/si/0371.html
http://www.irishstatutebook.ie/2010/en/si/0372.html
http://www.irishstatutebook.ie/2010/en/si/0373.html
http://www.irishstatutebook.ie/2010/en/si/0374.html
http://www.irishstatutebook.ie/2010/en/si/0375.html
http://www.irishstatutebook.ie/2010/en/si/0376.html
http://www.irishstatutebook.ie/2010/en/si/0377.html
http://www.irishstatutebook.ie/2010/en/si/0378.html
http://www.irishstatutebook.ie/2010/en/si/0379.html
http://www.irishstatutebook.ie/2010/en/si/0380.html
http://www.irishstatutebook.ie/2010/en/si/0381.html
http://www.irishstatutebook.ie/2010/en/si/0382.html
http://www.irishstatutebook.ie/2010/en/si/0383.html
http://www.irishstatutebook.ie/2010/en/si/0384.html
http://www.irishstatutebook.ie/2010/en/si/0385.html
http://www.irishstatutebook.ie/2010/en/si/0386.html
http://www.irishstatutebook.ie/2010/en/si/0387.html
http://www.irishstatutebook.ie/2010/en/si/0388.html
http://www.irishstatutebook.ie/2010/en/si/0389.html
http://www.irishstatutebook.ie/2010/en/si/0390.html
http://www.irishstatutebook.ie/2010/en/si/0391.html
http://www.irishstatutebook.ie/2010/en/si/0392.html
http://www.irishstatutebook.ie/2010/en/si/0393.html
http://www.irishstatutebook.ie/2010/en/si/0394.html
http://www.irishstatutebook.ie/2010/en/si/0395.html
http://www.irishstatutebook.ie/2010/en/si/0396.html
http://www.irishstatutebook.ie/2010/en/si/0397.html
http://www.irishstatutebook.ie/2010/en/si/0398.html
http://www.irishstatutebook.ie/2010/en/si/0399.html
http://www.irishstatutebook.ie/2010/en/si/0400.html
http://www.irishstatutebook.ie/2010/en/si/0401.html
http://www.irishstatutebook.ie/2010/en/si/0402.html
http://www.irishstatutebook.ie/2010/en/si/0403.html
http://www.irishstatutebook.ie/2010/en/si/0404.html
http://www.irishstatutebook.ie/2010/en/si/0405.html
http://www.irishstatutebook.ie/2010/en/si/0406.html
http://www.irishstatutebook.ie/2010/en/si/0407.html
http://www.irishstatutebook.ie/2010/en/si/0408.html
http://www.irishstatutebook.ie/2010/en/si/0409.html
http://www.irishstatutebook.ie/2010/en/si/0410.html
http://www.irishstatutebook.ie/2010/en/si/0411.html
http://www.irishstatutebook.ie/2010/en/si/0412.html
http://www.irishstatutebook.ie/2010/en/si/0413.html
http://www.irishstatutebook.ie/2010/en/si/0414.html
http://www.irishstatutebook.ie/2010/en/si/0415.html
http://www.irishstatutebook.ie/2010/en/si/0416.html
http://www.irishstatutebook.ie/2010/en/si/0417.html
http://www.irishstatutebook.ie/2010/en/si/0418.html
http://www.irishstatutebook.ie/2010/en/si/0419.html
http://www.irishstatutebook.ie/2010/en/si/0420.html
http://www.irishstatutebook.ie/2010/en/si/0421.html
http://www.irishstatutebook.ie/2010/en/si/0422.html
http://www.irishstatutebook.ie/2010/en/si/0423.html
http://www.irishstatutebook.ie/2010/en/si/0424.html
http://www.irishstatutebook.ie/2010/en/si/0425.html
http://www.irishstatutebook.ie/2010/en/si/0426.html
http://www.irishstatutebook.ie/2010/en/si/0427.html
http://www.irishstatutebook.ie/2010/en/si/0428.html
http://www.irishstatutebook.ie/2010/en/si/0429.html
http://www.irishstatutebook.ie/2010/en/si/0430.html
http://www.irishstatutebook.ie/2010/en/si/0431.html
http://www.irishstatutebook.ie/2010/en/si/0432.html
http://www.irishstatutebook.ie/2010/en/si/0433.html
http://www.irishstatutebook.ie/2010/en/si/0434.html
http://www.irishstatutebook.ie/2010/en/si/0435.html
http://www.irishstatutebook.ie/2010/en/si/0436.html
http://www.irishstatutebook.ie/2010/en/si/0437.html
http://www.irishstatutebook.ie/2010/en/si/0438.html
http://www.irishstatutebook.ie/2010/en/si/0439.html
http://www.irishstatutebook.ie/2010/en/si/0440.html
http://www.irishstatutebook.ie/2010/en/si/0441.html
http://www.irishstatutebook.ie/2010/en/si/0442.html
http://www.irishstatutebook.ie/2010/en/si/0443.html
http://www.irishstatutebook.ie/2010/en/si/0444.html
http://www.irishstatutebook.ie/2010/en/si/0445.html
http://www.irishstatutebook.ie/2010/en/si/0446.html
http://www.irishstatutebook.ie/2010/en/si/0447.html
http://www.irishstatutebook.ie/2010/en/si/0448.html
http://www.irishstatutebook.ie/2010/en/si/0449.html
http://www.irishstatutebook.ie/2010/en/si/0450.html
http://www.irishstatutebook.ie/2010/en/si/0451.html
http://www.irishstatutebook.ie/2010/en/si/0452.html
http://www.irishstatutebook.ie/2010/en/si/0453.html
http://www.irishstatutebook.ie/2010/en/si/0454.html
http://www.irishstatutebook.ie/2010/en/si/0455.html
http://www.irishstatutebook.ie/2010/en/si/0456.html
http://www.irishstatutebook.ie/2010/en/si/0457.html
http://www.irishstatutebook.ie/2010/en/si/0458.html
http://www.irishstatutebook.ie/2010/en/si/0459.html
http://www.irishstatutebook.ie/2010/en/si/0460.html
http://www.irishstatutebook.ie/2010/en/si/0461.html
http://www.irishstatutebook.ie/2010/en/si/0462.html
http://www.irishstatutebook.ie/2010/en/si/0463.html
http://www.irishstatutebook.ie/2010/en/si/0464.html
http://www.irishstatutebook.ie/2010/en/si/0465.html
""".strip()

urls = urls.splitlines()




# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        #   billnumber = re.findall("Bill Number (.*?) of 2010", page, re.DOTALL)
    #    source = re.findall("Source: (.*?)<BR>", page, re.DOTALL)
     #   method = re.findall("Method: (.*?)<BR>", page, re.DOTALL)
     #   status = re.findall("Status: (.*?)<P>", page, re.DOTALL)  
    #    cmte = re.findall("&#40;Select Committee on (.*?)&#41;", page, re.DOTALL)  
      # what do you use for brackets why does this not work for something like this SPAN></SPAN> (Select Committee on Foreign Affairs) <BR>DDMMYY <BR><!--<IMG cl
    print page
#    date = re.findall("\” of</i> (.*?)</p>", page, re.DOTALL)  
    msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page)
    if msdate:
        sealdata = "%s %s %s" % msdate.groups()
    else:
        print "No seal date found", url, page
        sealdata = None  
    mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)
    dept = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts
       # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]
# data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
     #   data = {'url': url, 'title': title, 'billnumber': billnumber, 'source':source, 'method':method, 'status':status, 'cmte':cmte}
    data = {'url': url, 'title': title, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }
    scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url

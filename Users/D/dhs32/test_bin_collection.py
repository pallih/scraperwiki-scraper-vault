import scraperwiki

# Blank Python

from selenium import webdriver

print dir(webdriver)

#driver = webdriver.Chrome()

from selenium import webdriver
driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
driver.get('http://www.google.com')

print dir(driver)
#print(dir(driver))
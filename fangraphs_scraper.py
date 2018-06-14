import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

url = 'https://www.baseball-reference.com/leagues/MLB/2014.shtml'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'xml')

data = soup.find_all('table', {'class': 'rgMasterTable', 'id': 'SeasonStats1_dgSeason27_ctl00'})
print(data.prettify())

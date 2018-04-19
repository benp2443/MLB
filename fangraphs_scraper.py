import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

url = 'https://www.fangraphs.com/statss.aspx?playerid=404&position=P'
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')

data = soup.find_all('table', { 'class': 'rgMasterTable', 'id': 'SeasonStats1_dgSeason27_ctl00' })

for i in data:
    print(i.prettify())

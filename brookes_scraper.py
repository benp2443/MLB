import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time

def direct_to_data():

	#driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	driver = webdriver.Chrome(executable_path = r'C:\Users\benpa\Documents\chromedriver\chromedriver.exe')

	url = 'http://www.brooksbaseball.net/pfxVB/pfx.php'
	driver.get(url)

	driver.maximize_window()

	day = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/select[2]')
	month = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/select[1]')
	year = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/select[3]')

	day.send_keys('5')
	time.sleep(1)

	month.send_keys('June')
	time.sleep(1)

	year.send_keys('2017')
	time.sleep(1)

	select = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/input[3]')
	select.click()
	time.sleep(1)

	game = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/select[4]')
	game.send_keys('Houston Astros - Kansas City Royals')

	select = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div/form/input[3]')
	select.click()

	pitcher = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[1]/form/select[5]')
	pitcher.send_keys('Ian Kennedy - 453178 - (kca)')
	select = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[1]/form/input[4]')
	select.click()

	driver.save_screenshot('screenshot.png')

	raw_data_link = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[2]/p[1]/a').get_attribute('href')
	driver.get(raw_data_link)
	#raw_data_link.click()
	#driver.close()
	return driver

driver = direct_to_data()
soup = BeautifulSoup(driver.page_source, 'lxml')

table = soup.find('table', {'border':'1'})
for row in table.find_all('tr'):
	columns = row.find_all('td')
	if len(columns) > 0:

		print(columns[15].text)

driver.quit()

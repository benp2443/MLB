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


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
import sys
import time


driver = webdriver.Chrome(executable_path = r'C:\Users\benpa\Documents\chromedriver\chromedriver.exe')

url = 'http://www.brooksbaseball.net/pfxVB/pfx.php?month=6&day=7&year=2017&game=gid_2017_06_07_anamlb_detmlb_1%2F&prevDate=67&league=mlb'
driver.get(url)
driver.maximize_window()

def get_pitcher_links():

	pitcher_tab = driver.find_element_by_name('pitchSel')
	pitchers = pitcher_tab.find_elements_by_tag_name('option')
	pitcher_list = []
	for pitcher in pitchers:
		pitcher_list.append(pitcher.get_attribute('value'))


	day_links = []
	for pitcher in pitcher_list:
		
		select = Select(driver.find_element_by_name('pitchSel'))
		select.select_by_value(pitcher)
		button = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[1]/form/input[4]')
		button.click()

		link_button = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[2]/p[1]/a')
		day_links.append(link_button.get_attribute('href'))
		time.sleep(1)

	return day_links


#links = []
#
#game_tab = driver.find_element_by_name('game')
#games = game_tab.find_elements_by_tag_name('option')
#games_list = []
#for game in games:
#	games_list.append(game.get_attribute('value'))
#
#for game in games_list:
#
#	select = Select(driver.find_element_by_name('game'))
#	select.select_by_value(game)
#	button = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[1]/form/input[4]')
#	button.click()
#
#	day_links = get_pitcher_links()
#	links += day_links
#
#print(len(links))
#print(links)


links = get_pitcher_links()
for link in links:
	print(link)
	print(type(link))

df = pd.DataFrame()

for link in links:

	driver.get(link)
	driver.maximize_window()

	soup = BeautifulSoup(driver.page_source, 'lxml')
	pitch_count = 0
	info = []
	table = soup.find('table')
	for tr in table.find_all('tr'):
		if tr.find('td') == None:
			continue
		else:
			data = tr.find_all('td')

			pitcher_id = data[5].text
			pitch_type = data[15].text
			game_id = data[22].text
			pitch_count += 1

			info.append([pitcher_id, pitch_type, game_id, pitch_count])

	temp = pd.DataFrame(info, columns = ['pitcher_id', 'pitch_type', 'game_id', 'pitch_count'])

	if len(df) == 0:
		df = temp
	else:
		df = pd.concat([df, temp], axis = 0)

	driver.close()

		
			

	





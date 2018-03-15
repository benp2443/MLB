import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
import sys
import time

def get_pitcher_links():
        pitcher_tab = driver.find_element_by_name('pitchSel')
        pitchers = pitcher_tab.find_elements_by_tag_name('option')

        if len(pitchers) == 0:
                return []

        pitcher_list = []

        for pitcher in pitchers:
                pitcher_list.append(pitcher.get_attribute('value'))

        day_links = []
        for pitcher in pitcher_list:
        
                select = Select(driver.find_element_by_name('pitchSel'))
                select.select_by_value(pitcher)

                button = driver.find_element_by_css_selector("input[value = 'Select']")
                button.click()
                
                link_button = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div[2]/div/div[2]/div[2]/p[1]/a')
                day_links.append(link_button.get_attribute('href'))

        return day_links


def game_data(link):

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

        return temp

driver = webdriver.Chrome(executable_path = r'C:\Users\benpa\Documents\chromedriver\chromedriver.exe')

years = [2014,2015,2016,2017]
months = range(3,13) # All month tabs go from March to December
days = range(1,32) # All day tabs go from 1 to 31

links = []

for year in years:
        for month in months:
                for day in days:

                        url = 'http://www.brooksbaseball.net/pfxVB/pfx.php?month={0}&day={1}&year={2}&prevDate=314&league=mlb'.format(month, day, year)
                        print(url)
                        driver.get(url)
                        driver.maximize_window()

                        game_tab = driver.find_element_by_name('game')
                        games = game_tab.find_elements_by_tag_name('option')

                        if len(games) == 0:
                                continue

                        games_list = []

                        for game in games:
                                games_list.append(game.get_attribute('value'))

                        for game in games_list:
                                
                                select = Select(driver.find_element_by_name('game'))
                                select.select_by_value(game)

                                try:
                                        button = driver.find_element_by_css_selector("input[value = 'Select']")
                                except:
                                        print('No Buttom')
                                        continue

                                button.click()

                                game_links = get_pitcher_links()

                                if len(game_links) == 0:
                                        continue

                                links += game_links

df = pd.DataFrame()

for link in links:

        temp = game_data(link)

        if len(df) == 0:
                df = temp
                print(df.tail())
        else:
                df = pd.concat([df, temp], axis = 0)
                print(df.tail())


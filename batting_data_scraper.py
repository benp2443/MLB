import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')


links = []

years = [2013, 2014, 2015, 2016]

for year in years:

    url = 'https://www.baseball-reference.com/leagues/MLB/{}.shtml'.format(year)
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    
    table = soup.find('table', {'id':'teams_standard_batting'})
    table_body = table.find('tbody')
    
    for tr in table_body.find_all('tr'):
        team = tr.find('th')
        try:
            end_link = team.find('a')['href']
            team_link = 'https://www.baseball-reference.com' + end_link
            links.append(team_link)
        except:
            continue

data = []

for link in links:

    link_split = link.split('/')
    year = link_split[-1][:4]
    
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    
    batting_stats_table = soup.find('table', {'id':'team_batting'})
    table_body = batting_stats_table.find('tbody')
    
    for row in table_body.find_all('tr'):
        try:
            name = row.find('td', {'data-stat':'player'}).find('a').text
            name_split = name.split(' ')
            name_first = name_split[0]
            name_last = name_split[1]
        except:
            continue
        try:
            ab = row.find('td', {'data-stat':'AB'}).text
            if not ab:
                ab = '0.0'
        except:
            continue
        try:
            bb = row.find('td', {'data-stat':'BB'}).text
            if not bb:
                bb = '0.0'
        except:
            continue
        try:
            so = row.find('td', {'data-stat':'SO'}).text
            if not so:
                so = '0.0'
        except:
            continue
        try:
            obp = row.find('td', {'data-stat':'onbase_perc'}).text
            if not obp:
                obp = '0.0'
        except:
            continue
        try:
            slg = row.find('td', {'data-stat':'slugging_perc'}).text
            if not slg:
                slg = '0.0'
        except:
            continue
    
        row_data = [year, name_first, name_last, ab, bb, so, obp, slg]
        data.append(row_data)

df = pd.DataFrame(data, columns = ['year', 'name_first', 'name_last', 'ab', 'bb', 'so', 'obp', 'slg'])
df.to_csv('batting_data.csv', index = False)

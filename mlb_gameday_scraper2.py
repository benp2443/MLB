import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 300)

driver = webdriver.PhantomJS(r'/usr/bin/phantomjs')

def atbat_data(soup, inning_number, topOrBot):
        
        TopBot_pitch_data = []
        
        outs = 0
        home_runs = 0
        away_runs = 0

        for atbat in soup.find_all('atbat'):

                atbat_atts = atbat.attrs

                if 'num' in atbat_atts:
                        ab_game_num = int(atbat['num'])
                else:
                        ab_game_num = np.inf

                if 'batter' in atbat_atts:
                        batter_id  = atbat['batter']
                else:
                        batter_id = ''

                if 'stand' in atbat_atts:
                        b_handedness = atbat['stand']
                else:
                        b_handedness = ''

                if 'pitcher' in atbat_atts:
                        pitcher_id = atbat['pitcher']
                else:
                        pitcher_id = ''

                if 'p_throws' in atbat_atts:
                        p_handedness = atbat['p_throws']
                else:
                        p_handedness = ''

                if 'event_num' in atbat_atts:
                        ab_event_number = atbat['event_num']
                else:
                        ab_event_number = ''

                if 'event' in atbat_atts:
                        ab_event = atbat['event']
                else:
                        ab_event = ''

                atbat_data = [inning_number, topOrBot, ab_game_num, batter_id, b_handedness, pitcher_id, p_handedness, \
                              ab_event_number, ab_event, outs, home_runs, away_runs]

                if 'o' in atbat_atts:
                        outs = int(atbat['o'])

                        if outs == 3:
                                outs = 0 # Reset for bottom of the inning
                else:
                        outs = -1

                if 'home_team_runs' in atbat_atts:
                        home_runs = int(atbat['home_team_runs'])
                else:
                        home_runs = -1

                if 'away_team_runs' in atbat_atts:
                        away_runs = int(atbat['away_team_runs'])
                else:
                        away_runs = -1


                ball_count = 0
                strike_count = 0
                pitch_sequence = ''

                for pitch in atbat.find_all('pitch'):
                        
                        pitch_data = []

                        ball_ct = ball_count
                        strike_ct = strike_count
                        pitch_sq = pitch_sequence

                        pitch_attributes = pitch.attrs

                        if 'des' in pitch_attributes:
                                p_description = pitch['des']
                        else:
                                p_description = ''

                        if 'type' in pitch_attributes:
                                type_ = pitch['type']
                        else:
                                type_ = ''

                        if 'px' in pitch_attributes:
                                px = pitch['px']
                        else:
                                px  = ''

                        if 'pz' in pitch_attributes:
                                py = pitch['pz']
                        else:
                                py = ''

                        if 'event_num' in pitch_attributes:
                                event_num = pitch['event_num']
                        else:
                                event_num = ''

                        if 'start_speed' in pitch_attributes:
                                start_speed = pitch['start_speed']
                        else:
                                start_speed = ''

                        if 'on_1b' in pitch_attributes:
                                on_first = True
                        else:
                                on_first = False

                        if 'on_2b' in pitch_attributes:
                                on_second = True
                        else:
                                on_second = False

                        if 'on_3b' in pitch_attributes:
                                on_third = True
                        else:
                                on_third = False

                        if 'sz_top' in pitch_attributes:
                                sz_top = pitch['sz_top']
                        else:
                                sz_top = ''

                        if 'sz_bot' in pitch_attributes:
                                sz_bot = pitch['sz_bot']
                        else:
                                sz_bot = ''

                        if 'pfx_x' in pitch_attributes:
                                pfx_x = pitch['pfx_x']
                        else:
                                pfx_x = ''

                        if 'pfx_z' in pitch_attributes:
                                pfx_z = pitch['pfx_z']
                        else:
                                pfx_z = ''

                        if 'pitch_type' in pitch_attributes:
                                pitch_type = pitch['pitch_type']
                        else:
                                pitch_type = ''

                        if 'type_confidence' in pitch_attributes:
                                type_confidence = pitch['type_confidence']
                        else:
                                type_confidence = ''

                        if 'zone' in pitch_attributes:
                                zone = pitch['zone']
                        else:
                                zone = ''

                        pitch_data = atbat_data + [p_description, type_, event_num, start_speed, on_first, \
                                on_second, on_third, sz_top, sz_bot, pfx_x, pfx_z, px, py, pitch_type, \
                                type_confidence, zone, strike_count, ball_count, pitch_sequence]

                        TopBot_pitch_data.append(pitch_data)

                        if type_ == 'S' and strike_count < 2:
                                strike_count += 1
                        elif type_ == 'B':
                                ball_count += 1

                        pitch_sequence += pitch_type
                        
        return TopBot_pitch_data


def individual_game(url, game_info_list, game_link_id):
        
        game_id = game_link_id.split('/')[-2]
        game_id = game_id.strip()
        print(game_id)
        sys.stdout.flush()

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'xml')
        data = []

        for individual_innings in soup.find_all('inning'):
                
                if 'num' in individual_innings.attrs:
                        inning = int(individual_innings['num'])
                else:
                        inning = -1

                top = individual_innings.find('top')
                if top != None:
                        top_data = atbat_data(top, inning, 'top')
                        for line in top_data:
                                data.append([game_id] + game_info_list + line)
                else:
                        print('No top')

                bottom = individual_innings.find('bottom')
                if bottom != None:
                        bottom_data = atbat_data(bottom, inning, 'bottom')
                        for line in bottom_data:
                                data.append([game_id] + game_info_list + line)
                else:
                        print('No bottom')

        
        df = pd.DataFrame(data, columns = ['game_id', 'game_type', 'home_team', 'home_league', 'away_team', 'away_league', \
                                           'stadium', 'city', 'inning', 'inning_half', 'ab_game_num', 'batter_id', 'b_handedness', \
                                           'pitcher_id', 'p_handedness', 'ab_event_number', 'ab_event', 'outs', 'home_runs', \
                                           'away_runs', 'p_description', 'type_', 'event_num', 'start_speed', 'on_first', \
                                           'on_second', 'on_third', 'sz_top', 'sz_bot', 'pfx_x', 'pfx_y', 'px', 'py', 'pitch_type', \
                                           'type_confidence', 'zone', 'strike_count', 'ball_count', 'pitch_sequence'])
        
        return df


def game_info(url_):
        
        driver.get(url_)
        soup = BeautifulSoup(driver.page_source, 'xml')

        game = soup.find('game')

        game_attributes = game.attrs

        if 'type' in game_attributes:
                season_period = game['type']

        else:
                season_period = 'null'


        for team in game.find_all('team'):

                team_attributes = team.attrs

                if 'type' in team_attributes:

                        if 'name_brief' in team_attributes:

        # Need to fix this chunck of code to better account for it if home or away is not there

                                if team['type'] == 'home':
                                        home = team['name_brief']

                                        if 'league' in team_attributes:
                                                league_home = team['league']
                                        else:
                                                league_home = 'Unknown'

                                else:
                                        away = team['name_brief']

                                        if 'league' in team_attributes:
                                                league_away = team['league']
                                        else:
                                                league_away = team['league']
                                

        stadium_ = game.find('stadium')

        stadium_attributes = stadium_.attrs

        if 'name' in stadium_attributes:
                stadium = stadium_['name']

        else:
                stadium = 'Unknown'

        if 'location' in stadium_attributes:
                location = stadium_['location']

        else:
                location = 'Unknown'

        period = season_period
        info = [season_period, home, league_home, away, league_away, stadium, location]

        return period, info



def links_scraper(url, startswith_string):

        links_list = []

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        links = soup.find('ul')
        
        for link in links.find_all('li'):

                if startswith_string == 'day':
                        string = link.find('a').text.strip()[0:-1] # cut the '/' at end of string
                        if string.endswith('00'):
                            continue ## error on website has games repeated in day_00 link
                else:
                        string = link.find('a').text.strip()

                if string.startswith(startswith_string):
                        if startswith_string.startswith('gid'):
                                links_list.append(url + '/' + string)
                        else:
                                links_list.append(url + string)

        return links_list

def game_check(url):

        inning = False
        game = False
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        links = soup.find('ul')
        if links == None:
                return 'false' 

        for link in links.find_all('li'):

                text = link.find('a').text.strip()

                if text.startswith('inning'):
                        inning = True
                elif text.startswith('game.xml'):
                        game = True

        if inning == True and game == True:
                return 'true'
        else:
                return 'false'


url = 'https://gd2.mlb.com/components/game/mlb/'
pitch_df = pd.DataFrame()
years = ['2016']
cut_months = ['01/', '02/', '03/', '12/']

for year in years:

        url = url + 'year_' + year + '/'
        gid_link_startswith = 'gid_' + year
        months_list = links_scraper(url, 'month')
        drop_months = []
        for month in months_list:
                if month[-3:] in cut_months:
                        drop_months.append(month)
        for month in drop_months:
                months_list.remove(month)

        for month in months_list:

                days_list = links_scraper(month, 'day')

                for day in days_list:

                        games_list = links_scraper(day, gid_link_startswith)

                        if len(games_list) > 0:
                                
                                for game in games_list:
                                        actual_game = game_check(game)

                                        if actual_game == 'true':
                                                game_info_url = game + 'game.xml'
                                                period, info = game_info(game_info_url)
                                                if period != 'S' and period != 'E' and period != 'A':
                                                        pitch_info_url = game + 'inning/inning_all.xml'
                                                        df = individual_game(pitch_info_url, info, game)

                                                        if len(pitch_df) == 0:
                                                                pitch_df = df
                                                        else:
                                                                pitch_df = pd.concat([pitch_df, df], axis = 0)
                                                else:
                                                        continue
                                        else:
                                                continue
                        else:
                                continue


pitch_df.to_csv('mlb_gd_2016.csv', index = False)


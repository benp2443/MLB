from bs4 import BeautifulSoup
from selenium import webdriver
import sys

driver = webdriver.PhantomJS(executable_path = r'C:\Users\benpa\Documents\chromedriver\phantomjs-2.1.1-windows\bin\phantomjs.exe')

def individual_game(url):

	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'xml')

	home_away = soup.find('inning')

	if 'home_team' in home_away.attrs:
		home_team = home_away['home_team']
	else:
		home_team = ''

	if 'away_team' in home_away.attrs:
		away_team = home_away['away_team']
	else:
		away_team = ''
	
	print('Home team: {0}, Away team: {1}'.format(home_team, away_team))
	sys.stdout.flush()
	
	for individual_innings in soup.find_all('inning'):
		
		if 'num' in individual_innings.attrs:
			inning = individual_innings['num']
		else:
			inning = ''

		for atbat in individual_innings.find_all('atbat'):

			atbat_atts = atbat.attrs

			if 'num' in atbat_atts:
				num = atbat['num']
			else:
				num = ''

			if 'b' in atbat_atts:
				balls = atbat['b']
			else:
				balls = ''

			if 's' in atbat_atts:
				strikes = atbat['s']
			else:
				strikes = ''

			if 'start_tfs_zulu' in atbat_atts:
				ab_start_date_time = atbat['start_tfs_zulu']
			else:
				ab_start_date_time = ''

			if 'end_tfs_zulu' in atbat_atts:
				ab_end_date_time = atbat['end_tfs_zulu']
			else:
				ab_end_date_time = ''

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

			if 'event2' in atbat_atts:
				ab_event_2 = atbat['event2']
			else:
				ab_event_2 = ''

			# Need to think about correctly assigning outs, home runs and away runs to the right column
			# ATM being assigned as the outcome of the current atbat

			if 'o' in atbat_atts:
				outs = atbat['o']
			else:
				outs = ''

			if 'home_team_runs' in atbat_atts:
				home_runs = atbat['home_team_runs']
			else:
				home_runs = ''

			if 'away_team_runs' in atbat_atts:
				away_runs = atbat['away_team_runs']
			else:
				away_runs = ''

			for pitch in atbat.find_all('pitch'):

				pitch_attributes = pitch.attrs

				if 'des' in pitch_attributes:
					p_description = pitch['des']
				else:
					p_description = ''

				if 'id' in pitch_attributes: ## What does this measure?
					id_ = pitch['id']
				else:
					id_ = ''

				if 'type' in pitch_attributes:
					type_ = pitch['type']
				else:
					type_ = ''

				if 'code' in pitch_attributes:
					code = pitch['code']
				else:
					code = ''

				if 'tfs' in pitch_attributes:
					p_time = pitch['tfs']
				else:
					p_time = ''

				if 'x' in pitch_attributes:
					x = pitch['x']
				else:
					x  = ''

				if 'y' in pitch_attributes:
					y = pitch['y']
				else:
					y = ''

				if 'event_num' in pitch_attributes:
					event_num = pitch['event_num']
				else:
					event_num = ''

				if 'start_speed' in pitch_attributes:
					start_speed = pitch['start_speed']
				else:
					start_speed = ''

				if 'end_speed' in pitch_attributes:
					end_speed = pitch['end_speed']
				else:
					end_speed = ''

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

				if 'px' in pitch_attributes:
					px = pitch['px']
				else:
					px = ''

				if 'pz' in pitch_attributes:
					pz = pitch['pz']
				else:
					pz = ''

				if 'x0' in pitch_attributes: #Note, the variables are done with the letter O not the number
					xO = pitch['x0']
				else:
					xO = ''

				if 'y0' in pitch_attributes:
					yO = pitch['y0']
				else:
					yO = ''

				if 'z0' in pitch_attributes:
					zO = pitch['z0']
				else:
					zO = ''

				if 'vx0' in pitch_attributes:
					vxO = pitch['vx0']
				else:
					vxO = ''

				if 'vy0' in pitch_attributes:
					vyO = pitch['vy0']
				else:
					vyO = ''

				if 'vz0' in pitch_attributes:
					vzO = pitch['vz0']
				else:
					vzO = ''

				if 'ax' in pitch_attributes:
					ax = pitch['ax']
				else:
					ax = ''

				if 'ay' in pitch_attributes:
					ay = pitch['ay']
				else:
					ay = ''

				if 'az' in pitch_attributes:
					az = pitch['az']
				else:
					az = ''

				if 'break_y' in pitch_attributes:
					break_y = pitch['break_y']
				else:
					break_y = ''

				if 'break_angle' in pitch_attributes:
					break_angle = pitch['break_angle']
				else:
					break_angle = ''

				if 'break_length' in pitch_attributes:
					break_length = pitch['break_length']
				else:
					break_length = ''

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

				if 'nasty' in pitch_attributes:
					nasty = pitch['nasty']
				else:
					nasty = ''

				if 'spin_dir' in pitch_attributes:
					spin_dir = pitch['spin_dir']
				else:
					spin_dir = ''

				if 'spin_rate' in pitch_attributes:
					spin_rate = pitch['spin_rate']
				else:
					spin_rate = ''

				if 'cc' in pitch_attributes:
					cc = pitch['cc']
				else:
					cc = ''

				if 'mt' in pitch_attributes:
					mt = pitch['mt']
				else:
					mt = ''


					
url = 'https://gd2.mlb.com/components/game/mlb/year_2017/month_07/day_05'

driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')

games = []

for links in soup.find('ul'):
	link = links.find('a').text.strip()

	if link.startswith('gid'):
		games.append(link)

for game in games:

	try:
		url_ = url + '/' + game + 'inning/inning_all.xml'
		individual_game(url_)
	except:
		print('{} game did not work'.format(game)) ##Need a print to console if any links do not work
		















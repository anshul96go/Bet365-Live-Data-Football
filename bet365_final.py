#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Scrap multiple games as well as single
# Give complete lines too
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#



#betfair scrap code
import bs4 as bs
#	import urllib.request
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import re
import time
import math
import csv
import shlex


def main_function(name_a = "Italy Serie A", team_a = "Bologna", team_b = "Lazio"):

	##give name of match
	name = name_a

	##open the page
	driver = webdriver.Firefox()
	driver.get("https://www.288365.com/?nr=1#/HO/")


	##selecting language
	time.sleep(10)
	#select_lang = Select(driver.find_element_by_id('DropDownList3'))
	try:	
		select_lang = driver.find_element_by_link_text('English')
		select_lang.click()
		time.sleep(10)
	except:
		delay = 60 # seconds
		try:
		    driver.refresh()
		    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
		    print("Page is ready!")
		except TimeoutException:
			print("dead")

	##selecting game
	try:
		game = driver.find_element_by_class_name('wn-Classification_InPlay ')
		game.click()
		time.sleep(5)
		print("game selected")
	except:
		delay = 60 # seconds
		try:
		    driver.refresh()
		    time.sleep(5)
		    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
		    print("Page is ready!")
		except TimeoutException:
			print("dead")
	
	##creating excel file	
	#get neame of teams
	#-------------- Checking in multiple ongoing match championship--------------------------------------------
	try:
		time.sleep(5)
		sauce = driver.page_source
		soup = bs.BeautifulSoup(sauce,'html.parser')
		#getting the lower element compared to single match championship
		#<div class="ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading " style="">Spain Tercera</div>
		matches = soup.find_all(attrs={"class": "ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading"})  #element to catch complete the match table 
		print("getting the file name")
		for match in matches:
			heading = match.text
			print("match name: ",heading)
			if heading == name:
				print("mil gaya match")
				print(match)
				match_heading = heading
				required=((match.parent.parent).next_sibling).next_sibling
				break;
		#print("Required tag: ", required)

		#getting the required match on basis of team name
		for child in required.children:
			first_team = (((((child.contents[0]).contents[0]).contents[0]).contents[0]).next_sibling.contents[0]).contents[0].text
			second_team = (((((child.contents[0]).contents[0]).contents[0]).contents[0]).next_sibling.contents[1]).contents[0].text
			print(first_team,second_team)
			if first_team==team_a and second_team==team_b:
				print("Got the table!!")
				required_match = child.contents[0]
		required = required_match
		table = required  #ipo-Fixture_TableRow
		#print("table:")
		#print(table)
		teams_col = table.contents[0] #
		score_table = (teams_col.next_sibling).next_sibling #ipo-MainMarkets 
		teams_col_true = teams_col.contents[0] #ipo-ScoreDisplayStandard_Wrapper 
		match_time_elm = (teams_col_true.contents[0])
		match_time = match_time_elm.text
		teams_elm = match_time_elm.next_sibling
		goals_elm = teams_elm.next_sibling
		team_1 = (teams_elm.contents[0]).contents[0].text
		team_2 = (teams_elm.contents[1]).contents[0].text
		
		#get file name
		fname = name + "_" + team_1.replace(" ","_") + "_" + team_2.replace(" ","_")  + "_bet365_5"
		print("filename: ",fname.replace(" ","_"))
		filename = fname.replace(" ","_") + ".csv"
		f = open(filename, "w", encoding='utf-8')
		headers = "Match Name ,Match Time, Team 1, Team 2, Goals 1, Goals 2, Odds Win 1, Odds Win 2, Odds Draw, Next Goal 1, Next Goal 2, No Next Goal count, No Next Goal Value, Match Goals Over Count, Match Goals Over Odd,Match Goals Under Count, Match Goals Under Odd, No next goal Full, Over Full, Under Full \n" 
		f.write(headers)
	except:
		print("fucked up!")
		delay = 60 # seconds
		try:
		    driver.refresh()
		    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
		    print("Page is ready!")
		except TimeoutException:
			print("dead")


	##looping over the game
	for i in range(1500):
		
		###getting required match
		print("iteration: ",i)
		try:	
			sauce = driver.page_source
			soup = bs.BeautifulSoup(sauce,'html.parser')
			#getting the lower element compared to single match championship
			#<div class="ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading " style="">Spain Tercera</div>
			matches = soup.find_all(attrs={"class": "ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading"})  #element to catch complete the match table 
			print("getting the file name")
			for match in matches:
				heading = match.text
				print("match name: ",heading)
				if heading == name:
					match_heading = heading
					required=((match.parent).next_sibling).next_sibling
					break;
			#print("Required tag: ", required)

			#getting the required match on basis of team name
			for child in required.children:
				first_team = (((((child.contents[0]).contents[0]).contents[0]).contents[0]).next_sibling.contents[0]).contents[0].text
				second_team = (((((child.contents[0]).contents[0]).contents[0]).contents[0]).next_sibling.contents[1]).contents[0].text
				print(first_team,second_team)
				if first_team==team_a and second_team==team_b:
					print("Got the table!!")
					required_match = child.contents[0]
			required = required_match
			table = required  #ipo-Fixture_TableRow
			#print("table:")
			#print(table)
			teams_col = table.contents[0] #
			score_table = (teams_col.next_sibling).next_sibling #ipo-MainMarkets 
		except:
			delay = 60 # seconds
			try:
			    driver.refresh()
			    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
			    print("Page is ready!")
			except TimeoutException:
				print("dead")	


		###get team names, time & goals
		try:	
			teams_col_true = teams_col.contents[0] #ipo-ScoreDisplayStandard_Wrapper 
			match_time_elm = (teams_col_true.contents[0])
			match_time = match_time_elm.text
			teams_elm = match_time_elm.next_sibling
			goals_elm = teams_elm.next_sibling
			team_1 = (teams_elm.contents[0]).contents[0].text
			team_2 = (teams_elm.contents[1]).contents[0].text
			goals_1_elm = (goals_elm.contents[0]).contents[0]
			goals_1 = goals_1_elm.text
			goals_2_elm = goals_1_elm.next_sibling
			goals_2 = goals_2_elm.text 
			print(match_time,team_1,team_2,goals_1,goals_2)
		except:
			delay = 60 # seconds
			try:
			    driver.refresh()
			    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
			    print("Page is ready!")
			except TimeoutException:
				print("dead")


		###get odds
		odds_1x2 = score_table.contents[0] #ipo-MainMarketRenderer 
		next_goal = odds_1x2.next_sibling
		match_goals = next_goal.next_sibling

		##get odds of team wins
		try:
			odd_team1 = odds_1x2.contents[0].text
		except:
			odd_team1 = -1
		try:
			odd_team2 = odds_1x2.contents[1].text
		except:
			odd_team2 = -1
		try:
			odd_draw = odds_1x2.contents[2].text
		except:
			odd_draw = -1
		print(odd_team1,odd_team2,odd_draw)

		##get odds of next goal
		try:
			next_goal_1 = next_goal.contents[0].text
		except:
			next_goal_1 = -1
		try:
			next_goal_2 = next_goal.contents[1].text
		except:
			next_goal_2 = -1
		try:
			no_next_goal_cond = (next_goal.contents[2]).contents[0].text
		except:
			no_next_goal_cond = -1
		try:
			no_next_goal_val = (next_goal.contents[2]).contents[1].text
		except:
			no_next_goal_val - 1
		try:
			no_next_goal_full = next_goal.contents[2].text
		except:
			no_next_goal_full = -1
		print(next_goal_1,next_goal_2,no_next_goal_cond,no_next_goal_val)
		print("full no next goal line: ",no_next_goal_full)
		
		##get match goals
		try:
			over_cond_elm = ((match_goals.contents[0]).contents[0])
			over_cond = over_cond_elm.next_sibling.text
		except:
			over_cond = -1
		try:
			over_val_elm =  (over_cond_elm.next_sibling).next_sibling
			over_val = over_val_elm.text
		except:
			over_val = -1
		try:
			over_full = match_goals.contents[0].text
		except:
			over_full = -1
		try:	
			under_cond_elm = ((match_goals.contents[1]).contents[0])
			under_cond = under_cond_elm.next_sibling.text
		except:
			under_cond = -1
		try:
			under_val_elm =  (under_cond_elm.next_sibling).next_sibling
			under_val = under_val_elm.text
		except:
			under_val = -1
		try:
			under_full = match_goals.contents[1].text
		except:
			under_full = -1
		print(over_cond,over_val,under_cond,under_val)
		print("Full Statements: ", over_full, under_full)
		##writing in file
		headers = "Match Name ,Match Time, Team 1, Team 2, Goals 1, Goals 2, Odds Win 1, Odds Win 2, Odds Draw, Next Goal 1, Next Goal 2, No Next Goal count, No Next Goal Value, Match Goals Over Count, Match Goals Over Odd,Match Goals Under Count, Match Goals Under Odd \n" 
		f.write(str(name) + "," + str(match_time) + "," + str(team_1) + "," + str(team_2) + "," + str(goals_1) + "," + str(goals_2) + "," + str(odd_team1) + "," + str(odd_team2) + "," + str(odd_draw) + "," + str(next_goal_1) + "," + str(next_goal_2) + "," + str(no_next_goal_cond) + "," + str(no_next_goal_val) + "," + str(over_cond) + "," + str(over_val) + "," + str(under_cond) + "," + str(under_val) + "," + str(no_next_goal_full) + "," + str(over_full) + "," + str(under_full) + "," + "\n")

		delay = 60 # seconds
		try:
		    driver.refresh()
		    myElem = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='ipo-CompetitionButton_MarketHeadingLabel']")))
		    print("Page is ready!")
		except TimeoutException:
			print("dead")


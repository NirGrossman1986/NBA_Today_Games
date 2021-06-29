# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:20:55 2021

@author: Nir Grossman
"""
import logging
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import numpy as np
import json
import datetime
import requests
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import playbyplayv2
from nba_api.stats.endpoints import playbyplay

# get NBA schedule data as JSON
year = '2020'
r = requests.get('https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/' + year + '/league/00_full_schedule.json')
json_data = r.json()

# prepare output files
fout = open("filtered_schedule.csv", "w")
fout.writelines('GameDate, GameID, Visitor, Home, HomeWin')

current_dt = datetime.datetime.now() 

# loop through each month/game and write out stats to file
for i in range(len(json_data['lscd'])):
    for j in range(len(json_data['lscd'][i]['mscd']['g'])):
        gamedate = json_data['lscd'][i]['mscd']['g'][j]['gdte']
        gamedate_dt = datetime.datetime.strptime(gamedate, "%Y-%m-%d")

        game_id = json_data['lscd'][i]['mscd']['g'][j]['gid']
        visiting_team = json_data['lscd'][i]['mscd']['g'][j]['v']['ta']
        home_team = json_data['lscd'][i]['mscd']['g'][j]['h']['ta']

        fout.write('\n' + gamedate +','+ game_id +','+ visiting_team +','+ home_team)

        # don't access scores for games that haven't been played yet
        if(gamedate_dt < current_dt):  
            home_team_won = json_data['lscd'][i]['mscd']['g'][j]['h']['s'] > json_data['lscd'][i]['mscd']['g'][j]['v']['s']
            fout.write(','+ str(home_team_won))

        
fout.close()
r.close()

#define today date

today = pd.to_datetime("today").date()

#define tomorrow date(not in use yet)
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

#define the culomn names of the table 
header_list = ["GameDate", "GameID", "Visitor", "Home", "HomeWin"]

#define the table
schedule2021a = pd.read_csv("filtered_schedule.csv", names=header_list)
df = schedule2021a

#filtering the table for today current date
start_date = str(today)
end_date = str(today)
after_start_date = df["GameDate"] >= start_date
before_end_date = df["GameDate"] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_dates = df. loc[between_two_dates]
print(filtered_dates)
 
gameid = filtered_dates["GameID"]

gameid2 = gameid.iloc[0]

df_appender = []

# A loop that creates a table that compares the teams playing today and summarizes the preferred team in each column that represents data
for (h,v,j,l) in zip(filtered_dates["Home"], filtered_dates["Visitor"], filtered_dates["GameID"], filtered_dates["GameID"]):
    i += 1
    team2 = teams.find_team_by_abbreviation(h)
    
    team2a =list(team2.items()) 
    teameid = team2a[0][1]
    teamnick1 = team2a[3][1]
    raw_data = leaguedashteamstats.LeagueDashTeamStats(team_id_nullable=teameid)
    fd = raw_data.get_data_frames()[0]
    team3 = teams.find_team_by_abbreviation(v)
    team3a =list(team3.items()) 
    teameid1 = team3a[0][1]
    teamnick2 = team3a[3][1]
    
    raw_data1 = leaguedashteamstats.LeagueDashTeamStats(team_id_nullable=teameid1)
    fd1 = raw_data1.get_data_frames()[0]
    

    df_row = pd.concat([fd, fd1])   
    df_row.set_index(pd.Index([0, 1]), inplace=True)
    df_row = df_row[['TEAM_ID', 'TEAM_NAME', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG3_PCT', 'FG_PCT']]
    
    
    column = df_row['PTS']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick = team_nick2.iloc[0][2]
    #print(nick)
    
    column = df_row['REB']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick2 = team_nick2.iloc[0][2]
    #print(nick2)
    
    column = df_row['AST']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick3 = team_nick2.iloc[0][2]
    #print(nick3)
    
    column = df_row['STL']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick4 = team_nick2.iloc[0][2]
    #print(nick4)
    
    column = df_row['BLK']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick5 = team_nick2.iloc[0][2]
    #print(nick5)
    
    column = df_row['FG3_PCT']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick6 = team_nick2.iloc[0][2]
    #print(nick6)
    
    column = df_row['FG_PCT']
    max_value = column.max()
    #print("max value is", max_value)
    max_index = column.idxmax()
    #print("max index is", max_index)
    result = df_row.iloc[max_index][0]
    #print("team ID", result)
    team_nick = teams.find_team_name_by_id(result)
    #print(team_nick)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick7 = team_nick2.iloc[0][2]
    #print(nick7)
    
    
    column = df_row['TEAM_ID']
    result = df_row.iloc[0][0]
    team_nick = teams.find_team_name_by_id(result)
    team_nick2 = pd.DataFrame.from_records([team_nick])
    nick8 = gameid2
    
      
    new_row = {'TEAM_ID': j,'TEAM_NAME': teamnick1 + " vs " + teamnick2, 'PTS': str(nick), 'REB': str(nick2), 'AST': str(nick3), 'STL': str(nick4), 'BLK': str(nick5), 'FG3_PCT': str(nick6), 'FG_PCT': str(nick7)}   
    df_row = df_row.append(new_row, ignore_index=True)
    
    
    print(df_row)
    
    
    html = df_row.to_html()
    df_appender.append(html)
    
       
html2 = filtered_dates.to_html()
text_file = open("index.html", "w")
text_file.write(html2)
for html in df_appender:    
    text_file.write(html)
text_file.close()

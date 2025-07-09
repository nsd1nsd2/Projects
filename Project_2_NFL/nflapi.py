"""
Name: Roshan Peri/Freddy Elyas 
File: nflapi.py
Purpose: Backend API for data processing for the panel page 
"""


import sys 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
#sys.path.append(r'Classwork\Sankey\Sankey_Code')
sys.path.append('Classwork/Sankey/Sankey_Code')
import sankey as sk 
class NFLAPI:
    """
    Creating an NFL API for seamless data processing in the 
    dashboard
    """
    nfl = None
    def load_nfl(self,filename):
        """
        Loading the file as well as combining the most common columns 
        """
        self.nfl = pd.read_csv(filename)
        self.nfl['offense_total'] = self.nfl['offense_total_yards_gained_pass'] + self.nfl['offense_total_yards_gained_run']
        self.nfl['defensive_total'] = self.nfl['defense_total_yards_gained_pass'] + self.nfl['defense_total_yards_gained_run']
        self.nfl['total_plays'] = self.nfl['offense_n_plays_run'] + self.nfl['offense_n_plays_pass']
        self.nfl['turnovers'] = self.nfl['offense_n_interceptions'] + self.nfl['offense_n_fumbles_lost_pass'] + self.nfl['offense_n_fumbles_lost_run']
        self.nfl['takeaways'] = self.nfl['defense_n_interceptions'] + self.nfl['defense_n_fumbles_lost_run'] + self.nfl['defense_n_fumbles_lost_pass']
        return self.nfl
    def get_team(self):
        """
        Getting a list of all the teams in the dataframe 
        and returning it to the dashboard
        """
        teams_list = self.nfl['team'].unique().tolist()
        return teams_list
    def filtered_df(self, team, year_range, check):
        """
        Getting a filtered datafram based on the user input of the years and team 
        """
        start_year, end_year = year_range
        df = self.nfl
        #If checked, will return the entire dataset
        if check == True: 
            return df
        elif check == False:
            subset = df[(df['team'] == team) & (df['season'] >= start_year) & (df['season'] <= end_year)]
            return subset
    def barplot(self,team, year_range, width, height, stat,color):
        """
        Making bargraphs based on the team and statistic that the users inputs 
        """
        start_year, end_year = year_range
        df = self.nfl
        #Creating the subset of the datafram based on the team and years selected
        subset = df[(df['team'] == team) & (df['season'] >= start_year) & (df['season'] <= end_year)]
        fig, ax = plt.subplots(figsize=(width,height))
        ax.bar(subset['season'], subset[stat], color = color)
        ax.set_xlabel("Seasons")
        ax.set_ylabel(stat.replace('_', ' ').title())
        ax.set_title(f"{team} - {stat.replace('_', ' ').title()}")
        return fig
    def trend(self,team, year_range, width, height, stat, color):
        """
        Making a line plot based on the statistc and team that the user inputs (similar to the bargraph)
        """
        start_year, end_year = year_range
        df = self.nfl
        fig, ax = plt.subplots(figsize=(width, height))
        team_data = df[(df['team'] == team) & (df['season'] >= start_year) & (df['season'] <= end_year)].sort_values('season')
        season_summary = team_data.groupby('season')[stat].mean().reset_index() #ChatGPT code
        ax.plot(season_summary['season'], season_summary[stat], marker='o', color = color)
        ax.set_title(f"{team} - {stat.replace('_', ' ').title()} Over Time") #ChatGPT code
        ax.set_xlabel("Season")
        ax.set_ylabel(stat.replace('_', ' ').title())
        ax.grid(True)
        return fig


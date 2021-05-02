#!/usr/bin/python
import numpy as np
import pandas as pd

def main():
	
	pd.set_option('display.max_rows', None)
	march_madness_bracket = pd.DataFrame()
	bracket_results = pd.DataFrame(columns=['round'])
	rounds = ('rd2_win', 'rd3_win', 'rd4_win', 'rd5_win', 'rd6_win', 'rd7_win')

	## Import 538 data file and transform dtypes
	teams = pd.read_csv('fivethirtyeight_ncaa_forecasts.csv', index_col=False).dropna()
	mens_teams = teams[(teams['gender'] == 'mens') & (teams['forecast_date'] == '2021-03-18') & (teams['team_alive'] == 1)]
	mens_teams.loc[:, 'team_seed'] = mens_teams.team_seed.str[:2]
	mens_teams['team_seed'] = mens_teams['team_seed'].astype(str).astype(int)
	
	## Assign teams to different regions sorted by seeding
	## TODO: Figure out how to sort entire df without splitting by region
	midwest_bracket = mens_teams[mens_teams['team_region'] == 'Midwest'].sort_values(by="team_seed")
	west_bracket = mens_teams[mens_teams['team_region'] == 'West'].sort_values(by="team_seed")
	south_bracket = mens_teams[mens_teams['team_region'] == 'South'].sort_values(by="team_seed")
	east_bracket = mens_teams[mens_teams['team_region'] == 'East'].sort_values(by="team_seed")

	## Setup teams into MM formatted bracket based on seeding/region
	for region in [midwest_bracket, west_bracket, south_bracket, east_bracket]:
		march_madness_bracket = pd.concat([march_madness_bracket, bracketize(region)], axis=0, ignore_index=True)

	for round in rounds:
		march_madness_bracket = simulate_round(march_madness_bracket[march_madness_bracket.team_alive == 1], round)
		bracket_results = pd.concat([bracket_results, march_madness_bracket], axis=0, ignore_index=True)
		losing_indexes = march_madness_bracket[march_madness_bracket.team_alive == 0].index
		march_madness_bracket.drop(losing_indexes, inplace=True)
		march_madness_bracket.reset_index(drop=True, inplace=True)

	export_bracket(bracket_results)

def bracketize(team_region):
	bracketed_format = pd.DataFrame()
	bracketed_format = bracketed_format.append(team_region.iloc[0])
	bracketed_format = bracketed_format.append(team_region.iloc[15])
	bracketed_format = bracketed_format.append(team_region.iloc[7])
	bracketed_format = bracketed_format.append(team_region.iloc[8])
	bracketed_format = bracketed_format.append(team_region.iloc[4])
	bracketed_format = bracketed_format.append(team_region.iloc[11])
	bracketed_format = bracketed_format.append(team_region.iloc[3])
	bracketed_format = bracketed_format.append(team_region.iloc[12])
	bracketed_format = bracketed_format.append(team_region.iloc[5])
	bracketed_format = bracketed_format.append(team_region.iloc[10])
	bracketed_format = bracketed_format.append(team_region.iloc[2])
	bracketed_format = bracketed_format.append(team_region.iloc[13])
	bracketed_format = bracketed_format.append(team_region.iloc[6])
	bracketed_format = bracketed_format.append(team_region.iloc[9])
	bracketed_format = bracketed_format.append(team_region.iloc[1])
	bracketed_format = bracketed_format.append(team_region.iloc[14])
	return bracketed_format

def simulate_round(team_pool, round_probability):
	for i in range(0, len(team_pool), 2):
		winner = get_winner(team_pool.loc[i, ['team_name', round_probability]], team_pool.loc[i+1, ['team_name',round_probability]])
		if team_pool.loc[i, 'team_name'] == winner:
			team_pool.at[i+1, 'team_alive'] = 0
		else:
			team_pool.at[i, 'team_alive'] = 0
	return team_pool

def get_winner(team1, team2):
	team1_odds = team1.iloc[1]
	team2_odds = team2.iloc[1]
	while(True):
		team1_win = np.random.random_sample() < team1_odds
		team2_win = np.random.random_sample() < team2_odds
		if team1_win == True and team2_win == False:
			return team1.team_name
		elif team1_win == False and team2_win == True:
			return team2.team_name
		else:
			continue

def export_bracket(bracket_results):
	bracket_results.loc[bracket_results.index < 64, 'round'] = "RO64"
	bracket_results.loc[(bracket_results.index >= 64) & (bracket_results.index < 96), 'round'] = "RO32"
	bracket_results.loc[(bracket_results.index >= 96) & (bracket_results.index < 112), 'round'] = "Sweet Sixteen"
	bracket_results.loc[(bracket_results.index >= 112) & (bracket_results.index < 120), 'round'] = "Elite 8"
	bracket_results.loc[(bracket_results.index >= 120) & (bracket_results.index < 124), 'round'] = "Final Four"
	bracket_results.loc[(bracket_results.index >= 124) & (bracket_results.index < 126), 'round'] = "Championship"
	bracket_results.to_csv('march_madness_bracket.csv', index=False, columns=["round", "team_seed", "team_name", "team_alive"])

if __name__ == '__main__':
	main()

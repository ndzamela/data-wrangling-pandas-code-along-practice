# --------------
import pandas as pd 
import numpy as np
# Read the data using pandas module.
df_ipl = pd.read_csv(path)

df_ipl.head()
print(df_ipl.shape)

# Find the list of unique cities where matches were played
print("Venues Played at: ", df_ipl['city'].unique())

print("THe number of unique cities where matches were played at: ", len(df_ipl['city'].unique()))

# Find the columns which contains null values if any ?
df_ipl.isnull().sum()

# List down top 5 most played venues
venues = df_ipl.groupby('venue')['match_code'].nunique().sort_values(ascending=False)
venues

print("Top 5 venues by number of matches: ", venues[0:5])

# Make a runs count frequency table
runs_cnt = df_ipl['runs'].value_counts()

print("Runs count frequency table: \n", runs_cnt)

# How many seasons were played and in which year they were played 
type(df_ipl['date'][0])
df_ipl['year'] = df_ipl['date'].apply(lambda date_row: date_row[:4])
df_ipl['month'] = df_ipl['date'].apply(lambda date_row: date_row[5:7])
df_ipl['month']
print(df_ipl.shape)
print("The number of seasons the matches were played in: ", len(df_ipl['year'].unique()))
print("The seasons the matches were played in: ", df_ipl['year'].unique())

# No. of matches played per season
matches_per_season = df_ipl.groupby('year')['match_code'].nunique().sort_values()

print("Matches held per season: \n", matches_per_season)

# Total runs across the seasons
runs_per_season = df_ipl.groupby('year')['total'].sum()

print("Total runs scored per season: \n", runs_per_season)

# Teams who have scored more than 200+ runs. Show the top 10 results
high_scores = df_ipl.groupby(['match_code','inning','team1','team2'])['total'].sum().reset_index()
teams_with_over_200_runs = high_scores[high_scores['total'] > 200]
print("Teams that had more than 200 runs: \n",teams_with_over_200_runs)

# What are the chances of chasing 200+ target
#print("----------------Question 10----------------")
high_scores1 = high_scores[high_scores['inning'] == 1]
high_scores2 = high_scores[high_scores['inning'] == 2]
high_scores1=high_scores1.merge(high_scores2[['match_code','inning','total']], on='match_code')
#print(high_scores1.columns.values)
high_scores1.rename(columns={'inning_x':'inning_1','inning_y':'inning_2','total_x':'inning1_runs','total_y':'inning2_runs'}, inplace=True)
#print(high_scores1.columns.values)
high_scores1 = high_scores1[high_scores1['inning1_runs']>200]
#high_scores1['is_score_chased'] = 1
high_scores1['is_score_chased'] = np.where(high_scores1['inning1_runs'] < high_scores1['inning2_runs'], 'yes','no')

chances = high_scores1['is_score_chased'].value_counts()

print(chances)

#high_scores1.head()
#high_scores2.head()

high_scores1=high_scores1.merge(high_scores2[['match_code','inning','total']], on='match_code')
print(high_scores1.columns.values)

# Which team has the highest win count in their respective seasons ?
remove_duplicate_matchcodes = df_ipl.drop_duplicates(subset="match_code", keep="first").reset_index(drop=True)
matchwon_by_team = remove_duplicate_matchcodes.groupby('year')['winner'].value_counts()

print(matchwon_by_team)




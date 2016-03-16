
# coding: utf-8

# In[203]:

import sqlalchemy
import pandas as pd
engine = sqlalchemy.create_engine('mysql://root:password@127.0.0.1:3306/nba')


# In[204]:

sql = """
select l.game_date_est,
-- PLAYER STATS
t.PLAYER_ID,
t.MIN as player_MIN,
t.FGA as player_FGA,
t.FGM as player_FGM,
t.FG3M as player_FG3M,
t.FG3A as player_FG3A,
t.FTA as player_FTA,
t.FTM as player_FTM,
t.OREB as player_OREB,
t.DREB as player_DREB,
t.AST as player_AST,
t.STL as player_STL,
t.BLK as player_BLK,
t.TO as player_TO,
t.PTS as player_PTS,
a.OFF_RATING as player_OFF_RATING,
a.DEF_RATING as player_DEF_RATING,
a.NET_RATING as player_NET_RATING,
a.PIE as player_PIE,
t.PLUS_MINUS as player_PLUS_MINUS,
-- PLAYER TEAM STATS
t_p.PLUS_MINUS as team_PLUS_MINUS,
-- OPPOSING TEAM STATS
t_o.OREB as opponent_OREB,
t_o.DREB as opponent_DREB,
t_o.STL as opponent_STL,
t_o.BLK as opponent_BLK,
a_o.OFF_RATING as opponent_OFF_RATING,
a_o.DEF_RATING as opponent_DEF_RATING,
a_o.NET_RATING as opponent_NET_RATING,
t.score
from traditional_boxscores t
join line_score l on l.game_id = t.game_id and l.team_id = t.team_id
join advanced_boxscores a on a.game_id = t.game_id and a.player_id = t.player_id and a.team_id = t.team_id
join advanced_boxscores_team a_o on t.game_id = a_o.game_id and t.team_id != a_o.team_id
join traditional_boxscores_team t_p on t_p.game_id = t.game_id and t.team_id = t_p.team_id
join traditional_boxscores_team t_o on t_o.game_id = t.game_id and t.team_id != t_o.team_id
"""
df = pd.read_sql(sql, engine)
df['game_date_est'] = pd.to_datetime(df.game_date_est)
df['player_MIN'] = df['player_MIN'].apply(lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1]))
df.sort_values(['PLAYER_ID', 'game_date_est'], inplace=True)


# In[205]:

df.describe()


# In[206]:

cols = df.keys()
excluded = ['game_date_est', 'PLAYER_ID', 'score', 'index']
# df for every game that every player played in
player_games = pd.DataFrame()

# watch out for PLUS_MINUS! everything else can be averaged. Need to delete index before render to CSV!
i = 0

player_groups = df.groupby('PLAYER_ID').groups
for player_id in player_groups:
    if i % 50 == 0:
        print "%0.2f%% complete" % ((float(i) / len(player_groups)) * 100)
    i += 1
    player_df = df[(df['PLAYER_ID'] == player_id)].sort_values(['game_date_est'])
    player_df['index'] = range(len(player_df)) 
    for col in cols:
        if 'PLUS_MINUS' not in col and col not in excluded:
            cumulative_sum = player_df[col].cumsum()
            player_df[col + '_cumsum'] = cumulative_sum
            player_df[col + '_prev'] = pd.rolling_mean(player_df[col], 1)
            player_df[col + '_mean_3'] = pd.rolling_mean(player_df[col], 3)
            player_df[col + '_mean_5'] = pd.rolling_mean(player_df[col], 5)
            player_df[col + '_mean'] = cumulative_sum.div(player_df['index'] + 1)
    player_games = player_games.append(player_df.fillna(0))


# In[207]:

cols = player_games.keys()
# we want score to come last!
csv_cols = [col for col in cols if col not in excluded] + ['score']
pct_train = 0.90
num_train = int(len(player_games) * pct_train)
num_validate = len(player_games) - num_train
player_games.head(num_train).to_csv('pybrain-practice/data/train.csv', header=False, columns=csv_cols, index=False)
player_games.tail(num_validate).to_csv('pybrain-practice/data/validation.csv', header=False, columns=csv_cols, index=False)


# In[208]:

player_games.tail(10)


# In[ ]:




# In[ ]:




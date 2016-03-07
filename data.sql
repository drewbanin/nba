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
limit 100

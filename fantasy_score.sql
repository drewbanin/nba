alter table traditional_boxscores add column score double;

update traditional_boxscores as q
join

(select 
*,
(points * 1) + (field_goal_3_made * 0.5) + (rebounds * 1.25) + (assists * 1.5) + (steals * 2) + (blocks * 2) + (turnovers * -0.5) + (double_double * 1.5) + (triple_double * 3) as score
from (
select *,
double_score >= 2 as double_double,
double_score >= 3 as triple_double
from (
select *,
 (pts_double + reb_double + ast_double + blk_double + stl_double) as double_score
from (
select
 player_name,
 game_id,
 team_id,
 player_id,
 pts as points,
 fg3m as field_goal_3_made,
 reb as rebounds,
 ast as assists,
 stl as steals,
 blk as blocks,
 `to` as turnovers,
  pts >= 10 as pts_double,
  reb >= 10 as reb_double,
  ast >= 10 as ast_double,
  blk >= 10 as blk_double,
  stl >= 10 as stl_double  
from traditional_boxscores
) s
)s2
)s3 
) final
on final.player_id = q.player_id and final.game_id = q.game_id and final.team_id = q.team_id
set q.score = final.score

select
REP_MapName,
CONG_MapName,
PWPStatsExist,
TurnoutMessage,
ResultsOfficial,
DisplayTurnoutStats,
SEN_MapName,
PostElectionStatsAvailable,
Order,
ElectionDate,
RaceStatsExist,
PKElectionID,
from unnest(Dates.Date)
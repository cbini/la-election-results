select
    d.pkelectionid as pk_election_id,
    d.electiondate as election_date,
    d.resultsofficial as results_official,
    d.rep_mapname as rep_map_name,
    d.cong_mapname as cong_map_name,
    d.sen_mapname as sen_map_name,
    d.turnoutmessage as turnout_message,
    d.pwpstatsexist as pwp_stats_exist,
    d.racestatsexist as race_stats_exist,
    d.postelectionstatsavailable as post_election_stats_available,
    d.displayturnoutstats as display_turnout_stats,
    d.order as `order`,
from {{ source("election_results", "election_dates") }} as ed
cross join unnest(ed.dates.date) as d

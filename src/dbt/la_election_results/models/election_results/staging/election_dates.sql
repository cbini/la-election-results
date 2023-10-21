select
    d.pkelectionid as pk_election_id,
    d.electiondate as election_date,
    d.rep_mapname as rep_map_name,
    d.cong_mapname as cong_map_name,
    d.sen_mapname as sen_map_name,
    d.turnoutmessage as turnout_message,
    d.order as `order`,

    if(d.resultsofficial = 1, true, false) as results_official,
    if(d.pwpstatsexist = 1, true, false) as pwp_stats_exist,
    if(d.racestatsexist = 1, true, false) as race_stats_exist,
    if(d.postelectionstatsavailable = 1, true, false) as post_election_stats_available,
    if(d.displayturnoutstats = 1, true, false) as display_turnout_stats,
from {{ source("election_results", "election_dates") }} as ed
cross join unnest(ed.dates.date) as d

select
    vp._election_date as _election_date,
    vp._parish as _parish,
    vp._race as _race,
    vp.precincts.versiondatetime as version_date_time,

    p.precinct as precinct,
    p.hasreported as has_reported,
    p.votercountqualified as voter_count_qualified,
    p.votercountvoted as voter_count_voted,

    c.id as choice_id,
    c.votetotal as choice_vote_total,
from {{ source("election_results", "votes_precinct") }} as vp
cross join unnest(vp.precincts.precinct) as p
cross join unnest(p.choice) as c

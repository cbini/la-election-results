select
    vp._race as race_id,
    vp.precincts.versiondatetime as version_date_time,
    right(concat('0', vp._parish), 2) as parish_value,
    parse_date('%Y%m%d', safe_cast(vp._election_date as string)) as election_date,

    p.precinct as precinct,
    p.votercountqualified as voter_count_qualified,
    p.votercountvoted as voter_count_voted,
    if(p.hasreported = 1, true, false) as has_reported,

    c.id as choice_id,
    c.votetotal as choice_vote_total,
from {{ source("election_results", "votes_precinct") }} as vp
cross join unnest(vp.precincts.precinct) as p
cross join unnest(p.choice) as c

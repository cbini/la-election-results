select
    vpr._election_date as _election_date,
    vpr._parish as _parish,
    vpr.races.versiondatetime as version_date_time,

    r.id as race_id,
    r.precinctsexpected as precincts_expected,
    r.precinctsreporting as precincts_reporting,
    r.votercountqualified as voter_count_qualified,
    r.votercountvoted as voter_count_voted,
    r.numabsenteeexpected as num_absentee_expected,
    r.numabsenteereporting as num_absentee_reporting,

    c.id as choice_id,
    c.votetotal as choice_vote_total,
    c.outcome as choice_outcome,
from {{ source("election_results", "votes_parish_race") }} as vpr
cross join unnest(vpr.races.race) as r
cross join unnest(r.choice) as c

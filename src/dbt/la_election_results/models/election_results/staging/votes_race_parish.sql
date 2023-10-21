select
    vrp._race as race_id,
    vrp.parishes.versiondatetime as version_date_time,
    parse_date('%Y%m%d', safe_cast(vrp._election_date as string)) as election_date,

    p.precinctsexpected as precincts_expected,
    p.precinctsreporting as precincts_reporting,
    p.votercountqualified as voter_count_qualified,
    p.votercountvoted as voter_count_voted,
    p.numabsenteeexpected as num_absentee_expected,
    p.numabsenteereporting as num_absentee_reporting,
    right(concat('0', p.parishvalue), 2) as parish_value,

    c.id as choice_id,
    c.votetotal as choice_vote_total,
    c.outcome as choice_outcome,
from {{ source("election_results", "votes_race_parish") }} as vrp
cross join unnest(vrp.parishes.parish) as p
cross join unnest(p.choice) as c

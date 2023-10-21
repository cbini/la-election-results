select
    vm.races.versiondatetime as version_date_time,
    parse_date('%Y%m%d', safe_cast(vm._election_date as string)) as election_date,

    r.id as race_id,
    r.votercountqualified as voter_count_qualified,
    r.votercountvoted as voter_count_voted,
    r.precinctsexpected as precincts_expected,
    r.precinctsreporting as precincts_reporting,
    r.numabsenteeexpected as num_absentee_expected,
    r.numabsenteereporting as num_absentee_reporting,

    c.id as choice_id,
    c.votetotal as choice_vote_total,
    c.outcome as choice_outcome,
from {{ source("election_results", "votes_multiparish") }} as vm
cross join unnest(vm.races.race) as r
cross join unnest(r.choice) as c

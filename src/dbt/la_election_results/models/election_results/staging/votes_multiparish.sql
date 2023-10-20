select
    vm._election_date as _election_date,
    vm.races.versiondatetime as version_date_time,

    r.id as race_id,
    r.votercountqualified as voter_count_qualified,
    r.votercountvoted as voter_count_voted,
    r.precinctsexpected as precincts_expected,
    r.precinctsreporting as precincts_reporting,
    r.numabsenteeexpected as num_absentee_expected,
    r.numabsenteereporting as num_absentee_reporting,

    c.id as choice_id,
    c.outcome as choice_outcome,
    c.votetotal as choice_vote_total,
from {{ source("election_results", "votes_multiparish") }} as vm
cross join unnest(vm.races.race) as r
cross join unnest(r.choice) as c

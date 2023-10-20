select
    pie._election_date,
    pie.parishesinelection.versiondatetime as version_date_time,

    p.parishvalue as parish_value,
    p.precincts as precincts,
    p.precinctsreported as precincts_reported,
    p.completewithabsentee as complete_with_absentee,
from {{ source("election_results", "parishes_in_election") }} as pie
cross join unnest(pie.parishesinelection.parish) as p

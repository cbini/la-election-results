with
    parishes_in_election as (
        select
            pie.parishesinelection.versiondatetime as version_date_time,
            parse_date(
                '%Y%m%d', safe_cast(pie._election_date as string)
            ) as election_date,

            p.precincts as precincts,
            p.precinctsreported as precincts_reported,
            right(concat('0', p.parishvalue), 2) as parish_value,
            if(p.completewithabsentee = 1, true, false) as complete_with_absentee,
        from {{ source("election_results", "parishes_in_election") }} as pie
        cross join unnest(pie.parishesinelection.parish) as p
    )

select pie.*, pm.name as parish_name,
from parishes_in_election as pie
inner join {{ ref("parish_metadata") }} as pm on pie.parish_value = pm.id

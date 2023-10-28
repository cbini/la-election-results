with
    census as (
        select *, replace(county, ' Parish', '') as parish_name,
        from {{ source("election_results", "census") }}
    )

select c.*, pc.precinct,
from census as c
left join
    {{ source("election_results", "precinct_crosswalk") }} as pc
    on c.parish_name = pc.parish_name
    and c.vtda = pc.vtda

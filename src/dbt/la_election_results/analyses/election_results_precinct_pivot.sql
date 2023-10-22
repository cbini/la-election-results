with
    prepivot as (
        select
            election_date,
            race_id,
            specific_title,
            parish_name,
            precinct,
            voter_count_qualified,
            choice_vote_total,
            coalesce(choice_party, 'NULL') as choice_party,
            sum(choice_vote_total) over (
                partition by election_date, race_id, parish_name, precinct
            ) as voter_count_voted,
        from {{ ref("election_results") }}
    )

select
    *,
    safe_divide(
        voter_count_voted, voter_count_qualified
    ) as voter_participation_qualified,
from
    prepivot pivot (
        sum(choice_vote_total) for choice_party
        in ('DEM', 'IND', 'LBT', 'NOPTY', 'NULL', 'OTHER', 'REP')
    )
order by voter_participation_qualified desc

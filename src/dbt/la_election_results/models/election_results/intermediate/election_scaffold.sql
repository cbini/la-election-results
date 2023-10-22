with
    date_parish as (
        select
            ed.pk_election_id,
            ed.election_date,
            ed.rep_map_name,
            ed.cong_map_name,
            ed.sen_map_name,
            ed.turnout_message,
            ed.order,
            ed.results_official,
            ed.pwp_stats_exist,
            ed.race_stats_exist,
            ed.post_election_stats_available,
            ed.display_turnout_stats,

            pie.parish_value,
            pie.precincts,
            pie.precincts_reported,
            pie.complete_with_absentee,
        from {{ ref("election_dates") }} as ed
        inner join
            {{ ref("parishes_in_election") }} as pie
            on ed.election_date = pie.election_date
    )

select
    dp.pk_election_id,
    dp.election_date,
    dp.rep_map_name,
    dp.cong_map_name,
    dp.sen_map_name,
    dp.turnout_message,
    dp.order,
    dp.results_official,
    dp.pwp_stats_exist,
    dp.race_stats_exist,
    dp.post_election_stats_available,
    dp.display_turnout_stats,
    dp.parish_value,
    dp.precincts,
    dp.precincts_reported,
    dp.complete_with_absentee,

    rc.level,
    rc.race_id,
    rc.office_level,
    rc.general_title,
    rc.specific_title,
    rc.summary_text,
    rc.full_text,
    rc.number_to_be_elected,
    rc.choice_id,
    rc.choice_description,
    rc.choice_party,
    rc.choice_color,
    rc.is_closed_party,
    rc.is_presidential_nominee,
    rc.is_multi_parish,
from date_parish as dp
inner join
    {{ ref("races_candidates") }} as rc
    on dp.election_date = rc.election_date
    and dp.parish_value = rc.parish_value
    and rc.level = 'parish'

union all

select
    dp.*,

    rc.level,
    rc.race_id,
    rc.office_level,
    rc.general_title,
    rc.specific_title,
    rc.summary_text,
    rc.full_text,
    rc.number_to_be_elected,
    rc.choice_id,
    rc.choice_description,
    rc.choice_party,
    rc.choice_color,
    rc.is_closed_party,
    rc.is_presidential_nominee,
    rc.is_multi_parish,
from date_parish as dp
inner join
    {{ ref("races_candidates") }} as rc
    on dp.election_date = rc.election_date
    and rc.level = 'multiparish'

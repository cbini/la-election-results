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

    vp.race_id,
    vp.parish_value,
    vp.precinct,
    vp.has_reported,
    vp.choice_id,
    vp.voter_count_qualified,
    vp.voter_count_voted,
    vp.choice_vote_total,

    pie.parish_name,
    pie.precincts,
    pie.precincts_reported,
    pie.complete_with_absentee,

    c.u7d001 as total_population_18plus,

    coalesce(rcp.office_level, rcm.office_level) as office_level,
    coalesce(rcp.general_title, rcm.general_title) as general_title,
    coalesce(rcp.specific_title, rcm.specific_title) as specific_title,
    coalesce(rcp.summary_text, rcm.summary_text) as summary_text,
    coalesce(rcp.full_text, rcm.full_text) as full_text,
    coalesce(rcp.choice_description, rcm.choice_description) as choice_description,
    coalesce(rcp.choice_party, rcm.choice_party) as choice_party,
    coalesce(rcp.choice_color, rcm.choice_color) as choice_color,
    coalesce(rcp.is_closed_party, rcm.is_closed_party) as is_closed_party,
    coalesce(rcp.is_multi_parish, rcm.is_multi_parish) as is_multi_parish,
    coalesce(
        rcp.is_presidential_nominee, rcm.is_presidential_nominee
    ) as is_presidential_nominee,
    coalesce(
        rcp.number_to_be_elected, rcm.number_to_be_elected
    ) as number_to_be_elected,
from {{ ref("election_dates") }} as ed
inner join {{ ref("votes_precinct") }} as vp on ed.election_date = vp.election_date
inner join
    {{ ref("parishes_in_election") }} as pie
    on vp.parish_value = pie.parish_value
    and vp.election_date = pie.election_date
left join
    {{ ref("races_candidates") }} as rcp
    on vp.election_date = rcp.election_date
    and vp.race_id = rcp.race_id
    and vp.parish_value = rcp.parish_value
    and vp.choice_id = rcp.choice_id
    and rcp.level = 'parish'
left join
    {{ ref("races_candidates") }} as rcm
    on vp.election_date = rcm.election_date
    and vp.race_id = rcm.race_id
    and vp.choice_id = rcm.choice_id
    and rcm.level = 'multiparish'
left join
    {{ ref("census") }} as c
    on pie.parish_name = c.parish_name
    and vp.precinct = c.precinct

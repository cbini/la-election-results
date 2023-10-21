select
    vp.election_date,
    vp.race_id,
    vp.parish_value,
    vp.precinct,
    vp.has_reported,
    vp.voter_count_qualified,
    vp.voter_count_voted,
    vp.choice_id,
    vp.choice_vote_total,

    ed.pk_election_id,
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

    pie.precincts,
    pie.precincts_reported,
    pie.complete_with_absentee,

    rc.level,
    rc.office_level,
    rc.general_title,
    rc.specific_title,
    rc.summary_text,
    rc.full_text,
    rc.number_to_be_elected,
    rc.choice_description,
    rc.choice_party,
    rc.choice_color,
    rc.is_closed_party,
    rc.is_presidential_nominee,
    rc.is_multi_parish,
from {{ ref("votes_precinct") }} as vp
inner join {{ ref("election_dates") }} as ed on vp.election_date = ed.election_date
inner join
    {{ ref("parishes_in_election") }} as pie
    on vp.election_date = pie.election_date
    and vp.parish_value = pie.parish_value
inner join
    {{ ref("races_candidates") }} as rc
    on vp.election_date = rc.election_date
    and vp.race_id = rc.race_id
    and vp.choice_id = rc.choice_id

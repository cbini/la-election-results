select
    es.pk_election_id,
    es.election_date,
    es.rep_map_name,
    es.cong_map_name,
    es.sen_map_name,
    es.turnout_message,
    es.order,
    es.results_official,
    es.pwp_stats_exist,
    es.race_stats_exist,
    es.post_election_stats_available,
    es.display_turnout_stats,
    es.parish_value,
    es.precincts,
    es.precincts_reported,
    es.complete_with_absentee,
    es.level,
    es.race_id,
    es.office_level,
    es.general_title,
    es.specific_title,
    es.summary_text,
    es.full_text,
    es.number_to_be_elected,
    es.choice_id,
    es.choice_description,
    es.choice_party,
    es.choice_color,
    es.is_closed_party,
    es.is_presidential_nominee,
    es.is_multi_parish,

    vp.precinct,
    vp.has_reported,
    vp.voter_count_qualified,
    vp.voter_count_voted,
    vp.choice_id,
    vp.choice_vote_total,
from {{ ref("election_scaffold") }} as es
left join
    {{ ref("votes_precinct") }} as vp
    on es.election_date = vp.election_date
    and es.race_id = vp.race_id
    and es.parish_value = vp.parish_value
    and es.choice_id = vp.choice_id

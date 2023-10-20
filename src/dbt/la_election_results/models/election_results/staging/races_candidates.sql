select
    rc._election_date as election_date,
    rc._level as `level`,
    rc._parish as parish,
    rc.races.writetime as write_time,

    r.id as race_id,
    r.generaltitle as general_title,
    r.specifictitle as specific_title,
    r.officelevel as office_level,
    r.summarytext as summary_text,
    r.fulltext as full_text,
    r.numbertobeelected as number_to_be_elected,
    r.isclosedparty as is_closed_party,
    r.ispresidentialnominee as is_presidential_nominee,
    r.ismultiparish as is_multi_parish,

    c.id as choice_id,
    c.desc as choice_description,
    c.color as choice_color,
from {{ source("election_results", "races_candidates") }} as rc
cross join unnest(rc.races.race) as r
cross join unnest(r.choice) as c

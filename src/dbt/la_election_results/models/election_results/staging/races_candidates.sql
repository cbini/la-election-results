select
    rc._level as `level`,
    rc._parish as parish_value,
    rc.races.writetime as write_time,
    parse_date('%Y%m%d', safe_cast(rc._election_date as string)) as election_date,

    r.id as race_id,
    r.generaltitle as general_title,
    r.specifictitle as specific_title,
    r.officelevel as office_level,
    r.summarytext as summary_text,
    r.fulltext as full_text,
    r.numbertobeelected as number_to_be_elected,
    if(r.isclosedparty = 1, true, false) as is_closed_party,
    if(r.ispresidentialnominee = 1, true, false) as is_presidential_nominee,
    if(r.ismultiparish = 1, true, false) as is_multi_parish,

    c.id as choice_id,
    lower(format('0x%X', safe_cast(c.color as int))) as choice_color,
    regexp_replace(c.desc, r'\s\(\w+\)', '') as choice_description,
    regexp_extract(c.desc, r'\((\w+)\)') as choice_party,
from {{ source("election_results", "races_candidates") }} as rc
cross join unnest(rc.races.race) as r
cross join unnest(r.choice) as c

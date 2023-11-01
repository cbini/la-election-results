import json
import os

import google.auth
from google.cloud import storage

from la_election_results.client import ElectionResultsClient

# instantiate client
CLIENT = ElectionResultsClient()

# setup gcs
credentials, project_id = google.auth.load_credentials_from_dict(
    info=json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
)

storage_client = storage.Client(project=project_id, credentials=credentials)

BUCKET = storage_client.get_bucket("la-election-results")


def dump_json_to_blob(blob_name, data):
    blob = BUCKET.blob(blob_name=blob_name)

    print(f"Saving to {blob.public_url}...")
    blob.upload_from_string(data=json.dumps(obj=data))


def get_multiparish_race_data(election_date, race_id):
    # VotesRaceByParish
    votes_race_by_parish = CLIENT.votes_race_by_parish(
        election_date=election_date, race_id=race_id
    )

    dump_json_to_blob(
        blob_name=(
            f"votes_race_parish/_election_date={election_date}/_race={race_id}/"
            "data.json"
        ),
        data=votes_race_by_parish,
    )

    # get all parish values for race
    parishes = votes_race_by_parish["Parishes"]["Parish"]

    if isinstance(parishes, dict):
        parishes = [parishes]

    parish_values = sorted([parish["ParishValue"] for parish in parishes])

    for parish_value in parish_values:
        # VotesRaceByPrecinct
        votes_race_by_precinct = CLIENT.votes_race_by_precinct(
            election_date=election_date, race_id=race_id, parish_value=parish_value
        )

        dump_json_to_blob(
            blob_name=(
                f"votes_precinct/_election_date={election_date}/_race={race_id}/"
                f"_parish={parish_value}/data.json"
            ),
            data=votes_race_by_precinct,
        )


def get_parish_race_data(election_date, parish_value):
    # VotesParish
    votes_parish = CLIENT.votes_parish(
        election_date=election_date, parish_value=parish_value
    )

    dump_json_to_blob(
        blob_name=(
            f"votes_parish_race/_election_date={election_date}/_parish={parish_value}/"
            "data.json"
        ),
        data=votes_parish,
    )

    # RacesCandidates
    races_candidates_by_parish = CLIENT.races_candidates_by_parish(
        election_date=election_date, parish_value=parish_value
    )

    dump_json_to_blob(
        blob_name=(
            f"races_candidates/_election_date={election_date}/_level=parish/"
            f"_parish={parish_value}/data.json"
        ),
        data=races_candidates_by_parish,
    )

    # get all race ids for parish
    parish_races = races_candidates_by_parish["Races"]["Race"]

    if isinstance(parish_races, dict):
        parish_races = [parish_races]

    parish_race_ids = sorted([race["ID"] for race in parish_races])

    for race_id in parish_race_ids:
        # VotesRaceByPrecinct
        votes_race_by_precinct = CLIENT.votes_race_by_precinct(
            election_date=election_date, race_id=race_id, parish_value=parish_value
        )

        dump_json_to_blob(
            blob_name=(
                f"votes_precinct/_election_date={election_date}/_race={race_id}/"
                f"_parish={parish_value}/data.json"
            ),
            data=votes_race_by_precinct,
        )


def get_data_for_election_date(election_date: str):
    # Votes_Multiparish
    votes_multiparish = CLIENT.votes_multiparish(election_date=election_date)

    dump_json_to_blob(
        blob_name=f"votes_multiparish/_election_date={election_date}/data.json",
        data=votes_multiparish,
    )

    # ParishesInElection
    parishes_in_election = CLIENT.parishes_in_election(election_date=election_date)

    dump_json_to_blob(
        blob_name=f"parishes_in_election/_election_date={election_date}/data.json",
        data=parishes_in_election,
    )

    # get all parish values
    parish_values = sorted(
        [
            parish["ParishValue"]
            for parish in parishes_in_election["ParishesInElection"]["Parish"]
        ]
    )

    # RacesCandidates_Multiparish
    races_candidates_multiparish = CLIENT.races_candidates_multiparish(
        election_date=election_date
    )

    dump_json_to_blob(
        blob_name=f"races_candidates/_election_date={election_date}/_level=multiparish/_parish=all/data.json",
        data=races_candidates_multiparish,
    )

    # get all multiparish race ids
    multiparish_race_ids = sorted(
        [race["ID"] for race in races_candidates_multiparish["Races"]["Race"]]
    )

    # multiparish race votes
    for race_id in multiparish_race_ids:
        get_multiparish_race_data(election_date=election_date, race_id=race_id)

    # parish-specific race votes
    for parish_value in parish_values:
        get_parish_race_data(election_date=election_date, parish_value=parish_value)

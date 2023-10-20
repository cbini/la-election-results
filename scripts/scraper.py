import json
import os

import google.auth
import pendulum
from google.cloud import storage

from la_election_results.client import ElectionResultsClient


def get_data_for_election_date(
    client: ElectionResultsClient, bucket: storage.Bucket, election_date: str
):
    # ParishesInElection
    blob = bucket.blob(
        blob_name=f"parishes_in_election/_election_date={election_date}/data.json"
    )
    blob.upload_from_string(
        data=json.dumps(obj=client.parishes_in_election(election_date=election_date))
    )
    print(f"\tSaved to {blob.public_url}...")

    # RacesCandidates_Multiparish
    blob = bucket.blob(
        blob_name=(
            f"races_candidates/_election_date={election_date}/"
            "_level=multiparish/_parish=all/data.json"
        )
    )
    blob.upload_from_string(
        data=json.dumps(
            obj=client.races_candidates_multiparish(election_date=election_date)
        )
    )
    print(f"\tSaved to {blob.public_url}...")

    # Votes_Multiparish
    votes_multiparish_data = client.votes_multiparish(election_date=election_date)
    blob = bucket.blob(
        blob_name=f"votes_multiparish/_election_date={election_date}/data.json"
    )
    blob.upload_from_string(data=json.dumps(obj=votes_multiparish_data))
    print(f"\tSaved to {blob.public_url}...")

    # instantiate parish_values for later
    parish_values = set()

    # ensure races is list
    races = votes_multiparish_data["Races"].get("Race", [])
    if not isinstance(races, list):
        races = [races]

    for race in races:
        race_id = race["ID"]

        # VotesRaceByParish
        votes_race_by_parish_data = client.votes_race_by_parish(
            election_date=election_date, race_id=race_id
        )
        blob = bucket.blob(
            blob_name=(
                f"votes_race_parish/_election_date={election_date}/"
                f"_race={race_id}/data.json"
            )
        )
        blob.upload_from_string(data=json.dumps(obj=votes_race_by_parish_data))
        print(f"\tSaved to {blob.public_url}...")

        # ensure parishes is list
        parishes = votes_race_by_parish_data["Parishes"].get("Parish", [])
        if not isinstance(parishes, list):
            parishes = [parishes]

        for parish in parishes:
            parish_value = parish["ParishValue"]
            parish_values.add(parish_value)

            # VotesRaceByPrecinct
            blob = bucket.blob(
                blob_name=(
                    f"votes_precinct/_election_date={election_date}/"
                    f"_race={race_id}/_parish={parish_value}/data.json"
                )
            )
            blob.upload_from_string(
                data=json.dumps(
                    obj=client.votes_race_by_precinct(
                        election_date=election_date,
                        race_id=race_id,
                        parish_value=parish_value,
                    )
                )
            )
            print(f"\tSaved to {blob.public_url}...")

    for parish_value in parish_values:
        # RacesCandidates
        blob = bucket.blob(
            blob_name=(
                f"races_candidates/_election_date={election_date}/_level=parish/"
                f"_parish={parish_value}/data.json"
            )
        )
        blob.upload_from_string(
            data=json.dumps(
                obj=client.races_candidates_by_parish(
                    election_date=election_date, parish_value=parish_value
                )
            )
        )
        print(f"\tSaved to {blob.public_url}...")

        # VotesParish
        blob = bucket.blob(
            blob_name=(
                f"votes_parish_race/_election_date={election_date}/"
                f"_parish={parish_value}/data.json"
            )
        )
        blob.upload_from_string(
            data=json.dumps(
                obj=client.votes_parish(
                    election_date=election_date, parish_value=parish_value
                )
            )
        )
        print(f"\tSaved to {blob.public_url}...")


def main():
    client = ElectionResultsClient()

    # setup gcs
    credentials, project_id = google.auth.load_credentials_from_dict(
        info=json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
    )
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.get_bucket("la-election-results")

    # ElectionDates
    election_dates_data = client.election_dates()

    blob = bucket.blob(blob_name="election_dates/data.json")
    blob.upload_from_string(data=json.dumps(obj=election_dates_data))
    print(f"\tSaved to {blob.public_url}...")

    for date in election_dates_data["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        get_data_for_election_date(
            client=client, bucket=bucket, election_date=election_date_fmt
        )

        break


if __name__ == "__main__":
    main()

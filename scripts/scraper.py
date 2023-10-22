import json
import os

import google.auth
import pendulum
from google.cloud import storage

from la_election_results.client import ElectionResultsClient


def get_data_for_election_date(
    client: ElectionResultsClient, bucket: storage.Bucket, election_date: str
):
    # Votes_Multiparish
    blob = bucket.blob(
        blob_name=f"votes_multiparish/_election_date={election_date}/data.json"
    )
    blob.upload_from_string(
        data=json.dumps(obj=client.votes_multiparish(election_date=election_date))
    )
    print(f"Saved to {blob.public_url}...")

    # ParishesInElection
    parishes_in_election = client.parishes_in_election(election_date=election_date)

    blob = bucket.blob(
        blob_name=f"parishes_in_election/_election_date={election_date}/data.json"
    )
    blob.upload_from_string(data=json.dumps(obj=parishes_in_election))
    print(f"Saved to {blob.public_url}...")

    # create list of all parish values
    parish_values = sorted(
        [
            parish["ParishValue"]
            for parish in parishes_in_election["ParishesInElection"]["Parish"]
        ]
    )

    # RacesCandidates_Multiparish
    races_candidates_multiparish = client.races_candidates_multiparish(
        election_date=election_date
    )

    blob = bucket.blob(
        blob_name=(
            f"races_candidates/_election_date={election_date}/"
            "_level=multiparish/_parish=all/data.json"
        )
    )
    blob.upload_from_string(data=json.dumps(obj=races_candidates_multiparish))
    print(f"Saved to {blob.public_url}...")

    # multiparish race votes
    multiparish_race_ids = sorted(
        [race["ID"] for race in races_candidates_multiparish["Races"]["Race"]]
    )

    for race_id in multiparish_race_ids:
        # VotesRaceByParish
        blob = bucket.blob(
            blob_name=(
                f"votes_race_parish/_election_date={election_date}/"
                f"_race={race_id}/data.json"
            )
        )
        blob.upload_from_string(
            data=json.dumps(
                obj=client.votes_race_by_parish(
                    election_date=election_date, race_id=race_id
                )
            )
        )
        print(f"Saved to {blob.public_url}...")

        # VotesRaceByPrecinct
        for parish_value in parish_values:
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
            print(f"Saved to {blob.public_url}...")

    # parish-specific race votes
    for parish_value in parish_values:
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
        print(f"Saved to {blob.public_url}...")

        # RacesCandidates
        races_candidates_by_parish = client.races_candidates_by_parish(
            election_date=election_date, parish_value=parish_value
        )

        blob = bucket.blob(
            blob_name=(
                f"races_candidates/_election_date={election_date}/_level=parish/"
                f"_parish={parish_value}/data.json"
            )
        )
        blob.upload_from_string(data=json.dumps(obj=races_candidates_by_parish))
        print(f"Saved to {blob.public_url}...")

        # VotesRaceByPrecinct
        parish_race_ids = sorted(
            [race["ID"] for race in races_candidates_by_parish["Races"]["Race"]]
        )

        for race_id in parish_race_ids:
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
            print(f"Saved to {blob.public_url}...")


def main():
    client = ElectionResultsClient()

    # setup gcs
    credentials, project_id = google.auth.load_credentials_from_dict(
        info=json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
    )
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.get_bucket("la-election-results")

    # ElectionDates
    election_dates = client.election_dates()

    blob = bucket.blob(blob_name="election_dates/data.json")
    blob.upload_from_string(data=json.dumps(obj=election_dates))
    print(f"Saved to {blob.public_url}...")

    for date in election_dates["Dates"]["Date"]:
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

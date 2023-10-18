import json
import pathlib

import pendulum

from la_election_results.client import ElectionResultsClient


def get_data_for_election_date(
    client: ElectionResultsClient, data_dir: pathlib.Path, election_date: str
):
    # ParishesInElection
    filepath = (
        data_dir
        / "parishes_in_election"
        / f"_election_date={election_date}"
        / "data.json"
    )

    print(f"\tSaving to {filepath}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        obj=client.parishes_in_election(election_date=election_date),
        fp=filepath.open(mode="w"),
    )

    # RacesCandidates_Multiparish
    filepath = (
        data_dir
        / "races_candidates"
        / f"_election_date={election_date}"
        / "_level=multiparish"
        / "_parish=all"
        / "data.json"
    )

    print(f"\tSaving to {filepath}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        obj=client.races_candidates_multiparish(election_date=election_date),
        fp=filepath.open(mode="w"),
    )

    # Votes_Multiparish
    votes_multiparish_data = client.votes_multiparish(election_date=election_date)

    filepath = (
        data_dir / "votes_multiparish" / f"_election_date={election_date}" / "data.json"
    )

    print(f"\tSaving to {filepath}")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj=votes_multiparish_data, fp=filepath.open(mode="w"))

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

        filepath = (
            data_dir
            / "votes_race_parish"
            / f"_election_date={election_date}"
            / f"_race={race_id}"
            / "data.json"
        )

        print(f"\tSaving to {filepath}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        json.dump(obj=votes_race_by_parish_data, fp=filepath.open(mode="w"))

        # ensure parishes is list
        parishes = votes_race_by_parish_data["Parishes"].get("Parish", [])
        if not isinstance(parishes, list):
            parishes = [parishes]

        for parish in parishes:
            parish_value = parish["ParishValue"]
            parish_values.add(parish_value)

            # VotesRaceByPrecinct
            filepath = (
                data_dir
                / "votes_precinct"
                / f"_election_date={election_date}"
                / f"_race={race_id}"
                / f"_parish={parish_value}"
                / "data.json"
            )

            print(f"\tSaving to {filepath}")
            filepath.parent.mkdir(parents=True, exist_ok=True)
            json.dump(
                obj=client.votes_race_by_precinct(
                    election_date=election_date,
                    race_id=race_id,
                    parish_value=parish_value,
                ),
                fp=filepath.open(mode="w"),
            )

    for parish_value in parish_values:
        # RacesCandidates
        filepath = (
            data_dir
            / "races_candidates"
            / f"_election_date={election_date}"
            / "_level=parish"
            / f"_parish={parish_value}"
            / "data.json"
        )

        print(f"\tSaving to {filepath}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        json.dump(
            obj=client.races_candidates_by_parish(
                election_date=election_date, parish_value=parish_value
            ),
            fp=filepath.open(mode="w"),
        )

        # VotesParish
        filepath = (
            data_dir
            / "votes_parish_race"
            / f"_election_date={election_date}"
            / f"_parish={parish_value}"
            / "data.json"
        )

        print(f"\tSaving to {filepath}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        json.dump(
            obj=client.votes_parish(
                election_date=election_date, parish_value=parish_value
            ),
            fp=filepath.open(mode="w"),
        )


def main():
    client = ElectionResultsClient()
    data_dir = pathlib.Path("./.data")

    # ElectionDates
    election_dates_data = client.election_dates()

    filepath = data_dir / "election_dates" / "data.json"

    print(f"\tSaving to {filepath}...")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj=election_dates_data, fp=filepath.open(mode="w"))

    for date in election_dates_data["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        get_data_for_election_date(
            client=client, data_dir=data_dir, election_date=election_date_fmt
        )


if __name__ == "__main__":
    main()

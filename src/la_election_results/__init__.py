import json
import pathlib

import requests


class ElectionResultsClient(requests.Session):
    def __init__(self) -> None:
        super().__init__()

        self.base_url = (
            "https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data"
        )

    def get_response_json(self, **kwargs):
        response = self.get(url=self.base_url, params=kwargs)

        response.raise_for_status()

        return response.json()

    def election_dates(self):
        return self.get_response_json(blob="ElectionDates.htm")

    def parishes_in_election(self, election_date):
        return self.get_response_json(blob=f"{election_date}/ParishesInElection.htm")

    def races_candidates_multiparish(self, election_date):
        return self.get_response_json(
            blob=f"{election_date}/RacesCandidates_Multiparish.htm"
        )

    def votes_multiparish(self, election_date):
        return self.get_response_json(blob=f"{election_date}/Votes_Multiparish.htm")

    def votes_race_by_parish(self, election_date, race_id):
        return self.get_response_json(
            blob=f"{election_date}/VotesRaceByParish/Votes_{race_id}.htm"
        )

    def races_candidates_by_parish(self, election_date, parish_value):
        return self.get_response_json(
            blob=f"{election_date}/RacesCandidates/ByParish_{parish_value}.htm"
        )

    def votes_parish(self, election_date, parish_value):
        return self.get_response_json(
            blob=f"{election_date}/VotesParish/Votes_{parish_value}.htm"
        )

    def votes_race_by_precinct(self, election_date, race_id, parish_value):
        return self.get_response_json(
            blob=(
                f"{election_date}/VotesRaceByPrecinct/"
                f"Votes_{race_id}_{parish_value}.htm"
            )
        )


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

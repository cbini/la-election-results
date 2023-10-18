import json
import pathlib

import pendulum
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


def save(filepath, data):
    print(f"\tSaving to {filepath}...")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj=data, fp=filepath.open(mode="w"))


def foo(client: ElectionResultsClient, data_dir: pathlib.Path, election_date: str):
    # ParishesInElection
    save(
        filepath=(
            data_dir
            / "parishes_in_election"
            / f"_election_date={election_date}"
            / "data.json"
        ),
        data=client.parishes_in_election(),
    )

    # RacesCandidates_Multiparish
    save(
        filepath=(
            data_dir
            / "races_candidates"
            / f"_election_date={election_date}"
            / "_level=multiparish"
            / "_parish=all"
            / "data.json"
        ),
        data=client.races_candidates_multiparish(),
    )

    # Votes_Multiparish
    votes_multiparish_data = download_blob_data(
        filepath=(
            data_dir
            / "votes"
            / f"_election_date={election_date}"
            / "_level=multiparish"
            / "_race=all"
            / "_parish=all"
            / "data.json"
        ),
        blob=f"{election_date}/Votes_Multiparish.htm",
    )

    # instantiate parish_values for later
    parish_values = set()

    # ensure races is list
    races = votes_multiparish_data["Races"].get("Race", [])
    if not isinstance(races, list):
        races = [races]

    for race in races:
        race_id = race["ID"]

        # VotesRaceByParish/Votes_{RaceID}
        votes_race_by_parish_data = download_blob_data(
            filepath=(
                data_dir
                / "votes"
                / f"_election_date={election_date}"
                / "_level=parish"
                / f"_race={race_id}"
                / "_parish=all"
                / "data.json"
            ),
            blob=f"{election_date}/VotesRaceByParish/Votes_{race_id}.htm",
        )

        # ensure parishes is list
        parishes = votes_race_by_parish_data["Parishes"].get("Parish", [])
        if not isinstance(parishes, list):
            parishes = [parishes]

        for parish in parishes:
            parish_value = parish["ParishValue"]
            parish_values.add(parish_value)

            # {ElectionDate}/VotesRaceByPrecinct/Votes_{RaceID}_{ParishValue}
            download_blob_data(
                filepath=(
                    data_dir
                    / "votes"
                    / f"_election_date={election_date}"
                    / "_level=precinct"
                    / f"_race={race_id}"
                    / f"_parish={parish_value}"
                    / "data.json"
                ),
                blob=(
                    f"{election_date}/VotesRaceByPrecinct/"
                    f"Votes_{race_id}_{parish_value}.htm"
                ),
            )

    for parish_value in parish_values:
        # RacesCandidates/ByParish_{ParishValue}
        download_blob_data(
            filepath=(
                data_dir
                / "races_candidates"
                / f"_election_date={election_date}"
                / "_level=parish"
                / f"_parish={parish_value}"
                / "data.json"
            ),
            blob=f"{election_date}/RacesCandidates/ByParish_{parish_value}.htm",
        )

        # VotesParish/Votes_{ParishValue}
        download_blob_data(
            filepath=(
                data_dir
                / "votes"
                / f"_election_date={election_date}"
                / "_level=parish"
                / "_race=all"
                / f"_parish={parish_value}"
                / "data.json"
            ),
            blob=f"{election_date}/VotesParish/Votes_{parish_value}.htm",
        )


def main():
    client = ElectionResultsClient()
    data_dir = pathlib.Path("./data")

    # ElectionDates
    election_dates_data = client.election_dates()
    save(filepath=data_dir / "election_dates" / "data.json", blob=election_dates_data)

    for date in election_dates_data["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        # ParishesInElection
        download_blob_data(
            filepath=(
                data_dir
                / "parishes_in_election"
                / f"_election_date={election_date_fmt}"
                / "data.json"
            ),
            blob=f"{election_date_fmt}/ParishesInElection.htm",
        )

        # RacesCandidates_Multiparish
        download_blob_data(
            filepath=(
                data_dir
                / "races_candidates"
                / f"_election_date={election_date_fmt}"
                / "_level=multiparish"
                / "_parish=all"
                / "data.json"
            ),
            blob=f"{election_date_fmt}/RacesCandidates_Multiparish.htm",
        )

        # Votes_Multiparish
        votes_multiparish_data = download_blob_data(
            filepath=(
                data_dir
                / "votes"
                / f"_election_date={election_date_fmt}"
                / "_level=multiparish"
                / "_race=all"
                / "_parish=all"
                / "data.json"
            ),
            blob=f"{election_date_fmt}/Votes_Multiparish.htm",
        )

        # instantiate parish_values for later
        parish_values = set()

        # ensure races is list
        races = votes_multiparish_data["Races"].get("Race", [])
        if not isinstance(races, list):
            races = [races]

        for race in races:
            race_id = race["ID"]

            # VotesRaceByParish/Votes_{RaceID}
            votes_race_by_parish_data = download_blob_data(
                filepath=(
                    data_dir
                    / "votes"
                    / f"_election_date={election_date_fmt}"
                    / "_level=parish"
                    / f"_race={race_id}"
                    / "_parish=all"
                    / "data.json"
                ),
                blob=f"{election_date_fmt}/VotesRaceByParish/Votes_{race_id}.htm",
            )

            # ensure parishes is list
            parishes = votes_race_by_parish_data["Parishes"].get("Parish", [])
            if not isinstance(parishes, list):
                parishes = [parishes]

            for parish in parishes:
                parish_value = parish["ParishValue"]
                parish_values.add(parish_value)

                # {ElectionDate}/VotesRaceByPrecinct/Votes_{RaceID}_{ParishValue}
                download_blob_data(
                    filepath=(
                        data_dir
                        / "votes"
                        / f"_election_date={election_date_fmt}"
                        / "_level=precinct"
                        / f"_race={race_id}"
                        / f"_parish={parish_value}"
                        / "data.json"
                    ),
                    blob=(
                        f"{election_date_fmt}/VotesRaceByPrecinct/"
                        f"Votes_{race_id}_{parish_value}.htm"
                    ),
                )

        for parish_value in parish_values:
            # RacesCandidates/ByParish_{ParishValue}
            download_blob_data(
                filepath=(
                    data_dir
                    / "races_candidates"
                    / f"_election_date={election_date_fmt}"
                    / "_level=parish"
                    / f"_parish={parish_value}"
                    / "data.json"
                ),
                blob=f"{election_date_fmt}/RacesCandidates/ByParish_{parish_value}.htm",
            )

            # VotesParish/Votes_{ParishValue}
            download_blob_data(
                filepath=(
                    data_dir
                    / "votes"
                    / f"_election_date={election_date_fmt}"
                    / "_level=parish"
                    / "_race=all"
                    / f"_parish={parish_value}"
                    / "data.json"
                ),
                blob=f"{election_date_fmt}/VotesParish/Votes_{parish_value}.htm",
            )


if __name__ == "__main__":
    main()

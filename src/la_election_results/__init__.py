import json
import pathlib

import pendulum
import requests


def foo(data_dir, asset_name, election_date_fmt, base_url):
    asset_filepath = data_dir / asset_name / f"{election_date_fmt}.json"
    asset_filepath.parent.mkdir(parents=True, exist_ok=True)

    asset_response = requests.get(
        url=base_url, params={"blob": f"{election_date_fmt}/{asset_name}.htm"}
    )

    json.dump(obj=asset_response.json(), fp=asset_filepath.open(mode="w"))


def main():
    base_url = "https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data"
    data_dir = pathlib.Path("./data")

    # get all election dates
    election_dates_filepath = data_dir / "ElectionDates" / "election_dates.json"
    election_dates_filepath.parent.mkdir(parents=True, exist_ok=True)

    election_dates_response = requests.get(
        url=base_url, params={"blob": "ElectionDates.htm"}
    )

    election_dates_data = election_dates_response.json()
    json.dump(obj=election_dates_data, fp=election_dates_filepath.open(mode="w"))

    for date in election_dates_data["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        # RacesCandidates_Multiparish
        asset_name = "RacesCandidates_Multiparish"

        asset_filepath = data_dir / asset_name / f"{election_date_fmt}.json"
        asset_filepath.parent.mkdir(parents=True, exist_ok=True)

        asset_response = requests.get(
            url=base_url, params={"blob": f"{election_date_fmt}/{asset_name}.htm"}
        )

        json.dump(obj=asset_response.json(), fp=asset_filepath.open(mode="w"))

        # Votes_Multiparish
        asset_name = "Votes_Multiparish"

        asset_filepath = data_dir / asset_name / f"{election_date_fmt}.json"
        asset_filepath.parent.mkdir(parents=True, exist_ok=True)

        asset_response = requests.get(
            url=base_url, params={"blob": f"{election_date_fmt}/{asset_name}.htm"}
        )

        votes_multiparish_data = asset_response.json()
        json.dump(obj=votes_multiparish_data, fp=asset_filepath.open(mode="w"))

        # VotesRaceByParish
        asset_name = "VotesRaceByParish"
        for race in votes_multiparish_data["Races"]["Race"]:
            race_id = race["ID"]

            asset_filepath = (
                data_dir / asset_name / f"{election_date_fmt}_{race_id}.json"
            )
            asset_filepath.parent.mkdir(parents=True, exist_ok=True)

            asset_response = requests.get(
                url=base_url,
                params={
                    "blob": f"{election_date_fmt}/{asset_name}/Votes_{race_id}.htm"
                },
            )

            votes_race_by_parish_data = asset_response.json()
            json.dump(obj=votes_race_by_parish_data, fp=asset_filepath.open(mode="w"))


if __name__ == "__main__":
    main()

import json
import pathlib

import pendulum
import requests


def get_response_json(url, **kwargs):
    response = requests.get(url=url, params=kwargs)

    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)


def main():
    base_url = "https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data"
    data_dir = pathlib.Path("./data")

    # ElectionDates
    election_dates_filepath = data_dir / "ElectionDates" / "election_dates.json"
    election_dates_filepath.parent.mkdir(parents=True, exist_ok=True)

    election_dates_data = get_response_json(url=base_url, blob="ElectionDates.htm")

    json.dump(obj=election_dates_data, fp=election_dates_filepath.open(mode="w"))

    for date in election_dates_data["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        # Votes_Multiparish
        asset_filepath = data_dir / "Votes_Multiparish" / f"{election_date_fmt}.json"
        asset_filepath.parent.mkdir(parents=True, exist_ok=True)

        votes_multiparish_data = get_response_json(
            url=base_url, blob=f"{election_date_fmt}/Votes_Multiparish.htm"
        )

        json.dump(obj=votes_multiparish_data, fp=asset_filepath.open(mode="w"))

        # ParishesInElection
        asset_filepath = data_dir / "ParishesInElection" / f"{election_date_fmt}.json"
        asset_filepath.parent.mkdir(parents=True, exist_ok=True)

        parishes_in_election_data = get_response_json(
            url=base_url, blob=f"{election_date_fmt}/ParishesInElection.htm"
        )

        json.dump(obj=parishes_in_election_data, fp=asset_filepath.open(mode="w"))

        # RacesCandidates_Multiparish
        asset_filepath = (
            data_dir / "RacesCandidates_Multiparish" / f"{election_date_fmt}.json"
        )
        asset_filepath.parent.mkdir(parents=True, exist_ok=True)

        races_candidates_multiparish_data = get_response_json(
            url=base_url, blob=f"{election_date_fmt}/RacesCandidates_Multiparish.htm"
        )

        json.dump(
            obj=races_candidates_multiparish_data, fp=asset_filepath.open(mode="w")
        )

        # RacesCandidates/ByParish_{parish_id}.htm

        # VotesParish/Votes_{parish_id}.htm

        # VotesRaceByParish
        asset_name = "VotesRaceByParish"

        races = votes_multiparish_data["Races"].get("Race", [])
        if not isinstance(races, list):
            races = [races]

        for race in races:
            race_id = race["ID"]

            asset_filepath = (
                data_dir / asset_name / election_date_fmt / f"{race_id}.json"
            )
            asset_filepath.parent.mkdir(parents=True, exist_ok=True)

            votes_race_by_parish_data = get_response_json(
                url=base_url,
                blob=f"{election_date_fmt}/{asset_name}/Votes_{race_id}.htm",
            )

            json.dump(obj=votes_race_by_parish_data, fp=asset_filepath.open(mode="w"))


if __name__ == "__main__":
    main()

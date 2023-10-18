import json
import pathlib

import pendulum

from la_election_results import ElectionResultsClient, get_data_for_election_date


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

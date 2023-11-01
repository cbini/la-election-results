import argparse

from la_election_results.functions import (
    CLIENT,
    dump_json_to_blob,
    get_data_for_election_date,
)


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("election_date", help="YYYYMMDD")
    args = argument_parser.parse_args()

    # ElectionDates
    dump_json_to_blob(
        blob_name="election_dates/data.json", data=CLIENT.election_dates()
    )

    get_data_for_election_date(election_date=args.election_date)


if __name__ == "__main__":
    main()

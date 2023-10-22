import pendulum

from la_election_results.client import ElectionResultsClient


def get_data_for_election_date(client: ElectionResultsClient, election_date: str):
    # ParishesInElection
    parishes_in_election = client.parishes_in_election(election_date=election_date)

    # create set of all parish values
    parish_values = set()
    for parish in parishes_in_election["ParishesInElection"]["Parish"]:
        parish_values.add(parish["ParishValue"])

    # RacesCandidates_Multiparish
    races_candidates_multiparish = client.races_candidates_multiparish(
        election_date=election_date
    )

    # add multiparish race_ids to set
    race_ids = set()
    for race in races_candidates_multiparish["Races"]["Race"]:
        race_ids.add(race["ID"])

    for parish_value in parish_values:
        # RacesCandidates
        races_candidates_by_parish = client.races_candidates_by_parish(
            election_date=election_date, parish_value=parish_value
        )

        # add parish race_ids to set
        for race in races_candidates_by_parish["Races"]["Race"]:
            race_ids.add(race["ID"])

    print(len(race_ids))
    print(race_ids)
    print(len(parish_values))
    print(parish_values)


def main():
    client = ElectionResultsClient()

    # ElectionDates
    election_dates = client.election_dates()

    for date in election_dates["Dates"]["Date"]:
        election_date = pendulum.from_format(
            string=date["ElectionDate"], fmt="MM/DD/YYYY"
        )
        election_date_fmt = election_date.format(fmt="YYYYMMDD")
        print(election_date_fmt)

        get_data_for_election_date(client=client, election_date=election_date_fmt)

        break


if __name__ == "__main__":
    main()

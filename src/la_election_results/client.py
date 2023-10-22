import requests
from tenacity import TryAgain, retry, wait_exponential


class ElectionResultsClient(requests.Session):
    def __init__(self) -> None:
        super().__init__()

        self.base_url = (
            "https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data"
        )

    # @retry(wait=wait_exponential(min=1, max=10))
    def get_response_json(self, **kwargs):
        response = self.get(url=self.base_url, params=kwargs)

        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if response.status_code == 403:
                print(e)
                print("Retrying")
                raise TryAgain from e
            else:
                raise e

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

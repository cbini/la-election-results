# API Calls

- ElectionDates

- {Election Date}/Votes_Multiparish
- {Election Date}/ParishesInElection
- {Election Date}/RacesCandidates_Multiparish

- {Election Date}/RacesCandidates/ByParish\_{Parish ID}
- {Election Date}/VotesParish/Votes\_{Parish ID}

- {Election Date}/VotesRaceByParish/Votes\_{Race ID}
- {Election Date}/VotesRaceByPrecinct/Votes\_{Race ID}\_{Parish ID}

## By Page

### Top-level

- ElectionDates

### Election Date

- RacesCandidates_Multiparish

#### Statewide Races

- Votes_Multiparish

##### Statewide > Results by Parish

- VotesRaceByParish/Votes\_{Race ID}

###### Statewide > Parish > Results by Precinct

- VotesRaceByPrecinct/Votes\_{Race ID}\_{Parish ID}
- RacesCandidates/ByParish\_{Parish ID}

#### LA Legislature Races

- Votes_Multiparish

##### Legislature > Results by Parish

- VotesRaceByParish/Votes\_{Race ID}

###### Legislature > Parish > Results by Precinct

- VotesRaceByPrecinct/Votes\_{Race ID}\_{Parish ID}
- RacesCandidates/ByParish\_{Parish ID}

#### Multiparish Races

- Votes_Multiparish

##### Multiparish > Results by Parish

- VotesRaceByParish/Votes\_{Race ID}

###### Multiparish > Parish > Results by Precinct

- VotesRaceByPrecinct/Votes\_{Race ID}\_{Parish ID}
- RacesCandidates/ByParish\_{Parish ID}

#### Parish Races

- ParishesInElection

##### Parish > Results by Parish

- VotesParish/Votes\_{Parish ID}
- RacesCandidates/ByParish\_{Parish ID}

###### Parish > Parish > Results by Precinct

- VotesRaceByPrecinct/Votes\_{Race ID}\_{Parish ID}

/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import { Species } from '../../models/Species'
import * as React from 'react'
import { ToLID } from '../../models/ToLID';
import { Specimen } from '../../models/Specimen'
import SearchResultType from '../../models/SearchResultType';
import { StyledSearchResultsTableTab } from './SearchResultsTableTabStyled';
import SearchResultsToLID from './SearchResultsToLID';
import SearchResultsSpecimen from './SearchResultsSpecimen';
import SearchResultsSpecies from './SearchResultsSpecies';

interface Props {
  searchResults: [ToLID | Specimen | Species, SearchResultType][];
}

const SearchResultsTableTab: React.FunctionComponent<Props> = ({
  searchResults,
}: Props) => {
  const getTolIdRender = (tolId: ToLID) => (
    <SearchResultsToLID
        tolid={tolId}
        key={`ToLID-${tolId.tolId}`}
    />
  );

  const getSpecimenRender = (specimen: Specimen) => (
    <SearchResultsSpecimen
        specimen={specimen}
        key={`Specimen-${specimen.specimenId}`}
    />
  );

  const getSpeciesRender = (species: Species) => (
    <SearchResultsSpecies
        species={species}
        key={`Species-${species.taxonomyId}`}
    />
  );

  const getSearchResultView = (searchResultPair: [ToLID | Specimen | Species, SearchResultType]) => {
    const searchResultType = searchResultPair[1];
    const searchResult = searchResultPair[0];
    switch (searchResultType) {
        case SearchResultType.ToLID:
            return getTolIdRender(searchResult as ToLID);
        case SearchResultType.Specimen:
            return getSpecimenRender(searchResult as Specimen);
        case SearchResultType.Species:
            return getSpeciesRender(searchResult as Species);
    }
  }

  return (
    <StyledSearchResultsTableTab>
        {
            searchResults.map(searchResult => getSearchResultView(searchResult))
        }
    </StyledSearchResultsTableTab> 
  )
}

export default SearchResultsTableTab;

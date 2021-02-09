import React from 'react';
import { Species } from '../models/Species'
import { StyledSearchResultsSpecies } from './SearchResultsSpeciesStyled';

interface SearchResultsSpeciesProps {
  species: Species;
}

const SearchResultsSpecies: React.FunctionComponent<SearchResultsSpeciesProps> = ({
  species,
}: SearchResultsSpeciesProps) => {
  
  return (
    <StyledSearchResultsSpecies>
      <div className="row">
        <div className="col-3">
            {species.prefix}
        </div>
        <div className="col-9">
        {species.taxonomyId}<br/>
        {species.scientificName}<br/>
        </div>
      </div>
    </StyledSearchResultsSpecies>
  );
};

export default SearchResultsSpecies;

import React from 'react';
import { ToLID } from '../models/ToLID'
import { StyledSearchResultsToLID } from './SearchResultsToLIDStyled';

interface SearchResultsToLIDProps {
  tolid: ToLID;
}

const SearchResultsToLID: React.FunctionComponent<SearchResultsToLIDProps> = ({
  tolid,
}: SearchResultsToLIDProps) => {
  
  return (
    <StyledSearchResultsToLID>
      <div className="row">
        <div className="col-3">
            {tolid.tolId}
        </div>
        <div className="col-9">
        {tolid.species.taxonomyId}<br/>
        {tolid.species.scientificName}<br/>
        Specimen ID: {tolid.specimen.specimenId}<br/>
        </div>
      </div>
    </StyledSearchResultsToLID>
  );
};

export default SearchResultsToLID;

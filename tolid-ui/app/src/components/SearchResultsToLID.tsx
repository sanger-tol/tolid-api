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
        <div className="col-4">
            <span className="type">ToLID</span><br/>
            <span className="identifier">{tolid.tolId}</span>
        </div>
        <div className="col-8">
            <span className="label">Taxonomy ID:</span> {tolid.species.taxonomyId} <a href={"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=" +tolid.species.taxonomyId} className="btn btn-primary btn-sm">NCBI</a><br/>
            <span className="label">Scientific name:</span> {tolid.species.scientificName}<br/>
            <span className="label">Specimen ID:</span> {tolid.specimen.specimenId}<br/>
        </div>
      </div>
    </StyledSearchResultsToLID>
  );
};

export default SearchResultsToLID;

import React from 'react';
import { Species } from '../models/Species'
import { ToLID } from '../models/ToLID'
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
        <div className="col-4">
          <span className="type">Species</span><br/>
          <span className="identifier">{species.prefix}</span>
        </div>
        <div className="col-8">
          <span className="label">Taxonomy ID:</span> {species.taxonomyId} <a href={"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=" +species.taxonomyId} className="btn btn-primary btn-sm">NCBI</a><br/>
          <span className="label">Scientific name:</span> {species.scientificName}<br/>
          <span className="label">ToLIDs:</span><ul>
            {species.tolIds.map((item: ToLID) => (
            <li key={item.tolId}>{item.tolId}: {item.specimen.specimenId}</li>
            ))}
          </ul>
        </div>
      </div>
    </StyledSearchResultsSpecies>
  );
};

export default SearchResultsSpecies;

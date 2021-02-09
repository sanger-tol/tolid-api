import React from 'react';
import { Specimen } from '../models/Specimen'
import { ToLID } from '../models/ToLID'
import { StyledSearchResultsSpecimen } from './SearchResultsSpecimenStyled';

interface SearchResultsSpecimenProps {
  specimen: Specimen;
}

const SearchResultsSpecimen: React.FunctionComponent<SearchResultsSpecimenProps> = ({
  specimen,
}: SearchResultsSpecimenProps) => {
  
  return (
    <StyledSearchResultsSpecimen>
      <div className="row">
        <div className="col-3">
            {specimen.specimenId}
        </div>
        <div className="col-9">
          <ul>
            {specimen.tolIds.map((item: ToLID) => (
                <li key={item.tolId}>{item.tolId}: {item.species.taxonomyId}</li>
            ))}
          </ul>
        </div>
      </div>
    </StyledSearchResultsSpecimen>
  );
};

export default SearchResultsSpecimen;

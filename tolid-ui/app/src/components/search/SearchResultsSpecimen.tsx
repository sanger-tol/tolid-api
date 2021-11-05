/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React from 'react';
import { Row, Col } from "react-bootstrap";
import { Specimen } from '../../models/Specimen';
import { ToLID } from '../../models/ToLID';
import { StyledSearchResultsSpecimen } from './SearchResultsSpecimenStyled';

interface SearchResultsSpecimenProps {
  specimen: Specimen;
}

const SearchResultsSpecimen: React.FunctionComponent<SearchResultsSpecimenProps> = ({
  specimen,
}: SearchResultsSpecimenProps) => {
  
  return (
    <StyledSearchResultsSpecimen>
      <Row>
        <Col sm={4}>
          <span className="type">Specimen</span><br/>
          <span className="identifier">{specimen.specimenId}</span>
        </Col>
        <Col sm={8} className="mb-5">
          <span className="label">ToLIDs:</span>
          <ul>
            {specimen.tolIds.map((item: ToLID) => (
                <li key={item.tolId}>{item.tolId}: {item.species.scientificName} ({item.species.taxonomyId}) <a href={"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=" +item.species.taxonomyId} className="btn btn-primary btn-sm">NCBI</a></li>
            ))}
          </ul>
        </Col>
      </Row>
    </StyledSearchResultsSpecimen>
  );
};

export default SearchResultsSpecimen;

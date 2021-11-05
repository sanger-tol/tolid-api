{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import React from 'react';
import { Row, Col } from "react-bootstrap";
import { Species } from '../../models/Species';
import { ToLID } from '../../models/ToLID';
import { StyledSearchResultsSpecies } from './SearchResultsSpeciesStyled';

interface SearchResultsSpeciesProps {
  species: Species;
}

const SearchResultsSpecies: React.FunctionComponent<SearchResultsSpeciesProps> = ({
  species,
}: SearchResultsSpeciesProps) => {
  
  return (
    <StyledSearchResultsSpecies>
      <Row>
        <Col sm={4}>
          <span className="type">Species</span><br/>
          <span className="identifier">{species.prefix}</span>
        </Col>
        <Col sm={8} className="mb-5">
          <span className="label">Taxonomy ID:</span> {species.taxonomyId} <a href={"https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=" +species.taxonomyId} className="btn btn-primary btn-sm">NCBI</a><br/>
          <span className="label">Scientific name:</span> {species.scientificName}<br/>
          <span className="label">ToLIDs:</span>
            {species.tolIds.length > 0 && <ul>
              {species.tolIds.map((item: ToLID) => (
                <li key={item.tolId}>{item.tolId}: {item.specimen.specimenId}</li>
                ))
              }
            </ul>}
            {species.tolIds.length === 0 && <span> None assigned</span>}
        </Col>
      </Row>
    </StyledSearchResultsSpecies>
  );
};

export default SearchResultsSpecies;

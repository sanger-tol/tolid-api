{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import React from "react";
import { Container, Col, Row } from "react-bootstrap";
import SearchResults from "../components/search/SearchResults"

function Search() {
  return (
    <div className="search">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">Search</h1>
          </div>
        </div>
        <div className="bg-circle-1 bg-circle"></div>
        <div className="bg-circle-2 bg-circle"></div>
        <div className="bg-circle-3 bg-circle"></div>
        <div className="bg-circle-4 bg-circle"></div>
      </header>
      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12" className="order-lg-1">
              <SearchResults/>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
}

export default Search;
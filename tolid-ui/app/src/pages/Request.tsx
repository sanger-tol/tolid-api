/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React from "react";
import RequestForm from "../components/request/RequestForm"
import { Container, Row, Col } from "react-bootstrap"

function Request() {
  return (
    <div className="request">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <Container>
            <h1 className="masthead-heading mb-0">Request a ToLID</h1>
          </Container>
        </div>
        <div className="bg-circle-1 bg-circle"></div>
        <div className="bg-circle-2 bg-circle"></div>
        <div className="bg-circle-3 bg-circle"></div>
        <div className="bg-circle-4 bg-circle"></div>
      </header>
      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12">
                <RequestForm/>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
}

export default Request;
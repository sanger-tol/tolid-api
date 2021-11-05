{/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/}

import React from "react";
import { Container, Row, Col } from "react-bootstrap"; 
import PrefixTable from "../components/prefixTable/PrefixTable";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <Container>
            <h1 className="masthead-heading mb-0">ToLID</h1>
            <h2 className="masthead-subheading mb-0">Tree of Life Identifiers</h2>
            <a href="api/v2/ui/" className="btn btn-primary btn-xl rounded-pill mt-5">Use the API</a>
            <Link to="/search" className="btn btn-primary btn-xl rounded-pill mt-5">Search</Link>
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
            <Col lg="12" className="order-lg-1">
              <div className="p-5">
                <h2 className="display-4">What are ToLIDs?</h2>
                <p>A complete ToLID is a unique identifier for an individuum of a species sampled for genome sequencing and consists of</p>
                <ul>
                  <li>the ToLID prefix made up of
                    <ul>
                      <li>a lower case letter for the high level taxonomic rank and a lower case letter for the clade (see clade prefix assignments below). Only one letter is used for vertebrates (VGP legacy).</li>
                      <li>one upper, two lower case letters for genus</li>
                      <li>one upper, three lower case letters for species (one upper, two lower case for vertebrates, VGP legacy)</li>
                    </ul>
                  </li>
                  <li>a number to indicate the individual that was sampled. The number is assigned in order of request and does not represent any ranking.</li>
                </ul>
                <p>e.g. <strong>aRanTem1</strong> for the first sampled individual of Rana temporaria, <strong>xgPerPere3</strong> for the third sampled individual of Peregriana peregra</p>
                
                <p>For naming genome assemblies of samples, we recommend to use the full ToLID and add .&lt;version&gt;
                Examples:</p>
                <ul>
                  <li>fCotGob3.1 (first assembly version of the 3rd individual of Cottoperca gobio)</li>
                  <li>fAstCal1.2 (second assembly version of the first individual of Astatotilapia calliptera)</li>
                </ul>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12">
              <div className="p-5">
                <h2 className="display-4">Why do we need them?</h2>
                <p>ToLIDs add a unique, easy to communicate identifier that provides species recognition, differentiates between specimen of the same species and adds some taxonomic context.</p>
                <p>The <a href="https://www.earthbiogenome.org/">Earth BioGenome Project (EBP)</a> recommends that all samples to be sequenced are registered for a ToLID. This helps with your internal records, facilitates internal and external communication about the samples and helps the EBP tracking all sequencing projects.</p>
                <p>ToLIDs are not a competition or replacement for INSDC BioSample records which hold all the metadata associated with the sample. Every sample should have both.</p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12">
              <div className="p-5">
                <h2 className="display-4">How can I get one?</h2>
                <p>On this website is a self-service system to enable you to simply enter your sample’s taxonomy ID and any internal identifier (the latter so that we can spot it if you accidentally ask for a ToLID for the same sample again) and get a ToLID in return. Click on the Login button and log in using Elixir, then click on "Create". ToLIDs go through a manual acceptance process but we aim to create them within 48 hours of request.</p>
                <p>You can search for already assigned ToLIDs in the search box above. The API documentation for the ToLID database can be found <a href="/api/v2/ui">here</a>.</p>
                <p>Any problems, <a href="mailto:tolid-help@sanger.ac.uk">email us</a>.</p>
                </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section>
        <Container>
          <Row className="row align-items-center">
            <Col lg="12" className="order-lg-1">
              <div className="p-5">
                <h2 className="display-4">What if the species is missing in the ToLID database?</h2>
                <p>The ToLID database contains all British angiosperms (BotSocBritIsles), all valid British taxa with taxonomy (NHM) and all “species” with sequence in INSDC. If a species is not in the database yet we'll add it.</p>
                <p>A species needs to have a taxonomy ID before ToLIDs can be requested. If not present, these should be requested and obtained from taxonomyDB first before contacting us. Instructions can be found <a href="https://ena-docs.readthedocs.io/en/latest/faq/taxonomy_requests.html">here</a>.</p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12" className="order-lg-1">
              <div className="p-5">
                <h2 className="display-4">How did you make the ToLIDs?</h2>
                <p>The list of unique prefixes assigned to species in the ToLID API is maintained in <a href="https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming">GitLab repository</a>.</p>
                <p>In order to assign two-letter prefixes (the first part of a ToLID) to all life, we proposed a pragmatic hierarchical grouping with the first letter based on higher level groups and the second letter defining sub groups within them. For legacy reasons, vertebrates are prefixed with one letter only. Although standard high level names are used for many groups, these are at a variety of taxonomic ranks, and others designations involve clearly non-monophyletic groupings, including catch-all clusters such as for example "other-animal-phyla". This assignment achieves a practical and manageable grouping that has proven robust to working through large lists of species from multiple sources with often contradicting taxonomic data. The groups explicitly do not represent assertions about taxonomy in general or taxonomic assignment of individual species.</p>
                <PrefixTable/>
              </div>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
}

export default Home;
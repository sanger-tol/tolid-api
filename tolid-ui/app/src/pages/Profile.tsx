import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import UserToLIDsList from "../components/profile/UserToLIDsList";
import UserRequestsList from "../components/profile/UserRequestsList";

function Profile() {
  return (
    <div className="contact">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <Container>
            <h1 className="masthead-heading mb-0">Profile</h1>
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
              <div className="p-5">
                <h2>My ToLIDs</h2>
                <UserToLIDsList />
                <h2>My Requests</h2>
                <UserRequestsList />
              </div>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
}

export default Profile;
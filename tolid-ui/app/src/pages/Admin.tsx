import React from "react";
import RequestsList from "../components/requestsList/RequestsList"

function Admin() {
  return (
    <div className="request">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">ToLID admin</h1>
          </div>
        </div>
        <div className="bg-circle-1 bg-circle"></div>
        <div className="bg-circle-2 bg-circle"></div>
        <div className="bg-circle-3 bg-circle"></div>
        <div className="bg-circle-4 bg-circle"></div>
      </header>
      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12 order-lg-1">
                <h2>Pending requests</h2>
                <RequestsList/>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Admin;
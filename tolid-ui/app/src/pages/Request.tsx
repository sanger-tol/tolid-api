import React from "react";
import RequestForm from "../components/request/RequestForm"

function Request() {
  return (
    <div className="request">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">Request a ToLID</h1>
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
                <RequestForm/>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Request;
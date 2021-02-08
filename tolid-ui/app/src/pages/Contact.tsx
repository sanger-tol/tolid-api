import React from "react";

function Contact() {
  return (
    <div className="contact">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">Contact</h1>
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
            <div className="col-lg-12">
              <div className="p-5">
                <p>Please email us with any queries about ToLIDs or to request access to being able to create ToLIDs.
                  Our email address is <a href="mailto:tolid-help@sanger.ac.uk">tolid-help@sanger.ac.uk</a>.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Contact;
import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0">ToLID</h1>
            <h2 className="masthead-subheading mb-0">Tree of Life Identifiers</h2>
            <a href="api/v2/ui/" className="btn btn-primary btn-xl rounded-pill mt-5">Use the API</a>
            <Link to="/search" className="btn btn-primary btn-xl rounded-pill mt-5">Search</Link>
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
              <div className="p-5">
                <h2 className="display-4">What are ToLIDs?</h2>
                <p>A complete ToLID is a unique identifier for an individual sampled and consists of</p>
                <ul>
                  <li>the ToLID prefix is made up of
                    <ul>
                      <li>a lower case letter for the high level taxonomic rank and a lower case letter for the clade (see clade prefix assignments). Only one letter is used for vertebrates (VGP legacy).</li>
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
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12">
              <div className="p-5">
                <h2 className="display-4">How can I use them?</h2>
                <p>The best place to get started is the <a href="api/v2/ui/">API documentation</a>. To create ToLIDs, you'll need an API key from <a href="mailto:tolid-help@sanger.ac.uk">the ToLID team</a>. We are working towards making this a full web-based service, but for now, please email us.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12 order-lg-1">
              <div className="p-5">
                <h2 className="display-4">What if the species is missing in the ToLID database?</h2>
                <p>The ToLID database contains all British angiosperms (BotSocBritIsles), all valid British taxa with taxonomy (NHM) and all “species” with sequence in INSDC. If a species is not in the database, an error message will be returned by the API. Please <a href="mailto:tolid-help@sanger.ac.uk">contact us</a> and we'll add it. A species needs to have a taxon ID before ToLIDs can be requested. If not present, these should be requested and obtained from taxonomyDB first before contacting us.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-12 order-lg-1">
              <div className="p-5">
                <h2 className="display-4">Where can I find out more?</h2>
                <p>The list of prefixes assigned to species in the ToLID API is maintained in <a href="https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming">GitLab repository</a>.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
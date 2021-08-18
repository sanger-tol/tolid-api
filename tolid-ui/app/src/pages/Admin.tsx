import { useState } from "react";
import { Tab, Tabs } from "react-bootstrap";
import RequestsList from "../components/requestsList/RequestsList";
import AddSpecies from '../components/addSpecies/AddSpecies';

function Admin() {
  const [key, setKey] = useState('request');
  const [numSpeciesAdded, setNumSpeciesAdded] = useState(0);

  const openAddSpeciesTab = () => {
    setKey("add-species");
  }

  const updateRequestsList = () => {
    // increment the number of species added, to update the 
    // props of RequestList, and thus force a refresh
    setNumSpeciesAdded(numSpeciesAdded + 1);
  }

  return (
    <div id="admin-container">
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
      <div className="container mt-2">
        <Tabs defaultActiveKey="request"
              id="admin-tab"
              className="ml-auto"
              activeKey={key}
              onSelect={(k) => setKey(k ?? 'request')}>
          <Tab eventKey="request"  title="Pending Requests">
            <section>
              <div className="container">
                <div className="row align-items-center">
                  <div className="col-lg-12 order-lg-1 mt-3">
                      <h2>Pending requests</h2>
                      <RequestsList openAddSpeciesTab={openAddSpeciesTab} numSpeciesAdded={numSpeciesAdded}/>
                  </div>
                </div>
              </div>
            </section>
          </Tab>
          <Tab eventKey="add-species" title="Add Species">
            <section>
              <div className="container">
                <div className="row align-items-center">
                  <div className="col-lg-12 order-lg-1 mt-3">
                      <h2>Add Species</h2>
                      <AddSpecies updateRequestsList={updateRequestsList}/>
                  </div>
                </div>
              </div>
            </section>
          </Tab>
        </Tabs>
      </div>
    </div>
  );
}

export default Admin;
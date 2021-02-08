import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Navigation, Footer, Home, Search, Contact } from "./pages";
import 'bootstrap/dist/css/bootstrap.min.css';
import './scss/one-page-wonder.scss';

function App() {
  return (
    <div className="App">
      <Router>
        <Navigation />
        <Switch>
          <Route path="/" exact component={() => <Home />} />
          <Route path="/search" exact component={() => <Search />} />
          <Route path="/contact" exact component={() => <Contact />} />
        </Switch>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
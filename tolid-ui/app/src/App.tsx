import React, { useState }  from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Navigation, Footer, Home, Search, Request, Admin, Profile, Login, Callback } from "./pages";
import { getTokenFromLocalStorage,
  getUserFromLocalStorage, 
  tokenHasExpired} from './services/localStorage/localStorageService';
import { AuthProvider } from './contexts/auth.context';
import { Redirect } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import './scss/one-page-wonder.scss';


function App() {
  const [token, setToken] = useState(getTokenFromLocalStorage);
  const [user, setUser] = useState(getUserFromLocalStorage);

    return (
    <div className="App">
      <AuthProvider
        value={{
          token,
          setToken,
          user,
          setUser,
        }}
      >
        <Router>
          <Navigation />
          <Switch>
            <Route path="/" exact component={() => <Home />} />
            <Route path="/search" exact><Search /></Route>
            <Route path="/request" exact>{(token && !tokenHasExpired(token)) ? <Request /> : <Redirect to="/" />}</Route>
            <Route path="/admin" exact>{(token && !tokenHasExpired(token)) ? <Admin /> : <Redirect to="/" />}</Route>
            <Route path="/profile" exact>{(token && !tokenHasExpired(token)) ? <Profile /> : <Redirect to="/" />}</Route>
            <Route path="/login" exact><Login /></Route>
            <Route path="/callback" exact><Callback /></Route>
          </Switch>
          <Footer />
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
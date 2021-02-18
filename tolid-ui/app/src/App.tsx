import React, { useState }  from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Navigation, Footer, Home, Search, Request, Admin, Profile, Login, Callback } from "./pages";
import { getTokenFromLocalStorage } from './services/localStorage/localStorageService';
import { AuthProvider } from './contexts/auth.context';

import 'bootstrap/dist/css/bootstrap.min.css';
import './scss/one-page-wonder.scss';


function App() {
  const [token, setToken] = useState(getTokenFromLocalStorage);
  const [permission, setPermission] = useState<string[]>([]);

    return (
    <div className="App">
      <AuthProvider
        value={{
          token,
          setToken,
          permission,
          setPermission,
        }}
      >
        <Router>
          <Navigation />
          <Switch>
            <Route path="/" exact component={() => <Home />} />
            <Route path="/search" exact component={() => <Search />} />
            <Route path="/request" exact component={() => <Request />} />
            <Route path="/admin" exact component={() => <Admin />} />
            <Route path="/profile" exact component={() => <Profile />} />
            <Route path="/login" exact component={() => <Login />} />
            <Route path="/callback" exact component={() => <Callback />} />
          </Switch>
          <Footer />
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
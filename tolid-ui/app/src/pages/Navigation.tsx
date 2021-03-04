import React from "react";
import { Link, withRouter, useHistory } from "react-router-dom";
import { useAuth } from '../contexts/auth.context';
import { authLogout } from '../services/auth/authService';
import {
  setTokenToLocalStorage,
} from '../services/localStorage/localStorageService';

interface NavigationProps {
  location: {pathname: string};
}

function Navigation(props: NavigationProps) {
  const { token, setToken } = useAuth();
  const history = useHistory();

  const logout = function() {
    authLogout().finally(() => {
      setTokenToLocalStorage('');
      setToken('');
      history.replace("/");
    })
  }

    return (
    <div className="navigation">
      <nav className="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
        <div className="container">
          <Link className="navbar-brand" to="/">ToLID</Link>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarResponsive">
            <ul className="navbar-nav ml-auto">
            <li
                className={`nav-item  ${
                  props.location.pathname === "/search" ? "active" : ""
                }`}
              >
                <Link className="nav-link" to="/search">
                  Search
                </Link>
              </li>
              {token &&
                <li
                  className={`nav-item  ${
                    props.location.pathname === "/request" ? "active" : ""
                  }`}
                >
                  <Link className="nav-link" to="/request">
                    Create
                  </Link>
                </li>
              } 
              {token &&
                <li
                  className={`nav-item  ${
                    props.location.pathname === "/admin" ? "active" : ""
                  }`}
                >
                  <Link className="nav-link" to="/admin">
                    Admin
                  </Link>
                </li>
              }
              {token &&
                <li
                  className={`nav-item  ${
                    props.location.pathname === "/profile" ? "active" : ""
                  }`}
                >
                  <Link className="nav-link" to="/profile">
                    Profile
                  </Link>
                </li>
              }
              {!token &&
                <li
                  className={`nav-item  ${
                    props.location.pathname === "/login" ? "active" : ""
                  }`}
                >
                  <Link className="nav-link" to="/login">
                    Login
                  </Link>
                </li>
              }
              {token &&
                <li
                  className="nav-item" 
                >
                    <a onClick={logout} className="nav-link" href="">Logout</a>
                </li>
              }

            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default withRouter(Navigation);
import React from "react";
import { Link, withRouter } from "react-router-dom";

interface NavigationProps {
  location: {pathname: string};
}

function Navigation(props: NavigationProps) {
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
              <li
                className={`nav-item  ${
                  props.location.pathname === "/request" ? "active" : ""
                }`}
              >
                <Link className="nav-link" to="/request">
                  Create
                </Link>
              </li>
              <li
                className={`nav-item  ${
                  props.location.pathname === "/admin" ? "active" : ""
                }`}
              >
                <Link className="nav-link" to="/admin">
                  Admin
                </Link>
              </li>
              <li
                className={`nav-item  ${
                  props.location.pathname === "/contact" ? "active" : ""
                }`}
              >
                <Link className="nav-link" to="/contact">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default withRouter(Navigation);
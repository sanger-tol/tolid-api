import React from "react";
import { withRouter, useHistory } from "react-router-dom";
import { Container, Navbar, Nav } from 'react-bootstrap';
import { useAuth } from '../contexts/auth.context';
import { authLogout } from '../services/auth/authService';
import {
  setTokenToLocalStorage,
  setUserToLocalStorage,
  tokenHasExpired
} from '../services/localStorage/localStorageService';

interface NavigationProps {
  location: {pathname: string};
}

function Navigation(props: NavigationProps) {
  const { token, setToken, user, setUser } = useAuth();
  const history = useHistory();


  const logout = function() {
    authLogout().finally(() => {
      setTokenToLocalStorage('');
      setUserToLocalStorage(null);
      setToken('');
      setUser(null);
      history.replace("/");
    })
  }

    return (
    <div className="navigation">
      <Navbar className="navbar-dark navbar-custom fixed-top" expand="lg">
        <Container>
          <Navbar.Brand href="/">ToLID</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link href="/search">
                Search
              </Nav.Link>
              {token && !tokenHasExpired(token) &&
                <Nav.Link className="nav-link" href="/request">
                  Create
                </Nav.Link>
              }
              {token && !tokenHasExpired(token) && user && user.roles && user.roles.some(role => role.role === "admin") &&
                <Nav.Link className="nav-link" href="/admin">
                  Admin
                </Nav.Link>
              }
              {token && !tokenHasExpired(token) &&
                <Nav.Link className="nav-link" href="/profile">
                  Profile
                </Nav.Link>
              }
              {(!token || tokenHasExpired(token)) &&
                <Nav.Link className="nav-link" href="/login">
                  Login
                </Nav.Link>
              }
              {token && !tokenHasExpired(token) &&
                <Nav.Link onClick={logout} className="nav-link" href="/">
                  Logout
                </Nav.Link>
              }
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}

export default withRouter(Navigation);
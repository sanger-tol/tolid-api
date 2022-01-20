/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React, { useCallback, useEffect } from 'react';
import { Container, Row, Col } from "react-bootstrap";
import { Redirect } from 'react-router-dom';
import { useAuth } from '../contexts/auth.context';
import { getUrlElixirLogin } from '../services/auth/authService';
import { getTokenFromLocalStorage, tokenHasExpired } from '../services/localStorage/localStorageService';
import {ReactComponent as ElixirLoginButton} from '../assets/btn-login.svg';

function Login() {
  const { token, setToken } = useAuth();
  useEffect(()=> {
    if(!getTokenFromLocalStorage()){
      setToken('');
    }
    // eslint-disable-next-line
  }, []);

  const login = useCallback(() => {
    getUrlElixirLogin().then((data: any) => {
      window.location.href = data.data.loginUrl;
    });
  }, []);
  return (!token || tokenHasExpired(token)) ? (
    <div className="login">
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <Container>
            <h1 className="masthead-heading mb-0">Login</h1>
          </Container>
        </div>
        <div className="bg-circle-1 bg-circle"></div>
        <div className="bg-circle-2 bg-circle"></div>
        <div className="bg-circle-3 bg-circle"></div>
        <div className="bg-circle-4 bg-circle"></div>
      </header>
      <section>
        <Container>
          <Row className="align-items-center">
            <Col lg="12" className="order-lg-1 text-center">
              <ElixirLoginButton id="elixirLoginButton" onClick={login}/>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  ) : (
    <Redirect to="/" />
  );
}

export default Login;
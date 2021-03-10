import React, { useCallback, useEffect } from 'react';
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
          <div className="container">
            <h1 className="masthead-heading mb-0">Login</h1>
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
            <div className="col-lg-12 order-lg-1 text-center">
              <ElixirLoginButton onClick={login}/>
            </div>
          </div>
        </div>
      </section>
    </div>
  ) : (
    <Redirect to="/" />
  );
}

export default Login;
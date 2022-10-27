/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React, { useCallback, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import { useAuth } from '../contexts/auth.context';
import { getUrlElixirLogin } from '../services/auth/authService';
import { getTokenFromLocalStorage, tokenHasExpired } from '../services/localStorage/localStorageService';
import { ReactComponent as ElixirLoginButton } from '../assets/btn-login.svg';

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
    <ElixirLoginButton onClick={login}/>
  ) : (
    <Redirect to="/" />
  );
}

export default Login;
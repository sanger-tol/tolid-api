/*
SPDX-FileCopyrightText: 2021 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Home, Profile, Search } from "./pages";
import { CreateTolpApp, Page } from '@tol/tol-ui'
import './scss/styling.scss';


const profile: Page = {
  name: 'Profile',
  auth_required: false,
  admin_only: false,
  ui_element: <Profile />
};

const search: Page = {
  name: 'Search',
  auth_required: true,
  admin_only: false,
  ui_element: <Search />
};

ReactDOM.render(
  <React.StrictMode>
    <CreateTolpApp
      brand='TOLID'
      home_page={<Home />}
      pages={[
        profile,
        search
      ]}
    />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import ReactDOM from 'react-dom';
import {
  Home,
  AddSpecies,
  PendingRequests,
  Profile,
  Search,
  Api
} from "./pages";
import reportWebVitals from "./reportWebVitals";
import { TolApp, Page, Dropdown } from '@tol/tol-ui';
import Logo from './assets/logo.png';
import "./scss/styling.scss";


const search: Page = {
  name: 'Search',
  element: <Search />
};

const api: Page = {
  name: 'Developers',
  element: <Api />
};

const profile: Page = {
  name: 'Profile',
  element: <Profile />,
  auth: true
};

const addSpecies: Page = {
  name: 'Add Species',
  element: <AddSpecies />,
};

const pendingRequests: Page = {
  name: 'Pending Requests',
  element: <PendingRequests />,
};

const admin: Dropdown = {
  name: 'Admin',
  pages: [addSpecies, pendingRequests],
  auth: ['admin']
};

ReactDOM.render( // eslint-disable-line
  <TolApp
    brand={
      <img
        src={Logo}
        alt="ToLID Logo"
        style={{
          height: 50,
          marginTop: -15,
          marginBottom: -15
        }}
      />
    }
    homePage={ <Home /> }
    pages={[
      search,
      api,
      profile,
      admin
    ]}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
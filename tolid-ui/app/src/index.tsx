/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import ReactDOM from 'react-dom';
import {
  Home,
  AddSpecies,
  PendingRequests,
  CreateRequest,
  Profile,
  Search
} from "./pages";
import reportWebVitals from "./reportWebVitals";
import { TolApp, Page, Dropdown } from '@tol/tol-ui';
import "./scss/styling.scss";


const createRequest: Page = {
  name: 'Create',
  element: <CreateRequest />
};

const profile: Page = {
  name: 'Profile',
  element: <Profile />
};

const search: Page = {
  name: 'Search',
  element: <Search />
};

const addSpecies: Page = {
  name: 'Add Species',
  element: <AddSpecies />,
  hidden: true
};

const pendingRequests: Page = {
  name: 'Requests',
  element: <PendingRequests />,
  hidden: true
};

const admin: Dropdown = {
  name: 'Admin',
  pages: [pendingRequests, addSpecies]
};

ReactDOM.render( // eslint-disable-line
  <TolApp
    brand="ToLID"
    homePage={ <Home /> }
    pages={[
      search,
      createRequest,
      profile,

      // dropdown
      admin,
      pendingRequests,
      addSpecies
    ]}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
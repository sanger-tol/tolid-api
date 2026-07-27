/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import ReactDOM from 'react-dom';
import {
  Home,
  AddSpecies,
  PendingRequests,
  Profile
} from "./pages";
import reportWebVitals from "./reportWebVitals";
import { SmartApp, TPageElements } from '@tol/tol-ui';
import Logo from './assets/logo.png';
import "./scss/styling.scss";


export const PAGE_ELEMENTS: TPageElements = {
  home: <Home />,
  addSpecies: <AddSpecies />,
  pendingRequests: <PendingRequests />,
  profile: <Profile />
};

ReactDOM.render( // eslint-disable-line
    <SmartApp
      id="tolid"
      brand={<img src={Logo} alt="ToLID Logo" style={{ height: 35 }} />}
      pageElements={PAGE_ELEMENTS}
      configurableBoards
    />
,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
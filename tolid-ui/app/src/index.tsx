/*
SPDX-FileCopyrightText: 2024 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import ReactDOM from 'react-dom';
import {
  Home,
  AddSpecies,
  MyTolids,
  PendingRequests,
} from "./pages";
import reportWebVitals from "./reportWebVitals";
import { SmartApp, TPageElements } from '@tol/tol-ui';
import Logo from './assets/logo.png';
import "./scss/styling.scss";


export const PAGE_ELEMENTS: TPageElements = {
  home: <Home />,
  addSpecies: <AddSpecies />,
  pendingRequests: <PendingRequests />,
  myTolids: <MyTolids />
};

ReactDOM.render( // eslint-disable-line
    <SmartApp
      id="tolid"
      brand={<img src={Logo} alt="ToLID Logo" style={{ height: 35 }} />}
      pageElements={PAGE_ELEMENTS}
    />
,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
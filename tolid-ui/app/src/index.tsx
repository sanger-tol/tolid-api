/*
SPDX-FileCopyrightText: 2023 Genome Research Ltd.

SPDX-License-Identifier: MIT
*/

import ReactDOM from 'react-dom';
import { Home } from "./pages";
import reportWebVitals from "./reportWebVitals";
import { TolApp, Page, Dropdown } from '@tol/tol-ui';
import "./scss/styling.scss";


/*
const timelines: Page = {
  name: 'Timelines',
  element: <Timelines />
};

const dropdown: Dropdown = {
  name: 'Dropdown',
  pages: [widgets, sunbursts],
  //auth: true,
  //admin: true
};
*/

ReactDOM.render( // eslint-disable-line
  <TolApp
    brand="ToLID"
    homePage={ <Home /> }
    pages={[]}
  />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
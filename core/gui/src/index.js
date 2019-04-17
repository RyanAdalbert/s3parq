import React from 'react';
import ReactDOM from 'react-dom';

import LoginPage from './Pages/LoginPage/LoginPage';
import AppPage from './Pages/AppPage/AppPage';

import * as serviceWorker from './serviceWorker';
import './index.css';

ReactDOM.render(<AppPage />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

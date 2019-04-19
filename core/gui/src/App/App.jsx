import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import styled from 'styled-components';

import AdminPage from '../Containers/AdminPage/AdminPage';
import LoginPage from '../Containers/LoginPage/LoginPage';

//Component fro Private Route

// Routes

const routes = [
  {
    path: '/admin',
    compontent: AdminPage
  },
  {
    path: '/login',
    component: LoginPage
  }
];
const App = () => <LoginPage />;

export default App;

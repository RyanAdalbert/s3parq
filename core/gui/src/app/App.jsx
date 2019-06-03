import React from 'react';
import styled from 'styled-components';
import { Router, Route } from 'react-router-dom';

import AdminPage from '../pages/AdminPage/AdminPage';
import LoginPage from '../pages/LoginPage/LoginPage';
import history from '../utils/history';
import PrivateRoute from './PrivateRoute';

// Styles
const AppContainer = styled.section`
  display: block;
`;

const App = () => (
  <AppContainer>
    <Router history={history}>
      <Route exact path="/" component={LoginPage} />
      <PrivateRoute path="/admin" component={AdminPage} />
    </Router>
  </AppContainer>
);

export default App;

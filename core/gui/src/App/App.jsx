import React from 'react';
import styled from 'styled-components';
import { Router, Route } from 'react-router-dom';

import AdminPage from '../views/AdminPage/AdminPage';
import LoginPage from '../views/LoginPage/LoginPage';
import history from '../utils/history';

// Styles
const AppContainer = styled.section`
  display: block;
`;

const App = () => (
  <AppContainer>
    <Router history={history}>
      <Route exact path="/" component={LoginPage} />
      <Route path="/admin" component={AdminPage} />
    </Router>
  </AppContainer>
);

export default App;
